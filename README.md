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

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Authors](#authors)
- [License](#license)
- [Logo](#logo)

<a name = "about"></a>
## 🧐 About

Web-application with a collection of python developer interview questions.
You are not prepared!

<a name = "getting_started"></a>
## 🏁 Getting Started

### Prerequisites

1. python = "^3.13"
2. uv = "^0.5.31"
3. git = "^2.49.0"
4. docker desktop = "4.38.0" or compatible CLI version

### Install and run application locally in development mode

1. Install Python with your preferred method [Python official website](https://www.python.org/)

2. Install uv using [official guide](https://docs.astral.sh/uv/getting-started/installation/)

3. Install Docker using [official guide](https://docs.docker.com/get-docker/)

4. Install git using [official guide](https://git-scm.com/downloads)

5. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/python_dev_questionnaire
```

6. Provide all necessary environmental variables in .env file (see .env.example):

7. Install dependencies:
```
make install
```
8. Apply migrations:
```
make migrate
```
9. Collect static files:
```
make static
```
10. Start app locally in dev mode:
```
make dev
```

### Deploy application using Docker Compose

1. Install Docker on your server using [official guide](https://docs.docker.com/get-docker/)

2. Provide all necessary environmental variables in .env file (see .env.example):

3. Build docker image:
```
TARGET=production docker compose build
```

4. Start docker container:
```
TARGET=production docker compose up -d
```

<a name = "built_using"></a>
## ⛏️ Built Using

- [uv](https://docs.astral.sh/uv/) - an extremely fast Python package and project manager, written in Rust
- [Django](https://www.djangoproject.com/) - high-level Python web framework
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
- [django-bootstrap5](https://pypi.org/project/django-bootstrap5/) - CSS framework Bootstrap 5 for Django
- [WhiteNoise](https://whitenoise.readthedocs.io/en/latest/) - simplified static file serving for Python web apps
- [dj-database-url](https://pypi.org/project/dj-database-url/) - database URL configuration for Django
- [python-dotenv](https://pypi.org/project/python-dotenv/) - manage environment variables
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - PostgreSQL database adapter
- [django-extensions](https://pypi.org/project/django-extensions/) - useful extensions for Django
- [django-filter](https://pypi.org/project/django-filter/) - reusable Django application that allows users to filter querysets dynamically
- [rollbar](https://pypi.org/project/rollbar/) - real-time error monitoring and reporting tool
- [ruff](https://pypi.org/project/ruff/) - an extremely fast Python linter and code formatter, written in Rust
- [pytest](https://pypi.org/project/pytest/) - testing framework
- [pytest-cov](https://pypi.org/project/pytest-cov/) - code coverage measurement for Python
- [factory-boy](https://pypi.org/project/factory-boy/) - factory and fixture emulation for testing
- [coverage](https://pypi.org/project/coverage/) - code coverage measurement for Python
- [pre-commit](https://pre-commit.com/) - framework for managing and maintaining multi-language pre-commit hooks
- [django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/) - debugging tool for Django
- [Docker](https://www.docker.com/) - containerization tool


<a name = "authors"></a>
## ✍️ Authors

[@Pythonusus](https://github.com/Pythonusus)

<a name = "license"></a>
## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.


<a name = "logo"></a>
## Logo
Made with [Ideogram AI](https://ideogram.ai/)

Stored at [imgur.com](https://imgur.com/)
