from flask import Flask, render_template, request, redirect, send_file
from parser_hh_ru import get_jobs
from exporter import save_to_csv

app = Flask('JobScrapper')

db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDb = db.get(keyword)
        if getDb:
            jobs = getDb
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
    else:
        return redirect('/')
    return render_template('report.html', job=keyword, results_number=len(jobs), jobs=jobs)

@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file("jobs.csv")
    except:
        return redirect('/')
app.run()