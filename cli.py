from pathlib import Path
import typer
from loguru import logger
from backup_verifier.config import load_config
from backup_verifier.verifier import run_restic_check

app = typer.Typer(help="Automated nightly backup verification tool")

@app.command()
def run(
    config: Path = typer.Option(
        "targets.yaml",
        "--config",
        "-c",
        help="Path to the YAML configuration file",
    ),
    sandbox: Path = typer.Option(
        "sandbox-restore",
        "--sandbox",
        "-s",
        help="Path to the temporary sandbox restore folder",
    ),
):
    """Runs the backup verification pipeline for all targets in the config."""
    logger.info(f"Loading configuration from {config}...")
    try:
        settings = load_config(config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise typer.Exit(code=1)

    success_all = True
    for target in settings.targets:
        logger.info(f"--- Verifying target: {target.name} (type: {target.type}) ---")
        
        # Get password from environment variable specified in YAML
        import os
        password = os.environ.get(target.password_env)
        if not password:
            logger.error(f"Environment variable '{target.password_env}' is not set!")
            success_all = False
            continue

        if target.type == "restic":
            success = run_restic_check(
                repo_path=target.repo_path,
                password=password,
                expected_file=target.expected_file,
                sandbox_path=sandbox,
            )
            if not success:
                success_all = False
        else:
            logger.warning(f"Target type '{target.type}' is not supported yet.")

    if not success_all:
        logger.error("Some backup verifications FAILED.")
        raise typer.Exit(code=1)
    
    logger.info("All backup verifications passed successfully!")

if __name__ == "__main__":
    app()
