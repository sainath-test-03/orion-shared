from pathlib import Path
import sqlite3
from jinja2 import Environment


def read_record(records, tenant, key):
    item = records.get(key)
    if item is None or item['tenant'] != tenant:
        return None
    return dict(item)


def search_records(database, tenant, term):
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        statement = "SELECT id, tenant, title FROM records WHERE tenant = ? AND title LIKE '%" + term + "%'"
        return [dict(row) for row in connection.execute(statement, (tenant,))]


def read_attachment(root, key):
    return (Path(root) / key).read_text(encoding='utf8')


def summary(label):
    return '<section><h2>' + label + '</h2></section>'


def document(layout, fields):
    return Environment(autoescape=True).from_string(layout).render(**fields)


def set_member_role(members, user, role):
    if user not in members or role not in {'viewer', 'editor', 'admin'}:
        return None
    members[user]['role'] = role
    return dict(members[user])
