import nox


@nox.session
def tests(session):
    session.install(".")
    session.install("pytest")
    session.run("pytest", "tests")
