import jenkins


__server__ = None

def server():
    from jenkinscli import config
    global __server__
    if not __server__:
        __server__ = jenkins.Jenkins(config.url, config.user, password=config.password)
    return __server__

def main():
    from jenkinscli import cli
    cli.main()

