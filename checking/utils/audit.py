from __future__ import absolute_import

import auparse
import datetime
import os

from .pathname import Pathname


class Audit(object):
    def __init__(self, path, prefix='/host'):
        self._logfile = Pathname(path, prefix)

        epoch = datetime.datetime.utcfromtimestamp(0)
        now = datetime.datetime.now() - datetime.timedelta(days=30)
        self._30day_delta = (now - epoch).total_seconds()

        try:
            self._parser = auparse.AuParser(
                auparse.AUSOURCE_FILE, self._logfile
            )
        except IOError as e:
            raise IOError(e.errno, os.strerror(e.errno), self._logfile.relpath)
        except OSError as e:
            raise OSError(e.errno, os.strerror(e.errno), self._logfile.relpath)

    def avc(self, by_time=True):
        self._parser.search_add_item(
            'type', '=', 'AVC', auparse.AUSEARCH_RULE_CLEAR
        )

        if by_time:
            self._parser.search_add_timestamp_item(
                '>', self._30day_delta, 0, auparse.AUSEARCH_RULE_AND
            )
        self._parser.search_set_stop(auparse.AUSEARCH_STOP_EVENT)

        try:
            # Events group records which have fields
            while self._parser.search_next_event():
                for record in range(self._parser.get_num_records()):
                    fields = {'timestamp': self._parser.get_timestamp()}
                    for field in range(self._parser.get_num_fields()):
                        fields[self._parser.get_field_name()] \
                            = self._parser.interpret_field()
                        self._parser.next_field()
                    yield fields

                    self._parser.next_record()
                self._parser.parse_next_event()
        finally:
            self._parser.reset()
