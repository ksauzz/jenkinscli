import click
import sys

from jenkinscli import server
from jenkinscli import console
from jenkinscli.cli import choice


@click.group()
def job():
    """Job Commands"""
    pass


@job.command()
@click.option('-d', '--depth', default=0, metavar='DEPTH')
@click.option('-p', '--prefix', default=None, metavar='PREFIX')
def list(depth, prefix):
    """List Jobs"""
    jobs = server().get_jobs(folder_depth=depth)
    if prefix:
        import builtins
        jobs = builtins.list(filter(lambda x: x['fullname'].startswith(prefix), jobs))
    if len(jobs) == 0:
        click.echo('job is not found')
        sys.exit(1)
    console.print_jobs(jobs)


@job.command()
@click.argument('job_name', autocompletion=choice.jobs)
def info(job_name):
    """Show Job Info"""
    job = server().get_job_info(job_name)

    if 'jobs' in job:
        for j in job['jobs']:
            console.print_job(j)
    else:
        console.print_job(job)
