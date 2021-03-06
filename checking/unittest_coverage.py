#!/usr/bin/env python

import sys
import unittest

import coverage
import coverage.version

OPTIONS = {
    'data_file': '.coverage',
    'branch': True,
    'include': [
        'checking/*',
        'container_check',
    ],
    'omit': [
        '*.sh',
        '*/test_*.py',
    ]
}

if __name__ == '__main__':
    """Run unit tests with coverage."""
    cov = coverage.coverage(**OPTIONS)

    try:
        cov.start()
        suite = unittest.TestLoader().discover('checking')
        result = unittest.TextTestRunner(verbosity=1).run(suite)

        if result.wasSuccessful():
            cov.stop()
            print('\nCoverage Summary:\n')
            cov.report(show_missing=True)

            # writing html report is optional depending on /host mounts
            try:
                covdir = '/host/var/tmp/coverage'
                cov.html_report(directory=covdir)
                print('HTML version: file://%s/index.html' % covdir)
            except IOError:
                pass
            sys.exit(0)
    finally:
        cov.erase()
    sys.exit(1)
