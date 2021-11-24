import bcrypt
import jwt
from datetime import datetime, timedelta

from .exceptions import (
    NoIncludeJWT,
    IncorrectJWT,
    ExpiredJWT
)


class HashService(object):
    @staticmethod
    def hash_string_to_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())\
            .decode('utf-8')

    @staticmethod
    def compare_pw_and_hash(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class JWTService(object):
    @staticmethod
    def run_auth_process(headers: dict,
                         token_type: str = 'access'):
        try:
            JWTService.check_header_include(headers, 'Authorization')
            pk = JWTService.decode_access_token_to_id(
                headers['Authorization'],
                token_type)
        except KeyError:
            raise NoIncludeJWT
        except jwt.exceptions.InvalidSignatureError:
            raise IncorrectJWT
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredJWT

        # if not UserService.check_pk_exists(pk):
        #     raise UserNotFound

        return pk

    @staticmethod
    def check_header_include(headers: dict, key: str) -> None:
        if (key not in headers) or (headers['Authorization'] == ''):
            raise KeyError

    @staticmethod
    def create_access_token_with_id(user_id: int,
                                    expired_minute: int = 10) -> str:
        return jwt.encode({
            'id': user_id,
            'exp': datetime.utcnow()+timedelta(minutes=expired_minute)
        }, 'JHHONG', algorithm='HS256', headers={
            'token': 'access'
        })

    @staticmethod
    def create_refresh_token_with_id(user_id: int,
                                     expired_days: int = 14):
        return jwt.encode({
            'id': user_id,
            'exp': datetime.utcnow()+timedelta(days=expired_days)
        }, 'JHHONG', algorithm='HS256', headers={
            'token': 'refresh'
        })

    @staticmethod
    def decode_access_token_to_id(access_token: str, token_type):
        if not token_type == jwt.get_unverified_header(access_token)['token']:
            raise jwt.exceptions.InvalidSignatureError
        return jwt.decode(access_token,
                          'JHHONG',
                          algorithms=['HS256'])['id']
