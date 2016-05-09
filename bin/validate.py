"""
Validate rst data in `description` & `summary` fields of json files.

Usage::

    python bin/validate.py
    python bin/validate.py bostonpy

"""

import glob
import json
import logging
import subprocess
import sys

import restructuredtext_lint


DATA_DIR = 'data'
LOG_FILENAME = 'pyvideo.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def validate_rst(rst):
    errors = restructuredtext_lint.lint(rst)
    return errors


def validate_file(file_path):
    with open(file_path) as fp:
        content = json.load(fp)

    errors = []
    for section_name in ('description', 'summary'):
        section = content.get(section_name)
        if section:
            error = validate_rst(section)
            if error:
                errors.append({
                    'file_path': file_path,
                    section_name: section,
                    'error':  error[0].message
                })
    return errors


def run_command(command):
    output = subprocess.check_output(command.split())
    return output.decode('utf-8').split('\n')


if __name__ == '__main__':

    conference = sys.argv[1:]
    if conference:
        pattern = '{}/{}/**/*.json'.format(DATA_DIR, conference[0])
    else:
        pattern = '{}/**/**/*.json'.format(DATA_DIR)

    json_files = glob.iglob(pattern, recursive=True)

    for json_file in json_files:
        errors = validate_file(json_file)
        if errors:
            logging.warning('conference: {}'.format(conference))
            logging.warning(errors)
