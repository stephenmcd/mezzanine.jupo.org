
from fabric.api import env
env.proj_app = "project"

from fabric.api import cd, prefix, sudo, run, task
from fabric.contrib.files import exists
from mezzanine.project_template import fabfile as mezzfab


doc_repos = ("mezzanine", "cartridge")


@task
def install():
    mezzfab.install()
    if not exists(mezzfab.env.venv_home):
        run("mkdir -p %s" % mezzfab.env.venv_home)
    with cd(mezzfab.env.venv_home):
        if not exists("docs"):
            run("virtualenv docs --distribute")
        run("pip install sphinx")
        with prefix("source %s/docs/bin/activate" % mezzfab.env.venv_home):
            for repo in doc_repos:
                repo_path = "docs/%s" % repo
                if not exists(repo_path):
                    with cd("docs"):
                        run("hg clone http://bitbucket.org/stephenmcd/" + repo)
                        with cd(repo):
                            run("python setup.py develop")


@task
def create():
    mezzfab.create()
    mezzfab.manage("reset_demo")


@task
def deploy():
    if not mezzfab.deploy():
        return
    for repo in doc_repos:
        with cd("%s/docs/%s" % (mezzfab.env.venv_home, repo)):
            run("hg pull")
            run("hg up -C")
            with prefix("source %s/docs/bin/activate" % mezzfab.env.venv_home):
                run("sphinx-build docs docs/build")