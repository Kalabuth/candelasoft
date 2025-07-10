from django.db.models import ForeignKey, CASCADE, CharField, DateField
from django.contrib.auth.models import User

from apps.common.models.base_model import BaseModel

class Subscription(BaseModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name="subscriptions")
    start_date = DateField()
    end_date = DateField()

    def __str__(self):
        return self.user.username
