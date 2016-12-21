"""
Alternative monitor for PostgreSQL CSV logs. This was written against the log
format of PostgreSQL 9.1. Note that the CSV format might change across
versions, and this script might breach. However, it is easily changed!
"""
from collections import namedtuple
from time import sleep
import csv
import sys

try:
    from term import render
    def emit(text):
        print render(text)
except ImportError:
    # Terminal module not available
    def emit(text):
        print text

LogRecord = namedtuple("LogRecord",
                       'log_time,'
                       'user_name,'
                       'database_name,'
                       'process_id,'
                       'connection_from,'
                       'session_id,'
                       'session_line_num,'
                       'command_tag,'
                       'session_start_time,'
                       'virtual_transaction_id,'
                       'transaction_id,'
                       'error_severity,'
                       'sql_state_code,'
                       'message,'
                       'detail,'
                       'hint,'
                       'internal_query,'
                       'internal_query_pos,'
                       'context,'
                       'query,'
                       'query_pos,'
                       'location,'
                       'application_name')


class StreamIterator(object):
    """
    Python's default CSV reader assumes that the values don't contain
    newlines. It reads files linewise. This poses problems for PostgreSQL
    logs, if the queries contained newlines. As the log records are properly
    escaped however, we can deal with this.

    This iterator will read the files *bytewise* and emit new CSV records only
    if a newline is found which is *not* inside an escaped string value.
    """
    def __init__(self, f):
        self.f = f
        self.inside_quote = False

    def __iter__(self):
        return self

    def next(self):
        last_char = ''
        inside_quote = False
        char = self.f.read(1)
        output = []
        while True:
            if char == '\n' and not inside_quote:
                return ''.join(output)

            if char == '"':
                inside_quote = not inside_quote

            output.append(char)
            last_char = char
            char = self.f.read(1)

            while not char:
                # keep reading ("tail -f" like behaviour)
                sleep(0.1)
                char = self.f.read(1)


def printout(record):
    """
    Simple handler for log records. Prints the log record to stdout
    """

    if record.error_severity == 'ERROR':
        emit("%(BOLD)s%(RED)s{0.log_time} "
             "{0.user_name} "
             '{0.database_name} '
             '{0.connection_from} '
             '{0.error_severity} '
             '{0.application_name}%(NORMAL)s\n'
             '%(YELLOW)s{0.message}%(NORMAL)s'.format(record))
    else:
        emit("%(BOLD)s{0.log_time} "
             "{0.user_name} "
             '{0.database_name} '
             '{0.connection_from} '
             '{0.error_severity} '
             '{0.application_name}%(NORMAL)s\n'
             '{0.message}'.format(record))


def monitor(filename, handler=printout):
    """
    Start monitoring the given filename.
    """
    with open(filename, 'r') as csvfile:
        csvfile.seek(0, 2)
        reader = csv.reader(StreamIterator(csvfile), delimiter=",", quotechar='"')
        for row in reader:
            row = LogRecord(*row)
            handler(row)


if __name__ == '__main__':
    monitor(sys.argv[1])
