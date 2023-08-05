import logging
import os

from ..vendor import ntplib


logger = logging.getLogger(__name__)
offset = None


class RecoverableClientError(Exception):
    def __init__(self, response):
        msg = 'Recoverable client error {status} in ingest.'.format(status=response.status)
        super(RecoverableClientError, self).__init__(msg)


class UnrecoverableClientError(Exception):
    def __init__(self, response):
        msg = 'Unrecoverable client error {status} in ingest: {response}.'.format(
            status=response.status, response=response.data
        )
        super(UnrecoverableClientError, self).__init__(msg)


def fix_timestamps(span):
    global offset
    if offset is None:
        try:
            offset = ntplib.NTPClient().request("pool.ntp.org", version=3).offset
            logger.debug("detected time offset using NTP: %f", offset)
        except Exception as e:
            logger.debug("could not determine time offset using NTP: %s", e)
            offset = 0

    span.start_time += offset
    for event in span.logs:
        event.timestamp += offset

    return span


class ProcessLocal:
    """
    Provides a basic per-process mapping container that wipes itself if the current PID changed since the last get/set.
    Aka `threading.local()`, but for processes instead of threads.
    """

    __pid__ = -1

    def __init__(self, mapping_factory=dict):
        self.__mapping_factory = mapping_factory

    def __handle_pid(self):
        new_pid = os.getpid()
        if self.__pid__ != new_pid:
            self.__pid__, self.__store = new_pid, self.__mapping_factory()

    def __delitem__(self, key):
        self.__handle_pid()
        return self.__store.__delitem__(key)

    def __getitem__(self, key):
        self.__handle_pid()
        return self.__store.__getitem__(key)

    def __contains__(self, item):
        self.__handle_pid()
        return self.__store.__contains__(item)

    def __setitem__(self, key, val):
        self.__handle_pid()
        return self.__store.__setitem__(key, val)
