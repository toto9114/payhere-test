from rest_framework.test import APITestCase, APIRequestFactory
from .views import SignUpAPIView, TokenAPIView, RevokeTokenAPIView
from user_auth.models import UserProfile


# Create your tests here.
class SignUpTestCase(APITestCase):
    def test_signup(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/auth/signup/', {
            "phone_number": "010-1234-1234",
            "password": "qwer1234",
        }, format='json')
        response = view(request)
        self.assertEqual(201, response.status_code)

    def test_phone_number_validation_1(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/auth/signup/', {
            "phone_number": "01012341234",
            "password": "qwer1234",
        }, format='json')
        response = view(request)
        self.assertEqual(201, response.status_code)

    def test_phone_number_validation_2(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/auth/signup/', {
            "phone_number": "12341234",
            "password": "qwer1234",
        }, format='json')
        response = view(request)
        self.assertEqual(400, response.status_code)

    def test_phone_number_validation_3(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/auth/signup/', {
            "phone_number": "010-1234-12345",
            "password": "qwer1234",
        }, format='json')
        response = view(request)
        self.assertEqual(400, response.status_code)

    def test_password_validation_1(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        #
        request = factory.post('/auth/signup/', {
            "phone_number": "01012341234",
            "password": "12345678",
        }, format='json')
        response = view(request)
        self.assertEqual(400, response.status_code)

    def test_password_validation_2(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        #
        request = factory.post('/auth/signup/', {
            "phone_number": "01012341234",
            "password": "qwerqwer",
        }, format='json')
        response = view(request)
        self.assertEqual(400, response.status_code)

    def test_password_validation_3(self):
        view = SignUpAPIView.as_view()
        factory = APIRequestFactory()
        #
        request = factory.post('/auth/signup/', {
            "phone_number": "01012341234",
            "password": "qwe123",
        }, format='json')
        response = view(request)
        self.assertEqual(400, response.status_code)


class TokenTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        UserProfile.objects.create_user(phone_number='01012341234', password='qwer1234')

    def test_token(self):
        token_view = TokenAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/auth/token/', {
            "phone_number": "01012341234",
            "password": "qwer1234"
        }, format='json')
        response = token_view(request)
        self.assertEqual(200, response.status_code)
        data = response.data
        fields = data.keys()
        self.assertIn('access_token', fields)
        self.assertIn('refresh_token', fields)

        # Revoke token
        revoke_token_view = RevokeTokenAPIView.as_view()
        request = factory.post('/auth/revoke_token/', {
            "refresh_token": data['refresh_token']
        }, HTTP_AUTHORIZATION=f"Bearer {data['access_token']}", format='json')
        response = revoke_token_view(request)
        self.assertEqual(204, response.status_code)
