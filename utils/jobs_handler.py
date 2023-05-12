import json
import requests
import pickle
import os
from collections import OrderedDict

CACHE_DIR = os.path.join(os.getcwd(), 'cache')
CACHE_FILENAME = os.path.join(CACHE_DIR, 'jobs_cache.pickle')

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

CACHE_SIZE = 30  # maximum number of entries in the cache

def fetch_jobs():
    if os.path.exists(CACHE_FILENAME):
        with open(CACHE_FILENAME, 'rb') as f:
            cache = pickle.load(f)
    else:
        cache = OrderedDict()

    base_url = 'https://api.newvisionapp.com/v2/jobportal/Jobs'
    params = {
        'limit': '20'
    }

    # Check if articles are already in the cache
    cache_key = json.dumps(params, sort_keys=True)
    if cache_key in cache:
        return cache[cache_key]

    # Fetch articles from the API
    url = f'{base_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}'
    response = requests.get(url)
    jobs = response.json()

    # Filter featured jobs
    featured_jobs = [job for job in jobs if any(job_class.get('name') == 'Feature' for job_class in job.get('jobclass', []))]
    
    # Get unique categories
    categories = list(set(category['title'] \
        for job in jobs for category in job.get('categories', []))) 
    category_counts = {category: 0 for category in categories}
    for job in jobs:
        counted_categories = set()
        for category in job.get('categories', []):
            category_title = category['title']
            if category_title not in counted_categories:
                category_counts[category_title] += 1
                counted_categories.add(category_title)

    data = (jobs, featured_jobs, categories, category_counts)

    # Add data to the cache
    cache[cache_key] = data

    # Enforce cache size limit
    if len(cache) > CACHE_SIZE:
        cache.popitem(last=False)  # remove the least recently used item

    with open(CACHE_FILENAME, 'wb') as f:
        pickle.dump(cache, f)

    return data

def fetch_job_categories():
    url = f'https://api.newvisionapp.com/v2/jobportal/JobCategory?limit=20&order=asc'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def fetch_single_job(job_id):
    url = f'https://api.newvisionapp.com/v2/jobportal/Jobs/{job_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

