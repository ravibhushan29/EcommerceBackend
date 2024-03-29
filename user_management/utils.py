from rest_framework_jwt.settings import api_settings


def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def send_otp(phone_number, otp):
    """
        write logic for send otp
    """
    pass
