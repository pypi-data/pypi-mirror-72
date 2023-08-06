# reed

Search for jobs using the Reed API in python.

This project was (heavily) inspired by the similar work on the Indeed API 
which can be found [here](https://github.com/indeedlabs/indeed-python).
Getting a publisher number from Indeed was a pain so I looked for similar
API's and stumbled upon Reed.

## API Credentials

To be able to interact with the Reed API you will need an API Key. This
key is passed into the reed client's constructor.

```python
from reed import ReedClient

client = ReedClient(api_key=YOUR_API_KEY)
```

You can sign up for an API key [here](https://www.reed.co.uk/developers/jobseeker).

## Performing a Job Search

```python
from reed import ReedClient

client = ReedClient(api_key)

params = {
    'keywords' : "data scientist",
    'locationName' : "London",
    'minimumSalary': 30000
}

response = client.search(**params)
```

## Retrieving job details

```python
from ReedClient import ReedClient

client = ReedClient(api_key)

result = client.job_details(job_id=job_id)
```


## API Parameters

### Job Search

**keywords** - 
This is the parameter for your search query. By default terms are ANDed.

**resultsToTake** -	
maximum number of results to return (the default is 100)

**employerId** - 
id of employer posting job

**employerProfileId** -	
profile id of employer posting job

**locationName** -	
the location of the job

**distanceFromLocation** -	
distance from location name in miles (default is 10)

**permanent** - 	
true/false

**contract** -	
true/false

**temp** - 	
true/false

**partTime** -  	
true/false

**fullTime** - 
true/false

**minimumSalary** -	
lowest possible salary e.g. 20000

**maximumSalary** -	
highest possible salary e.g. 30000

**postedByRecruitmentAgency** -
true/false

**postedByDirectEmployer** -
true/false

**graduate** -	
true/false