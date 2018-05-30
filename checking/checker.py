import copy
import logging
import os
import subprocess
import sys

import loggeradapter


class Checker(object):
    """Driver for checking host support for container tools."""

    def __init__(self, debug):
        """Construct Checker object."""
        self._debug = debug
        self._env = {}

        # build environment to run check in
        pythonpath = copy.deepcopy(sys.path)
        pythonpath.append('.')
        self._env['PYTHONPATH'] = os.pathsep.join(pythonpath)

        if debug:
            self._env['DEBUG'] = 'True'

    @property
    def env(self):
        """Environment for running checks."""
        return copy.deepcopy(self._env)

    def _call_check(self, cmd, **kw):
        """Execute command and capture results."""
        try:
            pid = subprocess.Popen(
                [cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                env=kw['env'])
            out, err = pid.communicate()

            return (
                out.strip().splitlines(),
                err.strip().splitlines(),
                pid.returncode,
            )
        except OSError as e:
            return [], [e.strerror], e.errno
        except ValueError as e:
            return [], [e.message], os.errno.EINVAL

    def _is_exec(self, p):
        """Return True path points to an executable."""
        return os.path.isfile(p) and os.access(p, os.X_OK)

    def check(self, path):
        """Execute checks found at path(s) and report results."""
        error = False
        log = loggeradapter.LoggerAdapter(logging.getLogger(),
                                          {'script': os.path.basename(path)})

        if not self._is_exec(path):
            log.warning('"{}" is not executable'.format(path))
            error = True
        else:
            out, err, rc = self._call_check(path, env=self._env)

            if rc == 0:
                if not out:
                    out = ['Completed successfully']
            else:
                error = True
                if not err:
                    err = ['Failed with return code: {}'.format(rc)]
            log.debug('{} return code: {}'.format(path, rc))

            if err:
                log.error(err[0])
                for line in err[1:]:
                    log.error('+- {}'.format(line))

            if out:
                log.info(out[0])
                for line in out[1:]:
                    log.info('+- {}'.format(line))
        return not error
