#!/usr/bin/env python3
"""
Bootstrap script — run once after clicking "Use this template" on GitHub.

Usage:
    python scripts/bootstrap.py

This script renames all occurrences of `project_name` and placeholder
values to your actual project details.
"""

import os
import re
import shutil
from pathlib import Path


def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    value = input(f"{label}{hint}: ").strip()
    return value or default


def replace_in_file(path: Path, replacements: dict[str, str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError):
        pass  # skip binary files


def main() -> None:
    print("\n🚀  Python Project Blueprint — Bootstrap\n")

    project_name = prompt("Project name (snake_case)", "my_project")
    project_title = prompt("Project title (human readable)", project_name.replace("_", " ").title())
    description = prompt("Short description", "A Python project.")
    author = prompt("Your name", "Your Name")
    email = prompt("Your email", "you@example.com")
    github_username = prompt("GitHub username", "YOUR_USERNAME")
    repo_name = prompt("GitHub repo name", project_name.replace("_", "-"))

    replacements = {
        "project_name": project_name,
        "project-name": project_name.replace("_", "-"),
        "Project Name": project_title,
        "Short description of your project": description,
        "Your Name": author,
        "you@example.com": email,
        "YOUR_USERNAME": github_username,
        "YOUR_REPO": repo_name,
    }

    root = Path(__file__).parent.parent
    skip_dirs = {".git", ".venv", "venv", "__pycache__", "node_modules"}

    print("\n📝  Renaming files and updating content...")

    # Rename src/project_name/ directory
    old_src = root / "src" / "project_name"
    new_src = root / "src" / project_name
    if old_src.exists() and project_name != "project_name":
        shutil.move(str(old_src), str(new_src))
        print(f"   Renamed src/project_name/ → src/{project_name}/")

    # Replace content in all text files
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            replace_in_file(path, replacements)

    print("\n✅  Done! Next steps:")
    print(f"   1. cd {repo_name}")
    print("   2. git init && git add . && git commit -m 'chore: initialise project'")
    print("   3. make install")
    print("   4. Start building 🎉\n")


if __name__ == "__main__":
    main()
