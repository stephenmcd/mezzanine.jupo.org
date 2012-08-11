
from fabric.api import cd, prefix, sudo, run, task
from fabric.contrib.files import exists
from mezzanine.project_template import fabfile as mezzfab


doc_repos = ("mezzanine", "cartridge")


@task
def install():
    mezzfab.install()
    with cd(mezzfab.env.venv_home):
        if not exists("docs"):
            run("virtualenv docs --distribute")
        with prefix("source %s/docs/bin/activate" % mezzfab.env.venv_home):
            sudo("pip install sphinx cartridge fabric")
        for repo in doc_repos:
            repo_path = "docs/%s" % repo
            if not exists(repo_path):
                with cd("docs"):
                    run("hg clone http://bitbucket.org/stephenmcd/" + repo)


@task
def create():
    mezzfab.create()
    manage("reset_demo")


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
