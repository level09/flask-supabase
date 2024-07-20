import supabase
from flask import current_app, g

class Supabase:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('SUPABASE_URL', '')
        app.config.setdefault('SUPABASE_KEY', '')
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        client = g.pop('supabase_client', None)
        if client is not None:
            # Perform any necessary cleanup for the Supabase client
            pass

    @property
    def client(self):
        if 'supabase_client' not in g:
            g.supabase_client = supabase.create_client(
                current_app.config['SUPABASE_URL'],
                current_app.config['SUPABASE_KEY']
            )
        return g.supabase_client