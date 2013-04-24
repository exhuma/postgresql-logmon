Simple log monitor for PostgreSQL CSV logs.

This monitor takes into account that some queries might contain newlines, and
properly parses the records.


Usage::

    python pglog.py /path/to/csvlog.csv
