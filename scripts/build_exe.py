"""
EstimateFlex Build Script
PyInstaller executable packaging

Utilisation :
    python scripts/build_exe.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"

# IMPORTANT : fichier spec conservé
SPEC_FILE = ROOT / "EstimateFlex.spec"


def header():
    print("=" * 60)
    print("EstimateFlex Build System")
    print("=" * 60)


def clean():
    print("\n[1/4] Cleaning previous builds...")

    for folder in (BUILD_DIR, DIST_DIR):
        if folder.exists():
            shutil.rmtree(folder)
            print(f"Deleted: {folder}")

    # NE PAS supprimer le .spec
    if not SPEC_FILE.exists():
        raise FileNotFoundError(f"Fichier spec introuvable : {SPEC_FILE}")


def build_pyinstaller():
    print("\n[2/4] Building executable...")

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        str(SPEC_FILE),
    ]

    print(" ".join(cmd))

    subprocess.run(
        cmd,
        cwd=ROOT,
        check=True,
    )


def copy_extra_resources():
    print("\n[3/4] Copying resources...")

    app_dir = DIST_DIR / "EstimateFlex"

    extras = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
    ]

    for item in extras:
        source = ROOT / item

        if source.exists():
            shutil.copy2(source, app_dir)
            print(f"Copied: {item}")


def summary():
    print("\n[4/4] Build Complete")

    app_dir = DIST_DIR / "EstimateFlex"

    print(f"\nApplication: {app_dir}")
    print("\nExecutable created successfully.")


def main():
    header()

    try:
        clean()
        build_pyinstaller()
        copy_extra_resources()
        summary()

    except subprocess.CalledProcessError as exc:
        print("\nBuild failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:
        print("\nUnexpected error")
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
