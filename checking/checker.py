import copy
import logging
import os
import subprocess
import sys


class Checker(object):
    """Driver for checking host support for container tools"""

    def _call_check(self, cmd, **kw):
        """Execute command and capture results"""

        try:
            pid = subprocess.Popen([cmd],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   close_fds=True,
                                   env=kw['env'])
            out, err = pid.communicate()
        except OSError as e:
            return [], [e.strerror], e.errno
        except ValueError as e:
            return [], [e.message], os.errno.EINVAL
        return (
            out.strip().splitlines(), err.strip().splitlines(), pid.returncode
        )

    def check(self, path=None, debug=False):
        """Execute checks found at path and report results"""

        files = os.listdir(path)
        if not files:
            logging.error("{} contains no checks".format(path))
            return False

        filename_len = len(max(files, key=len))

        def is_exec(p):
            """Does the given path point to an executable?"""
            return os.path.isfile(p) and os.access(p, os.X_OK)

        # build environment to run check in
        env = {}
        pythonpath = copy.deepcopy(sys.path)
        pythonpath.append('.')
        env['PYTHONPATH'] = os.pathsep.join(pythonpath)

        if debug:
            env['DEBUG'] = 'True'

        error = False
        for file in files:
            cmd = os.path.join(path, file)

            def fmt(msg, prefix=''):
                """Capture details for logging"""
                return '{:{w}} | {}{}'.format(
                    file, prefix, msg, w=filename_len
                )

            if not is_exec(cmd):
                logging.warn(fmt('Is not executable'))
            else:
                out, err, rc = self._call_check(cmd, env=env)

                if rc == 0:
                    if not out:
                        out = ['Completed successfully']
                else:
                    error = True
                    if not err:
                        err = ['Failed with return code: {}'.format(rc)]
                logging.debug('{} return code: {}'.format(cmd, rc))

                if err:
                    logging.error(fmt(err[0]))
                    for line in err[1:]:
                        logging.error(fmt(line, '+- '))

                if out:
                    logging.info(fmt(out[0]))
                    for line in out[1:]:
                        logging.info(fmt(line, '+- '))
        return not error
