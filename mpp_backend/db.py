import sqlite3
import csv
import json
import click
from flask import current_app,g

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db

def close_db(e= None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # elements = json.load(open('mpp_backend/static/periodic-table.json','r'))
    with current_app.open_resource('static/periodic-table.json') as f:
        elements = json.load(f)
        cur  = db.cursor()
        try:
            cur.executemany(
                "INSERT INTO elements (name, category, atomic_number, appearance, discovered_by, named_by, phase, bohr_model_image, summary, symbol) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
                elements
            )
            db.commit()
        except Exception as e:
            click.echo(e)

    #   yeysyesyey   YESSS DOAMNE CAT AM STAT LA KKT UASTA TREBUIA DOAR SA ZIC CA CE FEL DE FISIER SA -L DESCHICA U R IN LOC DE RB SAU CVC BRHGBH4GHEGRE
    with current_app.open_resource('static/molecules.csv', 'r') as file:
        molecules = csv.reader(file)
        try:
            cur.executemany( "INSERT INTO molecules (formula, logp, primary_element_symbol, primary_element) VALUES (?,?,?,?)",  molecules)
            db.commit()
        except Exception as e:
            click.echo(e)
    cur.close()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Am initilaizat baza de date')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)