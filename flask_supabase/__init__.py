from flask import current_app, g
from supabase import create_client, Client, ClientOptions
import os

class Supabase:
    def __init__(self, app=None, client_options=None):
        self.app = app
        self.client_options = client_options
        if app is not None:
            self.init_app(app, client_options)

    def init_app(self, app, client_options=None):
        app.config.setdefault('SUPABASE_URL', os.environ.get('SUPABASE_URL', ''))
        app.config.setdefault('SUPABASE_KEY', os.environ.get('SUPABASE_KEY', ''))
        app.config.setdefault('SUPABASE_CLIENT_OPTIONS', client_options)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        client = g.pop('supabase_client', None)
        if client is not None:
            # Perform any necessary cleanup for the Supabase client
            # Note: As of now, the Supabase Python client doesn't require explicit cleanup
            pass

    @property
    def client(self) -> Client:
        if 'supabase_client' not in g:
            url = current_app.config['SUPABASE_URL']
            key = current_app.config['SUPABASE_KEY']

            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set either in the Flask app config or environment variables")

            try:
                options = current_app.config.get('SUPABASE_CLIENT_OPTIONS')
                
                if options and not isinstance(options, ClientOptions):
                    options = ClientOptions(**options)

                g.supabase_client = create_client(url, key, options=options)
            except Exception as e:
                current_app.logger.error(f"Failed to create Supabase client: {str(e)}")
                raise
        return g.supabase_client

    def get_user(self):
        return self.client.auth.get_user()

    def sign_in_with_oauth(self, provider):
        return self.client.auth.sign_in_with_oauth({"provider": provider})

