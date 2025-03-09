<div align="center">

<img src="https://imgur.com/CvlDqSD.png" alt="Questionary logo" width="400" height="400">

# Python developer questionnaire

### Maintainability, tests and test coverage status:
[![Actions Status](https://github.com/Pythonusus/python_dev_questionnaire/actions/workflows/github-ci.yaml/badge.svg)](https://github.com/Pythonusus/python_dev_questionnaire/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c44a824fa624cba3989d/maintainability)](https://codeclimate.com/github/Pythonusus/python_dev_questionnaire/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c44a824fa624cba3989d/test_coverage)](https://codeclimate.com/github/Pythonusus/python_dev_questionnaire/test_coverage)

</div>

## 🔗 Link to web-service
[Try Python developer questionnaire by this link](https://python-dev-questionnaire.onrender.com)

## 📝 Table of Contents

- <a href="#about">About</a>
- <a href="#getting-started">Getting Started</a>
- <a href="#built-using">Built Using</a>
- <a href="#authors">Authors</a>
- <a href="#license">License</a>
- <a href="#logo">Logo</a>

<a id="about"></a>
## 🧐 About

Web-application with a collection of python developer interview questions.
You are not prepared!

<a id="getting-started"></a>
## 🏁 Getting Started

### Prerequisites

1. python = "^3.13"
2. uv = "^0.5.31"
3. git = "^2.49.0"
4. docker desktop = "4.38.0" or compatible CLI version

### Run application locally in development mode with Docker Compose

1. Install Python with your preferred method [Python official website](https://www.python.org/)

2. Install uv using [official guide](https://docs.astral.sh/uv/getting-started/installation/)

3. Install Docker using [official guide](https://docs.docker.com/get-docker/)

4. Install git using [official guide](https://git-scm.com/downloads)

5. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/python_dev_questionnaire
```
6. Provide all necessary environment variables in .env file (see .env.example):
7. Install dependencies in virtual environment using uv:
```
make install
```
8. Install pre-commit hooks:
```
make pre-commit
```
9. Collect static files:
```
make static
```
10. Build Docker Image:
```
make docker-build-dev
```
11. Run Docker Container:
```
make docker-start-dev
```
12. Make your changes to the project.
The code will be automatically reloaded because Docker Compose uses volumes for development.
However, if you make changes to models, you need to run ```make docker-migrate``` to apply migrations to the database.
You also need to run ```make docker-install``` if you modify project dependencies. Virtual environment is not shared
between host and container.

<a id="built-using"></a>
## ⛏️ Built Using

- [uv](https://docs.astral.sh/uv/) - an extremely fast Python package and project manager, written in Rust
- [django](https://www.djangoproject.com/) - high-level Python web framework
- [gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
- [django-bootstrap5](https://pypi.org/project/django-bootstrap5/) - CSS framework Bootstrap 5 for Django
- [whitenoise](https://whitenoise.readthedocs.io/en/latest/) - simplified static file serving for Python web apps
- [dj-database-url](https://pypi.org/project/dj-database-url/) - database URL configuration for Django
- [python-dotenv](https://pypi.org/project/python-dotenv/) - manage environment variables
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - PostgreSQL database adapter
- [django-extensions](https://pypi.org/project/django-extensions/) - useful extensions for Django
- [django-filter](https://pypi.org/project/django-filter/) - reusable Django application that allows users to filter querysets dynamically
- [ruff](https://pypi.org/project/ruff/) - an extremely fast Python linter and code formatter, written in Rust
- [pytest](https://pypi.org/project/pytest/) - testing framework
- [pytest-cov](https://pypi.org/project/pytest-cov/) - code coverage measurement for Python
- [pytest-django](https://pypi.org/project/pytest-django/) - pytest plugin for testing Django applications
- [factory-boy](https://pypi.org/project/factory-boy/) - factory and fixture emulation for testing
- [coverage](https://pypi.org/project/coverage/) - code coverage measurement for Python
- [pre-commit](https://pre-commit.com/) - framework for managing and maintaining multi-language pre-commit hooks
- [django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/) - debugging tool for Django
- [djlint](https://pypi.org/project/djlint/) - Django template linter and formatter
- [django-browser-reload](https://pypi.org/project/django-browser-reload/) - browser reload for Django
- [docker](https://www.docker.com/) - containerization tool

<a id="authors"></a>
## ✍️ Authors

[@Pythonusus](https://github.com/Pythonusus)

<a id="license"></a>
## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

<a id="logo"></a>
## Logo
Made with [Ideogram AI](https://ideogram.ai/)

Stored at [imgur.com](https://imgur.com/)
