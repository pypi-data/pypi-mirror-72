# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2020 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at https://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at https://trac.edgewall.org/.

from trac.db import Table, Column, DatabaseManager

def do_upgrade(env, ver, cursor):
    """Add the cache table."""
    table = Table('cache', key='id')[
        Column('id'),
        Column('generation', type='int')
    ]
    db_connector, _ = DatabaseManager(env).get_connector()
    for stmt in db_connector.to_sql(table):
        cursor.execute(stmt)
