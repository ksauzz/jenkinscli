import sys
from jenkinscli import server


def jobs(ctx, args, incomplete):
    return [(job['fullname']) for job in server().get_jobs(folder_depth=4) if job['fullname'].startswith(incomplete)]


def builds(ctx, args, incomplete):
    job_name = args[2]
    return [(build['number']) for build in server().get_job_info(job_name)['builds']]


def params(ctx, args, incomplete):
    job_name = args[2]
    job = server().get_job_info(job_name)
    params = []
    for prop in job["property"]:
        if prop['_class'] == 'hudson.model.ParametersDefinitionProperty':
            for param in prop['parameterDefinitions']:
                params = params + [("{}={}".format(param['defaultParameterValue']['name'],
                                                   param['defaultParameterValue']['value']), param['description'])]

    return params
