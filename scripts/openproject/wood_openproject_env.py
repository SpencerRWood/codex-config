"""Shared repository-environment helpers for global OpenProject commands."""

from __future__ import annotations

import os
from pathlib import Path

from wood_project.openproject import OpenProjectClient, OpenProjectSettings


ROOT_ID_ENV_KEYS = (
    "OPENPROJECT_INITIATIVE_ID",
    "OPENPROJECT_ROOT_WORK_PACKAGE_ID",
    "OPENPROJECT_ROOT_ID",
)
GLOBAL_CREDENTIAL_FILE = Path.home() / ".wood" / "runtime" / "openproject.env"


def parse_env(path: Path) -> dict[str, str]:
    if not path.exists():
        raise ValueError(f"Environment file not found: {path}")
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def selected_env_file(value: Path | None) -> Path:
    if value is not None:
        return value
    return Path.cwd() / ".env"


def openproject_token(repo_env: dict[str, str]) -> str:
    """Load the shared credential, with a concrete repo token as a fallback."""
    global_env = parse_env(GLOBAL_CREDENTIAL_FILE) if GLOBAL_CREDENTIAL_FILE.exists() else {}
    token = global_env.get("OPENPROJECT_API_TOKEN") or repo_env.get("OPENPROJECT_API_TOKEN", "")
    if not token:
        raise ValueError(
            f"Set OPENPROJECT_API_TOKEN in {GLOBAL_CREDENTIAL_FILE} or in the selected env file."
        )
    if token.startswith(("vaultwarden://", "env://")):
        raise ValueError(
            f"OPENPROJECT_API_TOKEN must be a concrete value in {GLOBAL_CREDENTIAL_FILE} "
            "or the selected env file."
        )
    return token


def initiative_id(env: dict[str, str], explicit: int | None = None) -> int:
    if explicit is not None:
        return explicit
    for key in ROOT_ID_ENV_KEYS:
        if value := env.get(key):
            try:
                return int(value)
            except ValueError as exc:
                raise ValueError(f"{key} must be an integer.") from exc
    raise ValueError(
        "Set OPENPROJECT_INITIATIVE_ID (or a supported root work-package ID) in the env file."
    )


def client_from_env(env: dict[str, str], *, user_agent: str) -> OpenProjectClient:
    base_url = env.get("OPENPROJECT_URL", "").rstrip("/")
    if not base_url:
        raise ValueError("The env file must define OPENPROJECT_URL.")
    token = openproject_token(env)
    global_env = parse_env(GLOBAL_CREDENTIAL_FILE) if GLOBAL_CREDENTIAL_FILE.exists() else {}
    ca_file = env.get("SSL_CERT_FILE") or global_env.get("SSL_CERT_FILE")
    if ca_file:
        if not Path(ca_file).is_file():
            raise ValueError(f"SSL_CERT_FILE does not exist or is not a file: {ca_file}")
        os.environ["SSL_CERT_FILE"] = ca_file
    return OpenProjectClient(
        OpenProjectSettings(
            base_url=base_url,
            token=token,
            token_provider="repository-env-file",
            user_agent=user_agent,
            project_id=env.get("OPENPROJECT_PROJECT_ID") or "",
        )
    )
