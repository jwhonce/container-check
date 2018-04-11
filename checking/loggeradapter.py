import logging


class LoggerAdapter(logging.LoggerAdapter):
    """Ensure LoggerAdapter has a value for %(script) fomatting"""

    def process(self, msg, kwargs):
        if 'extra' in kwargs:
            extra = self.extra.copy()
            extra.update(kwargs['extra'])
            kwargs['extra'] = extra
        else:
            kwargs['extra'] = self.extra

        if 'script' not in kwargs['extra'].keys():
            kwargs['extra']['script'] = ''

        return msg, kwargs
