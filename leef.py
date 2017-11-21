#!/usr/bin/python

"""
Based off of the IBM Guide for LEEF 1.0 - http://goo.gl/8u4Kfg
Code almost entirely borrowed from RyPeck
https://github.com/RyPeck/python-LEEF

usage:
from leef import LEEF_Logger
a = LEEF_Logger('vendor',
                'product name',
                1.1,
                2,
                0,
                '\t',
                '127.0.0.1'
                )
a.logEvent('Accept', {  'message': 'dude',
                        'userName': 'Brian'})
"""

from __future__ import print_function
import syslog_client

__version__ = '0.1.0'

class LEEF_Logger:
    import syslog_client
    """LEEF LOGGER"""
    # LEEF Headers
    version_major = None
    version_minor = None
    product_vendor = None
    product_name = None
    product_version = None

    def __init__(   self,
                    product_vendor,
                    product_name,
                    product_version,
                    version_major,
                    version_minor,
                    delimiter,
                    dest):
        """ Define the LEEF Headers for the application logging """
        self.version_major = version_major
        self.version_minor = version_minor
        self.product_vendor = product_vendor
        self.product_name = product_name
        self.product_version = product_version
        if delimiter not in ['\t', '|', '^']:
            raise ValueError("Delimeter must be '\\t', '|' or '^'")
        self.delimiter = delimiter
        self.log = syslog_client

    def logEvent(self, event_id, keys):
        """
        Log an event
        """
        log = self._createEventString(event_id, keys)
        print(log)
        self.log.send(  log,
                        self.log.INFO)
        #return self._createEventString(event_id, keys)

    def _createEventString(self, event_id, keys):
        header = self._createHeader(event_id)
        values = sorted([(str(k) + "=" + str(v))
                         for k, v in iter(keys.items())])
        payload = '\t'.join(values)
        return (header + payload)

    def _createHeader(self, event_id):
        return 'LEEF:{0}.{1}|{2}|{3}|{4}|{5}|'.format(
                    self.version_major,
                    self.version_minor,
                    self.product_vendor,
                    self.product_name,
                    self.product_version,
                    event_id)
