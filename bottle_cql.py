'''
This bottle-cql plugin allows for the passing of Cassandra Connection pools
around your application

The plugin inject an argument to all route callbacks that require a `db`
keyword.

Usage Example::

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

Copyright (c) 2013, David McNelis and Emerging Threats
License: MIT (see LICENSE for details)
'''

import inspect

import bottle
import cql

# PluginError is defined to bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError

class CQLPlugin(object):

    name = 'bottle_cql'
    api = 2

    def __init__(self, conn, 
                 keyword='cql', use_kwargs=False):
        '''
        :param conn: CQL Connection -- This should ultimately be pool of connections
        :param keyword: Keyword used to inject session database in a route

        '''
        self.conn = conn
        self.keyword = keyword
        self.use_kwargs = use_kwargs


    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument and check if metadata is available.'''
        for other in app.plugins:
            if not isinstance(other, CQLPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another SQLAlchemy plugin with "\
                                  "conflicting settings (non-unique keyword).")
            elif other.name == self.name:
                self.name += '_%s' % self.keyword

    def apply(self, callback, route):
        # hack to support bottle v0.9.x
        if bottle.__version__.startswith('0.9'):
            allconfig = route['config']
            _callback = route['callback']
        else:
            allconfig = route.config
            _callback = route.callback

        config = allconfig.get('cql', {})
        keyword = config.get('keyword', self.keyword)
        use_kwargs = config.get('use_kwargs', self.use_kwargs)

        argspec = inspect.getargspec(_callback)
        if not ((use_kwargs and argspec.keywords) or keyword in argspec.args):
            return callback

        def wrapper(*args, **kwargs):
            kwargs[keyword] = self.conn
            try:
                rv = callback(*args, **kwargs)

            except bottle.HTTPError:
                raise
            except bottle.HTTPResponse:
                raise
            return rv

        return wrapper


Plugin = CQLPlugin
