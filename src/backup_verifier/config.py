from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class BackupTarget(BaseModel):
    name: str
    type: str = Field(..., pattern="^(restic|postgres)$")
    repo_path: str
    password_env: str
    max_rpo_hours: int = 24
    expected_file: str

class Settings(BaseModel):
    version: str
    targets: list[BackupTarget]

def load_config(config_path: Path) -> Settings:
    """Loads and validates the YAML configuration file using Pydantic."""
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        raw_data = yaml.safe_load(f)
    
    return Settings(**raw_data)
