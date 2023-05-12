from datetime import datetime
from flask import Flask, render_template, request
from markupsafe import Markup
from utils.utils import format_date, get_time_ago
from utils.jobs_handler import fetch_jobs, fetch_job_categories, fetch_single_job


app = Flask(__name__, static_url_path='/static')

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    data = fetch_jobs()    
    # Unpack the data into separate variables
    jobs, featured_jobs, categories, category_counts = data
    return render_template('index.html', \
        jobs=jobs, \
        featured_jobs=featured_jobs, \
        categories=categories, \
        category_counts=category_counts, \
        format_date=format_date)


@app.route('/jobs/job/<string:job_title>/<int:job_id>')
def job(job_title, job_id):
    job = fetch_single_job(job_id)
    details = Markup(job['details'])
    return render_template('jobs/job.html', \
        job=job, \
        details=details, \
        format_date=format_date, \
        get_time_ago=get_time_ago)

if __name__ == '__main__':
    app.run()
