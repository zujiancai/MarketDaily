from backend import JobSettings, TEMP_DIR, CONN_STR_ENV_VAR
from batch_job.job_runner import JobRunner, JobSettingsFactory, JobData

import argparse
import os


# Step 4: Create the entrypoint for checking and executing the job
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute job by name.')
    parser.add_argument('jobName', help='Job friendly name, only data and digest are supported now.')
    args = parser.parse_args()
    job_name = str(args.jobName).lower()
    if job_name in JobSettings:
        # Step 5: instantiate a JobRunner object with job settings and job data configuration
        conn_str = os.environ.get(CONN_STR_ENV_VAR, 'UseDevelopmentStorage=true')
        job_data = JobData(conn_str, TEMP_DIR)
        # Don'f forget to create tables if it is the first time to run against the Azure storage account.
        job_data.create_if_not_exist()
        job_runner = JobRunner(JobSettingsFactory(JobSettings), job_data)
        print('Checking and running {0} job ...'.format(job_name))
        job_runner.run(job_name)
        print('Run completed.')
        print(' - success: ' + ', '.join(job_runner.run_success))
        print(' - error:   ' + ', '.join(job_runner.run_with_error))
        print(' - expired: ' + ', '.join(job_runner.set_expired))
        print(' - failed:  ' + ', '.join(job_runner.set_failed))
    else:
        print('ERROR: Job {0} is not supported.'.format(job_name))
