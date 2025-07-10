from rest_framework.serializers import ModelSerializer
from apps.core.models.suscription import Subscription
from apps.core.serializers.user_serializer import UserSerializer
from apps.common.exceptions import InvalidSubscriptionDates


from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models.suscription import Subscription
from apps.core.serializers.user_serializer import UserSerializer
from apps.common.exceptions import InvalidSubscriptionDates


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_id', 'start_date', 'end_date']

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end <= start:
            raise InvalidSubscriptionDates()
        return data
