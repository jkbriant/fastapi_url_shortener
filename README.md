# FastAPI URL Shortener

A simple, fast URL shortener built with FastAPI and Tailwind CSS. Features both a web interface and REST API for shortening and managing URLs.

## Features

- User-friendly forms to shorten URLs with one-click and copy to clipboard
- Full API support
- Simple in memory storage (resets on server restart)
- Clean UI with Tailwind CSS
- Error handling for JSON responses and web pages

## Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13+)
- **Frontend**: Jinja2 Templates + [Tailwind CSS](https://tailwindcss.com/)
- **Validation**: Pydantic
- **Package Manager**: [UV](https://github.com/astral-sh/uv)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi_urlshort
```

2. Install dependencies with UV:
```bash
uv sync
```

## Usage
```bash
uv run fastapi dev main.py
```

The application will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for detailed documentation.

## Project Structure

```
fastapi_urlshort/
├── main.py              # Main FastAPI application
├── schemas.py           # Pydantic models
├── pyproject.toml       # Project configuration
├── templates/           # Jinja2 HTML templates
│   ├── layout.html      # Base template
│   ├── home.html        # Main page with URL list
│   └── error.html       # Error page
└── static/              # Static assets (CSS, JS, icons)
```

## Todo
 - [ ] Change the storage of the addresses to use SQL
 - [ ] Cache frequently accessed web pages
 - [ ] Track the number of times a page has been accessed and the display statistics