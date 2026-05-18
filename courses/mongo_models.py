from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class ActivityLog(Document):
    action = StringField(required=True)
    endpoint = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'activity_logs'
    }