from fabric.api import env, run, local, cd, prompt
#from fabric.contrib.console import confirm
#from fabric.contrib.project import upload_project
#from fabric.contrib.files import exists, comment, uncomment
#from fabric.decorators import runs_once

def p():
    env.username = 'rlunch'
    env.hosts = ['%s@%s.webfactional.com:22' % (env.username,env.username),]
    env.branch = 'master'
    env.appname = 'brosandbooks'
    env.base_dir = '/home/%s/webapps/%s/' % (env.username,env.appname)
    env.proj_dir = env.base_dir + 'myproject/'
  
def deploy():
    print env.hosts
    # Push from local
    if env.branch:
        local('git push origin HEAD:%s' % env.branch)
    # Get from git
    with cd(env.proj_dir):
        run('git fetch origin')
        p = run('git diff --stat origin/master -- requirements.txt').strip()
        need_bootstrap = not bool(p)
        run('git reset --hard origin/%s' % env.branch)
        if need_bootstrap:
            run('pip install -r requirements.txt')
        need_migration = "( )" in run('source ../bin/activate; ./manage.py migrate --list')
        if need_migration:
            if "y" != prompt("Shall I run the migrations automatically? (y/N):"):
                raise StandardError("Run the migrations before deploying")
            run('source ../bin/activate; ./manage.py migrate')
    restart()
            
def restart():
    with cd(env.base_dir):
        run('./apache2/bin/restart')
        
def getdb():
    pass