import click
import sys
import time
import logging

from jenkinscli import console
from jenkinscli import server
from jenkinscli.cli import choice

logger = logging.getLogger(__name__)


@click.group()
def build():
    """Build Commands"""
    pass


@build.command()
@click.argument('job_name', autocompletion=choice.jobs)
@click.argument('build_number', type=int, required=False, autocompletion=choice.builds)
def info(job_name, build_number):
    """Show Build Info"""
    if not build_number:
        build_number = get_latest_build_number(job_name)
    build = server().get_build_info(job_name, build_number)
    console.print_build(build)


@build.command()
@click.argument('job_name', autocompletion=choice.jobs)
@click.argument('build_number', type=int, required=False, autocompletion=choice.builds)
@click.option('-f', '--follow', is_flag=True)
def log(job_name, build_number, follow):
    """Get Log"""
    if not build_number:
        build_number = get_latest_build_number(job_name)
    if follow:
        _streaming_log(job_name, build_number)
    else:
        click.echo(server().get_build_console_output(job_name, build_number))


def _streaming_log(job_name, build_number):
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
@click.argument('job_name', autocompletion=choice.jobs)
@click.option('-p', '--params', metavar='PARAM', multiple=True, autocompletion=choice.params, help='build parameters. e.g. -p KEY1=VALUE1 -p KEY2=VALUE2 ')
@click.option('-f', '--follow', is_flag=True, help='follow console log after submitting a build')
@click.pass_context
def run(ctx, job_name, params, follow):
    """Start a build job"""
    parameters = {'dummy': ''}
    for p in params:
        p = p.split('=')
        parameters[p[0]] = p[1]
    last_build_number = get_latest_build_number(job_name)
    server().build_job(job_name, parameters=parameters)
    click.echo('submitted')
    if not follow:
        return

    click.echo('waiting for start of the job.', nl=False)
    while True:
        time.sleep(2)
        click.echo('.', nl=False)
        # note: it's possible next job is not the submitted one above.
        build_number = get_latest_build_number(job_name, no_message=True)
        if build_number > last_build_number:
            break

    ctx.invoke(log, job_name=job_name, build_number=build_number, follow=True)


@build.command()
@click.argument('job_name', autocompletion=choice.jobs)
@click.argument('build_number', type=int, required=False, autocompletion=choice.builds)
def stop(job_name, build_number):
    """Stop a build job"""
    if not build_number:
        build_number = get_latest_build_number(job_name)
    server().stop_build(job_name, build_number)


# TODO: refactor
def get_latest_build_number(job_name, no_message=False):
    if not no_message:
        click.echo('looking up the latest build number...\n')
    return server().get_job_info(job_name)['lastBuild']['number']
