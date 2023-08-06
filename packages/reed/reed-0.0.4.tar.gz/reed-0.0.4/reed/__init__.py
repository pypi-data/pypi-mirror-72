import requests
from requests.auth import HTTPBasicAuth

ROOT_URL = 'https://www.reed.co.uk/api/1.0/search?'
JOB_DETAILS_ROOT = 'https://www.reed.co.uk/api/1.0/jobs/'


class ReedClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def search(self, **args) -> list:
        '''
        Perform a job search with given arguments.
        '''
        return self.process_search_request(ROOT_URL, args)

    def process_search_request(self, url: str, args) -> list:
        '''
        Process job search request using requests library.
        '''
        auth = HTTPBasicAuth(username=self.api_key, password='')
        r = requests.get(url, auth=auth, params=args)

        if not r:
            r.raise_for_status()
        
        jobs = r.json()['results']
        total_results = r.json()['totalResults']

        if 'resultsToTake' in args.keys():

            if args['resultsToTake'] <= 100:
                return jobs

            else:
                results_to_take = args['resultsToTake']

        else:
            # return 100 jobs by default
            return jobs

        jobs_to_skip = 100
        remaining_jobs = results_to_take - jobs_to_skip

        while (len(jobs) < results_to_take) and (len(jobs) < total_results):
            args['resultsToSkip'] = jobs_to_skip
            args['resultsToTake'] = remaining_jobs
            r = requests.get(url, auth=auth, params=args)
            jobs.extend(r.json()['results'])
            jobs_to_skip += 100
            remaining_jobs = results_to_take - jobs_to_skip

        return jobs

    def job_details(self, job_id: int) -> dict:
        '''
        Retrieve details of the job with given id.
        '''

        if not type(job_id) is int:
            raise ValueError("'job_id' must be type 'int'")

        url = JOB_DETAILS_ROOT + str(job_id)
        return self.process_job_details_request(url)

    def process_job_details_request(self, url: str) -> dict:
        '''
        Process a job details request using requests library.
        '''
        auth = HTTPBasicAuth(username=self.api_key, password='')
        r = requests.get(url, auth=auth)

        if not r:
            r.raise_for_status()

        return r.json()
