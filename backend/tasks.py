from celery import Celery
import os
celery = Celery(__name__, broker=os.getenv('REDIS_URL','redis://redis:6379'))
@celery.task
def weekly_scan():
    print('Weekly scan')
