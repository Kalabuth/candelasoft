from rest_framework.exceptions import APIException, ValidationError


class SubscriptionNotFound(APIException):
    status_code = 404
    default_detail = "Suscripción no encontrada."
    default_code = "subscription_not_found"


class ExternalAPIError(APIException):
    status_code = 502
    default_detail = "Error al comunicarse con la API externa."
    default_code = "external_api_error"


class UserAlreadyExists(ValidationError):
    default_detail = "El nombre de usuario o el e‑mail ya están registrados."
    default_code = "user_already_exists"


class InvalidSubscriptionDates(ValidationError):
    default_detail = "La fecha de fin debe ser posterior a la fecha de inicio."
    default_code = "invalid_subscription_dates"