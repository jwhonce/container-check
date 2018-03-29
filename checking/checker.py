import logging
import os
import subprocess
import sys


class Checker(object):
    """Driver for checking host support for container tools"""

    def check(self, path=None, debug=False):
        files = os.listdir(path)
        if not files:
            logging.error("{} contains no checks".format(path))
            return False

        filename_len = len(max(files, key=len))

        # build environment to run check in
        env = {}
        env['PYTHONPATH'] = ':'.join(sys.path) + ':.'

        if debug:
            env['DEBUG'] = 'True'

        def is_exec(p):
            """Does the given path point to an executable?"""
            return os.path.isfile(p) and os.access(p, os.X_OK)

        error = False
        for file in files:
            cmd = os.path.join(path, file)

            def fmt(msg):
                """Capture details for logging"""
                return '{:{w}} | {}'.format(file, msg, w=filename_len)

            if is_exec(cmd):
                try:
                    output = subprocess.check_output(
                        cmd, close_fds=True, stderr=subprocess.STDOUT, env=env
                    ).strip()

                    if not output:
                        output = 'Completed successfully'

                    logging.info(fmt(output))
                except subprocess.CalledProcessError as e:
                    error = True
                    cooked = e.output.strip()
                    logging.error(fmt(cooked if cooked else str(e)))
                    logging.debug(str(e))
                    continue
            else:
                logging.warn(fmt('Is not executable'))

        return not error
