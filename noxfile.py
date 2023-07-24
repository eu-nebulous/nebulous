import nox

nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True

YAML_PATHS = [
    "./zuul.d/",
]

PYTHON_PATHS = [
    "./noxfile.py",
]


@nox.session
def black(session):
    session.install("black")
    session.run("black", *PYTHON_PATHS)


@nox.session
def isort(session):
    session.install("isort")
    session.run("isort", "--profile=black", *PYTHON_PATHS)


@nox.session
def linters(session):
    session.install("yamllint")
    session.install("black")
    session.install("isort")
    session.install("flake8")
    session.run("yamllint", *YAML_PATHS)
    session.run("black", "--check", *PYTHON_PATHS)
    session.run("isort", "--profile=black", "--check", *PYTHON_PATHS)
    session.run("flake8", *PYTHON_PATHS)
