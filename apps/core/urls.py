from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views.subscription_view import SubscriptionView
from apps.core.views.user_register_view import UserRegisterView



router = DefaultRouter()
router.register(r'subscriptions', SubscriptionView, basename='subscriptions')

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('', include(router.urls)),
]