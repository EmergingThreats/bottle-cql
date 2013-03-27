import bottle
from bottle import HTTPError
from bottle.ext import cql as bottle_cql
import cql

conn = conn = cql.connect('localhost',9160,'et', cql_version='3.0.0')

app = bottle.Bottle()
plugin = bottle_cql.Plugin(conn, keyword="cql")
app.install(plugin)


@app.get('/:query')
def show(query, cql):
    cursor = conn.cursor()
    cursor.execute(query)

    for row in cursor:
        do_stuff()

    cursor.close()

run(app=app, host='localhost', port=80, reloader=True)