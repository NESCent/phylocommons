#!/usr/bin/env python2
import os
import sys

os.environ['LANG'] = 'en_US'
os.environ['LC_ALL'] = 'en_US'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phylofile.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
