import click

def print_jobs(jobs):
    longest_name = max(jobs, key=lambda x: len(x['fullname']))['fullname']
    format = "{:>"+str(len(longest_name))+"}:  {}"

    click.echo(format.format('Name', 'Url'))
    for job in jobs:
        click.echo(format.format(job['fullname'], job['url']))

def print_job(job):
    click.echo("Name: {}".format(job['name']))
    if 'builds' in job:
        print_builds(job['builds'])

def print_builds(builds, limit=5):
    i = 0
    for build in builds:
        if i < limit:
            click.echo("Build: {}".format(build['number']))
            i += 1

def print_build(build):
    format = '{:15}: {}'
    click.echo(format.format('Number', build['number']))
    click.echo(format.format('Result', build['result']))
    for action in build['actions']:
        print_action(action)

def print_action(action):
    format = '{:15}: {}'
    if '_class' in action:
        if action['_class'] == 'hudson.model.CauseAction':
            shortDesc = list(map(lambda x: x['shortDescription'], action['causes']))[0]
            click.echo(format.format('Short Desc', shortDesc))

        elif action['_class'] == 'hudson.plugins.git.util.BuildData':
            for key in action['buildsByBranchName']:
                click.echo(format.format('Branch', key))

        elif action['_class'] == 'hudson.model.ParametersAction':
            first = True
            name = 'Parameters'
            for param in action['parameters']:
                click.echo(format.format(name, "{}={}".format(param['name'], param['value'])))
                if first:
                    first = False
                    name = ''

