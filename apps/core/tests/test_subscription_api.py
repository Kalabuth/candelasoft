from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.core.models.suscription import Subscription
from datetime import date, timedelta
from rest_framework import status
from unittest.mock import patch


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="juan",
            email="juan@example.com",
            password="123456"
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )

    def test_create_user(self):
        data = {
            "username": "nuevo",
            "email": "nuevo@example.com",
            "password": "clave123"
        }
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_create_subscription(self):
        data = {
            "user_id": self.user.id,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=30))
        }
        response = self.client.post("/subscriptions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["email"], "juan@example.com")

    @patch("apps.common.external_services.jsonplaceholder.requests.get")
    def test_list_subscriptions_includes_external_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": 1,
                "name": "Upendra",
                "email": "juan@example.com",
                "gender": "female",
                "status": "inactive"
            }
        ]

        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("external_data", response.json()[0])
        self.assertEqual(response.json()[0]["external_data"]["status"], "inactive")

    @patch("apps.common.external_services.jsonplaceholder.requests.get")
    def test_subscription_retrieve_includes_external_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": 1,
                "name": "Juan Ejemplo",
                "email": "juan@example.com",
                "gender": "male",
                "status": "active"
            }
        ]

        url = f"/subscriptions/{self.subscription.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("external_data", response.json())
        self.assertEqual(response.json()["external_data"]["plan"], "premium")

    @patch("apps.common.external_services.jsonplaceholder.requests.get")
    @patch("apps.core.views.subscription_view.send_email_notification")
    def test_email_sent_when_status_is_inactive(self, mock_send_email, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": 2,
                "name": "Usuario Inactivo",
                "email": "juan@example.com",
                "gender": "male",
                "status": "inactive"
            }
        ]

        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_email.assert_called_once_with("juan@example.com")
