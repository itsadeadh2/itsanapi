import boto3
from django.conf import settings


class QueueService:
    def __init__(self, queue_url=None, sqs=None):
        self.queue_url = queue_url or settings.QUEUE_URL
        self.sqs = sqs or boto3.client("sqs")

    def add_to_queue(self, email):
        self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=email)
