#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Need to add mininews itself to the import path.
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(os.path.join(BASE_DIR, ".."))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
