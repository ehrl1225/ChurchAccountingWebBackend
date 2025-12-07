from itsdangerous import URLSafeTimedSerializer
from common.env import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generate_verify_token(subject: str) -> str:
    # subject: 이메일 또는 user_id
    return serializer.dumps(subject, salt="email-verify")

def verify_token(token: str, max_age:int) -> str:
    # 변환: subject (예: 이메일)
    return serializer.loads(token, salt="email-verify", max_age=max_age)
