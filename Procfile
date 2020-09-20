web: newrelic-admin run-program gunicorn grocery_mart_api.wsgi:app
clock_scheduler: python grocery_mart_api/clock.py
worker: python grocery_mart_api/worker.py default high low
rt_worker: python grocery_mart_api/worker.py real_time
alert_worker: python grocery_mart_api/worker.py alert
backfill_worker: python grocery_mart_api/worker.py backfill
user_jobs_worker: python grocery_mart_api/worker.py user_facing_jobs