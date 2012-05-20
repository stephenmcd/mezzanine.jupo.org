
from mezzanine.project_template.fabfile import *


_install = install
_deploy = deploy
_create = create

doc_repos = ("mezzanine", "cartridge")


def install():
    _install()
    with cd(env.venv_home):
        if not exists("docs"):
            run("virtualenv docs --distribute")
        with prefix("source %s/docs/bin/activate" % env.venv_home):
            sudo("pip install sphinx cartridge fabric")
        for repo in doc_repos:
            repo_path = "docs/%s" % repo
            if not exists(repo_path):
                with cd("docs"):
                    run("hg clone http://bitbucket.org/stephenmcd/" + repo)


def create():
    _create()
    manage("reset_demo")


def deploy():
    if not _deploy():
        return
    for repo in doc_repos:
        with cd("%s/docs/%s" % (env.venv_home, repo)):
            run("hg pull")
            run("hg up -C")
            with prefix("source %s/docs/bin/activate" % env.venv_home):
                run("sphinx-build docs docs/build")
