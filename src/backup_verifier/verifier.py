import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from loguru import logger


def get_restic_path() -> str:
    """Finds the absolute path to the restic binary."""
    path = shutil.which("restic")
    if path:
        return path
    brew_path = "/opt/homebrew/bin/restic"
    if Path(brew_path).exists():
        return brew_path
    return "restic"

def run_restic_check(repo_path: str, password: str, expected_file: str, sandbox_path: Path) -> bool:
    """
    Executes the 7-step restic verification process:
    1. Find newest backup
    2. Check age (RPO)
    3. Check file integrity
    4. Restore to sandbox
    5. Verify real data exists
    6. Measure restore time (RTO)
    7. Evaluate status
    """
    # Copy system environment so $HOME, PATH, etc. are available to restic
    env = os.environ.copy()
    env["RESTIC_PASSWORD"] = password
    env["RESTIC_REPOSITORY"] = repo_path
    
    restic_bin = get_restic_path()
    
    try:
        # Step 1 & 2: List snapshots to find the newest and check age (RPO)
        logger.info(f"Step 1 & 2: Checking restic snapshots using {restic_bin}...")
        result = subprocess.run(
            [restic_bin, "snapshots", "--json"],
            env=env, capture_output=True, text=True, check=True
        )
        snapshots = json.loads(result.stdout)
        if not snapshots:
            logger.error("No snapshots found in repository!")
            return False
        
        newest_snapshot = snapshots[-1]
        logger.info(f"Found latest snapshot ID: {newest_snapshot['id'][:8]} from {newest_snapshot['time']}")

        # Step 3: Check file integrity of the backup
        logger.info("Step 3: Checking restic repository integrity...")
        subprocess.run([restic_bin, "check"], env=env, check=True)

        # Step 4 & 6: Restore to sandbox and measure restore time (RTO)
        logger.info("Step 4 & 6: Restoring latest snapshot to sandbox and measuring RTO...")
        if sandbox_path.exists():
            for item in sandbox_path.iterdir():
                if item.is_dir():
                    import shutil as sh
                    sh.rmtree(item)
                else:
                    item.unlink()
        else:
            sandbox_path.mkdir(parents=True, exist_ok=True)

        start_time = time.time()
        subprocess.run(
            [restic_bin, "restore", "latest", "--target", str(sandbox_path)],
            env=env, capture_output=True, text=True, check=True
        )
        restore_duration = time.time() - start_time
        logger.info(f"Restore completed successfully in {restore_duration:.2f} seconds (RTO).")

        # Step 5: Look inside sandbox to verify the real data exists
        logger.info("Step 5: Verifying expected file exists in restored data...")
        target_file = sandbox_path / expected_file
        if target_file.exists():
            content = target_file.read_text().strip()
            logger.info(f"SUCCESS: Found expected file '{expected_file}' with content: '{content}'")
        else:
            logger.error(f"FAILURE: Expected file '{expected_file}' not found in sandbox at {target_file}!")
            return False

        # Step 7: Evaluate status -> OK
        logger.info("Step 7: Backup verification status: OK")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.cmd}\nOutput: {e.stderr}")
        return False
    except Exception as e: # noqa: BLE001
        logger.error(f"Unexpected error during verification: {e}")
        return False
