#!/usr/bin/env python
"""Entry point for Django management commands such as runserver and migrate."""

# os lets this script set environment variables before Django starts.
import os

# sys gives access to command-line arguments like runserver or test.
import sys


def main():
    """Configure Django and pass the typed command to Django's CLI runner."""
    # This tells Django which settings file should be used for this project.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')
    try:
        # This is Django's built-in command runner.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # This error message helps if Django is missing or the virtual environment is inactive.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # This line forwards the typed command, for example `python manage.py runserver`.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Only run main() when this file is executed directly.
    main()
