"""Lint and test boardfarm_docsis on multiple python environments."""
import nox

_PYTHON_VERSIONS = ["3.9", "3.10"]
# Fail nox session when run a program which
# is not installed in its virtualenv
nox.options.error_on_external_run = True


def basic_install(session):
    session.install("--upgrade", "pip")
    session.install("--upgrade", "pip", "wheel")


@nox.session(python=_PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Lint boardfarm_docsis."""
    basic_install(session)
    session.install("--upgrade", "pip", "wheel", ".[dev]")
    session.run("black", ".", "--check")
    session.run("isort", ".", "--check-only")
    session.run("flake8", "boardfarm_docsis")


@nox.session(python=_PYTHON_VERSIONS)
def pylint(session: nox.Session) -> None:
    """Lint boardfarm_docsis using pylint without dev dependencies."""
    basic_install(session)
    # FIXME: boardfarm-lgi-shared is a circular dependency that shall not be there.
    session.install("--upgrade", "pip", "wheel", ".", "pylint", "boardfarm-lgi-shared")
    session.run("pylint", "boardfarm_docsis")


@nox.session(python=_PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Test boardfarm_docsis."""
    basic_install(session)
    # FIXME: ftfy is needed by boardfarm-lgi-shared, as such both should
    # be removed. boardfarm-lgi-shared is a hidden dependency.
    # Line should just be: "--upgrade", "pip", "wheel", ".[test]",
    session.install(
        "--upgrade", "pip", "wheel", ".[test]", "boardfarm-lgi-shared", "ftfy"
    )
    session.run("pytest", "unittests/", "integrationtests/")
