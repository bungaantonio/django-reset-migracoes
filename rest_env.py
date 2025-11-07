#!/usr/bin/env python3
"""
DJANGO ENVIRONMRNT RESET TOOL.

This script performs a clean rebuild of a Django project environment.
It can:
- Delete the local SQLite database (optional)
- Clean old migration files
- Generate and apply new migrations
- Install dependencies from requirements.txt

Fully cross-platform (Windows, macOS, Linux).
Safe for both local development and CI/CD pipelines.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DB_PATH = Path("./db.sqlite3")
REQ_PATH = Path("./requirements.txt")

# Detect CI environment (GitHub Actions, GitLab CI, etc.)
IN_CI = os.getenv("CI", "").lower() in {"true", "1"}

# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def color(text: str, code: str) -> str:
    """Return colored terminal text."""
    return f"\033[{code}m{text}\033[0m"

def run_cmd(cmd: list[str], check: bool = True):
    """Run a subprocess command and display it."""
    print(color(f"\n→ Executing: {' '.join(cmd)}", "94"))  # blue
    result = subprocess.run(cmd, check=check)
    return result

def confirm(message: str, force: bool) -> bool:
    """Ask for confirmation, unless --yes or CI mode is active."""
    if force or IN_CI:
        return True
    while True:
        resp = input(f"{message} (y/n): ").lower().strip()
        if resp == "y":
            return True
        elif resp == "n":
            return False
        print("Please respond with 'y' or 'n'.")

# ---------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------
def delete_db(force: bool):
    if DB_PATH.exists():
        if confirm(f"Delete database '{DB_PATH}'?", force):
            DB_PATH.unlink()
            print(color(f"Database deleted: {DB_PATH}", "92"))
        else:
            print("Operation cancelled.")
            sys.exit(0)
    else:
        print(f"Database not found: {DB_PATH}")

def clear_migrations(force: bool):
    migrations = [
        p for p in Path(".").rglob("migrations")
        if (p / "__init__.py").exists() and ".venv" not in str(p)
    ]
    if not migrations:
        print("No migration folders found.")
        return

    print("Found migration folders:")
    for m in migrations:
        print(f" - {m}")

    if confirm("Remove all migration files (except __init__.py)?", force):
        for folder in migrations:
            for file in folder.rglob("*.py"):
                if file.name != "__init__.py":
                    print(f"Deleting: {file}")
                    file.unlink()
            for cache in folder.rglob("__pycache__"):
                shutil.rmtree(cache, ignore_errors=True)
        print(color("Migration files cleaned.", "92"))
    else:
        print("Migration cleanup cancelled.")

def apply_migrations():
    try:
        run_cmd([sys.executable, "manage.py", "makemigrations"])
        run_cmd([sys.executable, "manage.py", "migrate"])
        print(color("Migrations applied successfully.", "92"))
    except subprocess.CalledProcessError:
        print(color("Error while applying migrations.", "91"))
        sys.exit(1)

def install_requirements(force: bool):
    if REQ_PATH.exists() and confirm(f"Install dependencies from '{REQ_PATH}'?", force):
        try:
            run_cmd([sys.executable, "-m", "pip", "install", "-r", str(REQ_PATH)])
            print(color("Dependencies installed successfully.", "92"))
        except subprocess.CalledProcessError:
            print(color("Error while installing dependencies.", "91"))
            sys.exit(1)
    else:
        print(f"File '{REQ_PATH}' not found or installation skipped.")

# ---------------------------------------------------------------------
# CLI and main flow
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Reset Django environment safely.")
    parser.add_argument("--yes", "-y", action="store_true",
                        help="Run without interactive confirmations.")
    parser.add_argument("--skip-db", action="store_true",
                        help="Skip deleting the database file.")
    parser.add_argument("--skip-clean", action="store_true",
                        help="Skip migration cleanup.")
    parser.add_argument("--skip-install", action="store_true",
                        help="Skip dependency installation.")
    return parser.parse_args()

def main():
    args = parse_args()
    print(color("\n--- Django Environment Reset ---", "96"))  # cyan

    if not args.skip_db:
        delete_db(args.yes)
    if not args.skip_clean:
        clear_migrations(args.yes)

    apply_migrations()

    if not args.skip_install:
        install_requirements(args.yes)

    print(color("\nEnvironment reset completed successfully!", "92"))

if __name__ == "__main__":
    main()
