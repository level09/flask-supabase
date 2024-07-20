# Flask-Supabase Extension

The Flask-Supabase extension provides a simple and intuitive way to integrate Supabase into your Flask applications. With minimal setup, you can start leveraging the power of Supabase in your Flask projects, whether it's for database operations, authentication, or any other feature supported by Supabase.

## Features

- Easy integration of Supabase into Flask applications.
- Automatic management of Supabase API keys and URLs.
- Efficient handling of Supabase client instances throughout the application lifecycle.

## Installation

Install Flask-Supabase using pip:

```
pip install flask-supabase
```

## Quick Start

1. **Set up your Flask application**

First, ensure you have Flask installed. If not, you can install it using pip:

```
pip install Flask
```

Then, set up a basic Flask application:

```python
from flask import Flask
app = Flask(__name__)
```

2. **Configure the Flask-Supabase extension**

Import and initialize the `Supabase` extension, passing your Flask app object to it. Don't forget to set the `SUPABASE_URL` and `SUPABASE_KEY` in your app's configuration:

```python
from flask_supabase import Supabase

app.config['SUPABASE_URL'] = 'your_supabase_project_url'
app.config['SUPABASE_KEY'] = 'your_supabase_api_key'
supabase_extension = Supabase(app)
```

Alternatively, if you are using a factory function to create your Flask app, you can set up the Supabase extension like this:

```python
supabase_extension = Supabase()

def create_app():
    app = Flask(__name__)
    app.config['SUPABASE_URL'] = 'your_supabase_project_url'
    app.config['SUPABASE_KEY'] = 'your_supabase_api_key'
    supabase_extension.init_app(app)
    return app
```

3. **Use the Supabase client in your application**

Now, you can access the Supabase client in your route handlers using `supabase_extension.client`. Here's an example of how to perform a database operation with Supabase:

```python
@app.route('/users')
def get_users():
    response = supabase_extension.client.from_('users').select('*').execute()
    return response.data
```

## Documentation

For more information on Supabase and its capabilities, visit [Supabase documentation](https://supabase.io/docs).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Support

If you have any questions or encounter any issues, please open an issue on the project's GitHub page.

## Acknowledgements

This project is not officially associated with Supabase. All trademarks are the property of their respective owners.