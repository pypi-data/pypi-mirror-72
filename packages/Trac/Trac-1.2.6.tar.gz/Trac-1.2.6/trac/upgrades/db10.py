# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2020 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at https://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at https://trac.edgewall.org/.

sql = [
#-- Make the node_change table contain more information, and force a resync
"""DROP TABLE revision;""",
"""DROP TABLE node_change;""",
"""CREATE TABLE revision (
    rev             text PRIMARY KEY,
    time            integer,
    author          text,
    message         text
);""",
"""CREATE TABLE node_change (
    rev             text,
    path            text,
    kind            char(1), -- 'D' for directory, 'F' for file
    change          char(1),
    base_path       text,
    base_rev        text,
    UNIQUE(rev, path, change)
);"""
]


def do_upgrade(env, ver, cursor):
    for s in sql:
        cursor.execute(s)
    print('Please perform a "resync" after this upgrade.')
