#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


project_dir = Path(__file__).resolve().parent.parent / "example_project"

subprocess.run(
    [sys.executable, "manage.py", "test"],
    cwd=project_dir,
    check=True,
)
