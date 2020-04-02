import click
import sys
import time
import logging

logger = logging.getLogger(__name__)

from jenkinscli import server
from jenkinscli import console

@click.group()
def build():
    pass

@build.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def info(job_name, build_number):
    if not build_number:
        build_number = get_latest_build_number(job_name)
    build = server().get_build_info(job_name, build_number)
    console.print_build(build)

@build.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def output(job_name, build_number):
    if not build_number:
        build_number = get_latest_build_number(job_name)
    click.echo(server().get_build_console_output(job_name, build_number))

@build.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def output_stream(job_name, build_number):
    if not build_number:
        build_number = get_latest_build_number(job_name)
    start = 0
    while True:
        res = server().get_build_progressive_console_output(job_name, build_number, start=start)
        if start != res['size']:
            click.echo(res['output'].strip())
        logger.debug('got console output: more={}, start={}, next_start={}'.format(res['more'], start, res['size']))
        time.sleep(2)
        if res['more']:
            start = res['size']
        else:
            break

@build.command()
@click.argument('job_name')
@click.option('-p', '--params', multiple=True)
def run(job_name, params):
    parameters = {'dummy': ''}
    for p in params:
        p = p.split('=')
        parameters[p[0]] = p[1]
    click.echo(server().build_job(job_name, parameters=parameters))

@build.command()
@click.argument('job_name')
@click.argument('build_number', type=int, required=False)
def stop(job_name, build_number):
    if not build_number:
        build_number = get_latest_build_number(job_name)
    server().stop_build(job_name, build_number)


# TODO: refactor
def get_latest_build_number(job_name):
        click.echo('looking up the latest build number...\n')
        return server().get_job_info(job_name)['lastBuild']['number']


