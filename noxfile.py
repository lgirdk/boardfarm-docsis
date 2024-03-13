"""Lint and test boardfarm-docsis on multiple python environments."""

import nox

_PYTHON_VERSIONS = ["3.11"]

# Fail nox session when run a program which
# is not installed in its virtualenv
nox.options.error_on_external_run = True


@nox.session(python=_PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Lint boardfarm-docsis."""
    session.install("--upgrade", "--pre", "boardfarm3")
    # if we install . with --pre then not just the pre-releases of boardfarm packages
    # are picked up
    session.install("--upgrade", ".[dev]")
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", "check", ".")
    session.run("flake8", ".")
    session.run("mypy", "boardfarm3_docsis")


@nox.session(python=_PYTHON_VERSIONS)
def pylint(session: nox.Session) -> None:
    """Lint boardfarm-docsis using pylint without dev dependencies."""
    session.install("--upgrade", "--pre", "boardfarm3")
    session.install("--upgrade", ".", "pylint")
    session.run("pylint", "boardfarm3_docsis")


# @nox.session(python=_PYTHON_VERSIONS)
# def test(session: nox.Session) -> None:
#     """Test boardfarm-docsis."""
