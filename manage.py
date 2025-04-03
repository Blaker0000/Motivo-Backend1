#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""

import os
import sys

def main():
    """
    Run administrative tasks.
    
    This function sets the default Django settings module (motivo_backend.settings)
    and then calls Django's built-in command line functionality.
    """
    # 1. Tell Python which Django settings to use.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motivo_backend.settings')
    
    try:
        # 2. Import Django's command execution function.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 3. If Django isn’t installed or something is missing, raise an error.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 4. Run Django’s command-line utility with the arguments provided.
    execute_from_command_line(sys.argv)

# 5. If you run this file directly (python manage.py ...), call main().
if __name__ == '__main__':
    main()
