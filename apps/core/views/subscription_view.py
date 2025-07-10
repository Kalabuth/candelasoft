from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.core.models.suscription import Subscription
from apps.core.serializers.subscription_serializer import SubscriptionSerializer
from apps.common.external_services.jsonplaceholder import fetch_external_data
from apps.common.utils.email_utils import send_email_notification


class SubscriptionView(ModelViewSet):
    queryset = Subscription.objects.select_related("user").all()
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        subscriptions = self.get_queryset()
        enriched_data = []

        for sub in subscriptions:
            print("entra")
            external_data = fetch_external_data(sub.user.email)

            if external_data.get("status") == "inactive":
            
                send_email_notification(sub.user.email)

            serialized = SubscriptionSerializer(sub).data
            serialized["external_data"] = external_data
            enriched_data.append(serialized)

        return Response(enriched_data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        external_data = fetch_external_data(instance.user.email)

        if external_data.get("status") == "inactive":
            send_email_notification(instance.user.email)

        serialized = SubscriptionSerializer(instance).data
        serialized["external_data"] = external_data
        return Response(serialized, status=status.HTTP_200_OK)
