import redis
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from bmstu import settings
from .perm import *
from .serializers import UserSerializer

session_storage = redis.StrictRedis(host='127.0.0.1', port='6379')

# Удаление файла данных Redis:
# redis-cli flushall


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        },
    ),
    responses={
        200: openapi.Response(
            description='User registered successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                },
            ),
        ),
        400: 'Invalid input',
    },
)
@api_view(['POST'])
def register(request):
    """
    Регистрация с вводом логина и пароля
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'User registered successfully',
                'data': serializer.data
            })
        return JsonResponse(serializer.errors, status=400)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'jwt': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        400: "Bad Request: Invalid input data",
        401: "Unauthorized: Invalid username or password",

    }
)
@api_view(['POST'])
def login(request):
    """
    Авторизация с вводом логина и пароля
    """
    if request.method == 'POST':

        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = get_user_model()
        user = user.objects.filter(username=username).first()

        if user is None:
            return JsonResponse({'message': 'Пользователя не существует!'})

        if not user.check_password(password):
            return JsonResponse({'message': 'Пароль неверный!'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
        serializer = UserSerializer(user)
        response.data = {
            'message': 'Успешная авторизация!',
            'jwt': token,
            'user': serializer.data
        }
        return response


@api_view(['GET'])
def user(request):
    """
    Вывод информации об авторизованном пользователе
    """
    if request.method == 'GET':
        token = None
        username = None
        password = None
        token_head = request.headers.get('Authorization', None)
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            token = base64.b64decode(token)
            token = token.decode('utf-8')
            username, password = token.split(':')
            user = get_user_model()
            user = user.objects.filter(username=username).first()

            if user is None:
                return JsonResponse({'message': 'Пользователя не существует!'})

            if not user.check_password(password):
                return JsonResponse({'message': 'Пароль неверный!'})

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
            serializer = UserSerializer(user)
            response.data = {
                'message': 'Успешная авторизация!',
                'jwt': token,
                'user': serializer.data
            }
            return response


        else:
            token = request.COOKIES.get('jwt')
            print('token cookies', token)

        if not token:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        try:
            print(token)
            payload = jwt.decode(token[2:len(token) - 1], 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        user = get_user_model()

        user = user.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        return JsonResponse({'message': 'Аутентификация успешна',
                             'access_token': token,
                             'user': serializer.data
                             })



@api_view(['POST'])
@isAuth
def logout(request):
    """
    Выход из аккаунта
    """
    if request.method == 'POST':
        token_head = request.headers.get('Authorization', None)
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
        else:
            token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({'message': 'Токен не найден'})
        try:
            payload = jwt.decode(token[2:len(token) - 1], 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Токен недействителен'})

        user_id = payload.get('id')
        user_token = f"token:{user_id}:{token}"

        session_storage.set(user_token, user_id, ex=10000)

        response = Response()

        response.delete_cookie('jwt', domain='')
        # response.delete_cookie('jwt')
        response.data = {'message': 'Вы вышли из системы!'}

        return response