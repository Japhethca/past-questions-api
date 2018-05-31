from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def generate_token(data):
    payload = jwt_payload_handler(data)
    token = jwt_encode_handler(payload)
    return token


def decode_token(token):
    return jwt_decode_handler(token)
