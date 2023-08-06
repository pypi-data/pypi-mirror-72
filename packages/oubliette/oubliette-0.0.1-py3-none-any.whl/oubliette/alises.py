from collections import OrderedDict

import oubliette


def lookup(query, default=None, table=None):
    if table:
        return alises.get(table, {}).get(query, default)
    for table_name, table in alises.items():
        if query in table:
            return table[query]
    return default


alises = OrderedDict([
    ("directions", oubliette.core.navigation.directions.alises),
])
