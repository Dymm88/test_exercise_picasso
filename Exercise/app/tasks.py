from celery import shared_task
from .models import File


@shared_task
def process_file(file_id):
    file = File.objects.get(pk=file_id)
    file.processed = True
    file.save()
