#!/usr/bin/env python
# Copyright (c) Jack Bortone 2007-2011 <jack@isotopesoftware.ca>
# All rights reserved.
# <LICENSE=ISC>

import logging
logging.basicConfig(level=logging.DEBUG)

import logging.handlers 

# default logger for this app will be syslog
rootLogger = logging.getLogger(__name__)
syslogHandler = logging.handlers.SysLogHandler(
        address="/dev/log", facility=16
        )
rootLogger.addHandler(syslogHandler)
#rootLogger.debug('this is a test msg sent to the syslog daemon!')

def log_to_syslog(s, emitter=rootLogger.debug
    ):
    try:
        emitter(s)
    except:
        #problem emitting log record..
        raise
    return None

logger_func = lambda msg: log_to_syslog(msg)

