import csv

def save_to_csv(jobs):
    with open('jobs.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'company', 'city', 'link'])
        for job in jobs:
            writer.writerow(list(job.values()))
    return