
from mezzanine.project_template.fabfile import *


doc_repos = ("mezzanine", "cartridge")


def install_docs():
    with cd(env.venv_home):
        if not exists("docs"):
            run("virtualenv docs --distribute")
        with prefix("source %s/docs/bin/activate" % env.venv_home):
            sudo("pip install sphinx cartridge")
        for repo in doc_repos:
            repo_path = "docs/%s" % repo
            if not exists(repo_path):
                with cd("docs"):
                    run("hg clone http://bitbucket.org/stephenmcd/" + repo)

def install_all():
    install()
    install_docs()
    deploy_all()
    manage("createsuperuser")
    manage("reset_demo")

def deploy_docs():
    for repo in doc_repos:
        with cd("%s/docs/%s" % (env.venv_home, repo)):
            run("hg pull")
            run("hg up -C")
            with prefix("source %s/docs/bin/activate" % env.venv_home):
                run("sphinx-build docs docs/build")

def deploy_all():
    deploy()
    deploy_docs()
