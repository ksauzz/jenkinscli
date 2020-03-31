import click
import jenkins
import sys
import os
import time

from jenkinscli import config
from jenkinscli import console
from jenkinscli import server

@click.group()
@click.option('--url')
@click.option('--user')
@click.option('--password')
@click.option('-k', '--insecure', is_flag=True)
def main(**kwargs):
    config.init(**kwargs)
    if config.insecure:
        # this is defined in jenkins
        os.environ['PYTHONHTTPSVERIFY'] = '0'

    global server
    server = jenkins.Jenkins(config.url, username=config.user, password=config.password)

@main.command()
@click.option('-d','--depth', default=0)
@click.option('-p','--prefix', default=None)
def jobs(depth, prefix):
    jobs = server.get_jobs(folder_depth=depth)
    if prefix:
        jobs = list(filter(lambda x: x['fullname'].startswith(prefix) ,jobs))
    if len(jobs) == 0:
        click.echo('job is not found')
        sys.exit(1)
    console.print_jobs(jobs)

@main.command()
@click.argument('job_name')
def job(job_name):
    job = server.get_job_info(job_name)

    if 'jobs' in job:
        for j in job['jobs']:
            console.print_job(j)
    else:
        console.print_job(job)

@main.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def build_info(job_name, build_number):
    if not build_number:
        build_number = server.get_job_info(job_name)['lastBuild']['number']
    build = server.get_build_info(job_name, build_number)
    console.print_build(build)

@main.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def build_output(job_name, build_number):
    if not build_number:
        build_number = server.get_job_info(job_name)['lastBuild']['number']
    click.echo(server.get_build_console_output(job_name, build_number))

@main.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def build_output_stream(job_name, build_number):
    if not build_number:
        build_number = server.get_job_info(job_name)['lastBuild']['number']
    start = 0
    while True:
        res = server.get_build_progressive_console_output(job_name, build_number, start=start)
        click.echo(res['output'].strip())
        time.sleep(2)
        if not res['more']:
            break
        else:
            start = start + res['size']

@main.command()
@click.argument('job_name')
@click.option('-p', '--params', multiple=True)
def build(job_name, params):
    parameters = {'dummy': ''}
    for p in params:
        p = p.split('=')
        parameters[p[0]] = p[1]
    click.echo(server.build_job(job_name, parameters=parameters))

@main.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def build_stop(job_name, build_number):
    if not build_number:
        build_number = server.get_job_info(job_name)['lastBuild']['number']
    server.stop_build(job_name, build_number)
