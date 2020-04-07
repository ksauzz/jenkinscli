import sys
from jenkinscli import server

def jobs(ctx, args, incomplete):
    return [(job['fullname']) for job in server().get_jobs(folder_depth=4) if job['fullname'].startswith(incomplete)]

def builds(ctx, args, incomplete):
    job_name = args[2]
    return [(build['number']) for build in server().get_job_info(job_name)['builds']]
