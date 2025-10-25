# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask-Supabase is a Flask extension that provides simple integration with Supabase. The extension follows standard Flask extension patterns with support for both direct initialization and factory pattern via `init_app()`.

## Architecture

**Single-Module Extension**
- All code is in `flask_supabase/__init__.py` (single file extension)
- The `Supabase` class manages Supabase client lifecycle using Flask's application context
- Client instances are stored in `g` (Flask's request-scoped storage) and auto-created on first access
- Configuration pulled from `app.config` or environment variables (`SUPABASE_URL`, `SUPABASE_KEY`)
- Supports optional `ClientOptions` for advanced Supabase client configuration

**Key Design Patterns**
- Flask extension pattern with `init_app()` for factory support
- Lazy client initialization via `@property` decorator on `.client`
- Request-scoped client instances (created per-request, torn down after request)
- Fails fast if required config (`SUPABASE_URL`, `SUPABASE_KEY`) is missing

## Development Commands

**Build Package**
```bash
python -m build
# Or with flit directly:
flit build
```

**Install Locally for Testing**
```bash
pip install -e .
```

**Publish to PyPI**
```bash
flit publish
```

## Configuration

The extension requires two config values:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key
- `SUPABASE_CLIENT_OPTIONS` (optional) - Dict or ClientOptions instance

These can be set via Flask config or environment variables.

## Usage Patterns

**Direct Initialization**
```python
from flask import Flask
from flask_supabase import Supabase

app = Flask(__name__)
app.config['SUPABASE_URL'] = 'your_url'
app.config['SUPABASE_KEY'] = 'your_key'
supabase = Supabase(app)
```

**Factory Pattern**
```python
supabase = Supabase()

def create_app():
    app = Flask(__name__)
    app.config['SUPABASE_URL'] = 'your_url'
    app.config['SUPABASE_KEY'] = 'your_key'
    supabase.init_app(app)
    return app
```

**Client Access**
```python
# Within request context:
supabase.client.from_('table').select('*').execute()
```
