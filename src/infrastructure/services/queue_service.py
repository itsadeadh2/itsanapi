import boto3

class QueueService:
    def __init__(self, queue_url, sqs=None):
        self.sqs = sqs or boto3.client('sqs')
        self.queue_url = queue_url

    def add_to_queue(self, email):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=email
        )