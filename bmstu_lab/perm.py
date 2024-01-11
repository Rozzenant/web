import base64
from functools import wraps
import datetime
from rest_framework.response import Response
from .serializers import UserSerializer

import jwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied


def isAuth(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        token_head = request.headers.get('Authorization')
        auth = False
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            auth = True
            print('token', token)
        else:
            token = request.COOKIES.get('jwt')
            print('token cok', token)

        if not token and request.headers.get('jwt', None) is None:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        if auth:

            token = base64.b64decode(token).decode('utf-8')
            username, password = token.split(':')
            user = get_user_model()
            user = user.objects.filter(username=username).first()

            if user is None:
                return JsonResponse({'message': 'Пользователя не существует!'})

            if not user.check_password(password):
                return JsonResponse({'message': 'Пароль неверный!'})

            user_id = user.id

        else:
            if request.headers.get('jwt', None) is not None:
                token = request.headers.get('jwt')
                token = '  ' + token + ' '
            try:
                payload = jwt.decode(token[2:len(token) - 1], 'secret', algorithms='HS256')
                user_id = payload['id']
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Аутентификация не пройдена!')

        # Проверка успешной аутентификации
        user = get_user_model()
        user = user.objects.filter(id=user_id).first()
        if not user:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        return view_func(request, *args, **kwargs)

    return wrap


def isModerator(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        token_head = request.headers.get('Authorization')
        auth = False
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            auth = True
            print('token', token)
        else:
            token = request.COOKIES.get('jwt')
            print('token cok', token)

        if not token and request.headers.get('jwt', None) is None:
            raise PermissionDenied('Доступ запрещен: Токен отсутствует.')

        if auth:

            token = base64.b64decode(token).decode('utf-8')
            username, password = token.split(':')
            user = get_user_model()
            user = user.objects.filter(username=username).first()

            if user is None:
                return JsonResponse({'message': 'Пользователя не существует!'})

            if not user.check_password(password):
                return JsonResponse({'message': 'Пароль неверный!'})

            user_id = user.id

        else:
            if request.headers.get('jwt', None) is not None:
                token = request.headers.get('jwt')
                token = '  ' + token + ' '
            try:
                payload = jwt.decode(token[2:len(token) - 1], 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise PermissionDenied('Доступ запрещен: требуется авторизация.')
            except jwt.InvalidTokenError:
                raise PermissionDenied('Доступ запрещен: Недействительный токен.')

            user_id = payload.get('id')

        if not user_id:
            raise PermissionDenied('Доступ запрещен: Неверные данные в токене.')

        user = get_user_model()
        user = user.objects.filter(id=user_id, Is_Super=True).first()
        if not user:
            raise PermissionDenied('Доступ запрещен: Недостаточно прав для выполнения операции.')

        return view_func(request, *args, **kwargs)

    return wrap
