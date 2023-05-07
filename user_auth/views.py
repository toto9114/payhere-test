from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny

from user_auth.models import UserProfile
from middleware.response_middleware import CommonResponse
from utils import validator

import re


# Create your views here.
class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        if not validator.validate_phone_number(phone_number):
            return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                  message='휴대폰 번호를 확인해주세요.',
                                  data=None)

        if not validator.validate_password(password):
            return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                  message='비밀번호는 8자리 이상 영문과 숫자가 포함되어야 합니다.',
                                  data=None)

        phone_number = re.sub(r'\D', '', phone_number)

        UserProfile.objects.create_user(phone_number=phone_number, password=password)

        return Response(data={}, status=status.HTTP_201_CREATED)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        phone_number = re.sub(r'\D', '', phone_number)
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                  message='Phone_number does not exist',
                                  data=None)

        if not user.check_password(password):
            return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                  message='Incorrect password',
                                  data=None)

        refresh = RefreshToken.for_user(user)
        return CommonResponse(data={
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)


class RevokeTokenAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except TokenError as e:
                return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                      message=str(e),
                                      data=None)
        else:
            return CommonResponse(status=status.HTTP_400_BAD_REQUEST,
                                  message='refresh token field is empty',
                                  data=None)
