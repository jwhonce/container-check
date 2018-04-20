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
    cov = coverage.coverage(**OPTIONS)

    cov.start()
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('checking')
    result = unittest.TextTestRunner(verbosity=1).run(tests)

    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print('Coverage Summary: {}'.format(coverage.version.__version__))
        cov.report(show_missing=True)

        # this doesn't work :(
        covdir = '/host/var/tmp/coverage'
        print cov.html_report(directory=covdir, title='ContainerCheck')
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()
        sys.exit(0)
    sys.exit(1)
