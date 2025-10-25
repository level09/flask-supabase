import os

from flask import current_app, g
from supabase import Client, ClientOptions, create_client


class Supabase:
    """Flask extension for Supabase integration.

    Provides simple integration with Supabase, following standard Flask extension patterns.
    Supports both direct initialization and factory pattern via init_app().
    """

    def __init__(self, app=None, client_options=None):
        """Initialize the Supabase extension.

        Args:
            app: Flask application instance (optional for factory pattern).
            client_options: Supabase ClientOptions instance or dict (optional).
        """
        self.app = app
        self.client_options = client_options
        if app is not None:
            self.init_app(app, client_options)

    def init_app(self, app, client_options=None):
        """Initialize the extension with a Flask application.

        Args:
            app: Flask application instance.
            client_options: Supabase ClientOptions instance or dict (optional).
        """
        app.config.setdefault("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
        app.config.setdefault("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
        app.config.setdefault("SUPABASE_CLIENT_OPTIONS", client_options)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        client = g.pop("supabase_client", None)
        if client is not None:
            # Perform any necessary cleanup for the Supabase client
            # Note: As of now, the Supabase Python client doesn't require explicit cleanup
            pass

    @property
    def client(self) -> Client:
        """Get the Supabase client instance.

        Creates and caches a client instance per request context.
        The client is automatically torn down after the request.

        Returns:
            Supabase Client instance.

        Raises:
            ValueError: If SUPABASE_URL or SUPABASE_KEY are not configured.
        """
        if "supabase_client" not in g:
            url = current_app.config["SUPABASE_URL"]
            key = current_app.config["SUPABASE_KEY"]

            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_KEY must be set either in the Flask app config or environment variables"
                )

            try:
                options = current_app.config.get("SUPABASE_CLIENT_OPTIONS")

                if options and not isinstance(options, ClientOptions):
                    options = ClientOptions(**options)

                g.supabase_client = create_client(url, key, options=options)
            except Exception as e:
                current_app.logger.error(f"Failed to create Supabase client: {str(e)}")
                raise
        return g.supabase_client

    def get_user(self, jwt=None):
        """Get the authenticated user.

        Args:
            jwt: Optional JWT token to validate. If None, uses the current session.

        Returns:
            User object from Supabase auth.
        """
        return self.client.auth.get_user(jwt)

    def sign_in_with_oauth(self, provider):
        """Sign in with an OAuth provider.

        Args:
            provider: OAuth provider name (e.g., 'google', 'github').

        Returns:
            OAuth response from Supabase auth.
        """
        return self.client.auth.sign_in_with_oauth({"provider": provider})
