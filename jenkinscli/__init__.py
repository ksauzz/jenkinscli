import jenkins

__server__ = None

def server():
    return __server__

def connect(url, user, password):
    global __server__
    __server__ = jenkins.Jenkins(url, user, password=password)

def main():
    from jenkinscli import cli
    cli.main()

