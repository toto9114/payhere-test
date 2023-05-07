from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate
from product.models import Category, Product
from product.views import ProductViewSets
from user_auth.models import UserProfile
from utils.pagination import DEFAULT_PAGE_SIZE
from utils.jamo import extract_chosung


# Create your tests here.
class ProductCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category(
            name='카테고리1'
        ).save()

        user = UserProfile(
            phone_number='01012341234',
            password='qwer1234'
        )
        user.save()

        cls.user = user
        cls.payload = {
            "category": "1",
            "price": 10000,
            "cost": 5000,
            "name": "테스트 상품",
            "content": "내용",
            "barcode": "1234567890123",
            "expire": "2023-05-07",
            "size": "small"
        }

    def test_product_create(self):
        view = ProductViewSets.as_view({'post': 'create', 'put': 'update', 'get': 'list', 'delete': 'destroy'})
        factory = APIRequestFactory()
        request = factory.post('/products/', self.payload, format='json')
        response = view(request)
        self.assertEqual(401, response.status_code)

        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(201, response.status_code)


class ProductUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category(
            name='카테고리1'
        )
        category.save()
        user = UserProfile(
            phone_number='01012341234',
            password='qwer1234'
        )
        user.save()

        product = Product(
            **{
                "category": category,
                "price": 10000,
                "cost": 5000,
                "name": "테스트 상품",
                "content": "내용",
                "barcode": "1234567890123",
                "expire": "2023-05-07",
                "size": "small"
            }
        )
        product.save()

        cls.user = user
        cls.payload = {
            "name": "슈크림 라떼",
            "price": 12000,
            "cost": 6000
        }
        cls.product_id = product.id

    def test_product_update(self):
        view = ProductViewSets.as_view({'post': 'create', 'put': 'update', 'get': 'list', 'delete': 'destroy'})
        factory = APIRequestFactory()

        request = factory.put(f'/products/{self.product_id}/', self.payload, format='json')
        response = view(request, pk=self.product_id)
        self.assertEqual(401, response.status_code)

        force_authenticate(request, user=self.user)
        response = view(request, pk=self.product_id)

        self.assertEqual(200, response.status_code)
        for k, v in self.payload.items():
            self.assertEqual(response.data[k], v)


class ProductRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category(
            name='카테고리1'
        )
        category.save()
        user = UserProfile(
            phone_number='01012341234',
            password='qwer1234'
        )
        user.save()

        name_list = ['슈크림 라떼', '아메리카노', '라떼', '콜드브루', '아인슈페너',
                     '카페모카', '그린티', '아포가토', '밀크티', '버블티',
                     '초코 프라페']

        bulk_instance = []
        for name in name_list:
            product = Product(
                **{
                    "category": category,
                    "price": 10000,
                    "cost": 5000,
                    "name": name,
                    "name_jamo": extract_chosung(name),
                    "content": "내용",
                    "barcode": "1234567890123",
                    "expire": "2023-05-07",
                    "size": "small"
                }
            )
            bulk_instance.append(product)
        Product.objects.bulk_create(bulk_instance)

        cls.user = user
        cls.total = len(name_list)

    def test_pagination(self):
        view = ProductViewSets.as_view({'post': 'create', 'put': 'update', 'get': 'list', 'delete': 'destroy'})
        factory = APIRequestFactory()

        request = factory.get(f'/products/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        data = response.data
        self.assertEqual(200, response.status_code)
        self.assertEqual(DEFAULT_PAGE_SIZE, len(data['results']))
        self.assertEqual(self.total, data['total'])
        self.assertIsNotNone(data['links']['next'])

    def test_search_query(self):
        view = ProductViewSets.as_view({'post': 'create', 'put': 'update', 'get': 'list', 'delete': 'destroy'})
        factory = APIRequestFactory()
        params = {'query': '라떼'}
        request = factory.get(f'/products/', params)
        force_authenticate(request, user=self.user)
        response = view(request)
        data = response.data
        self.assertEqual(2, data['total'])

        params = {'query': 'ㅍㄹㅍ'}
        request = factory.get(f'/products/', params)
        force_authenticate(request, user=self.user)
        response = view(request)
        data = response.data
        self.assertEqual(1, data['total'])


class ProductDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category(
            name='카테고리1'
        )
        category.save()
        user = UserProfile(
            phone_number='01012341234',
            password='qwer1234'
        )
        user.save()

        product = Product(
            **{
                "category": category,
                "price": 10000,
                "cost": 5000,
                "name": "테스트 상품",
                "content": "내용",
                "barcode": "1234567890123",
                "expire": "2023-05-07",
                "size": "small"
            }
        )
        product.save()

        cls.user = user
        cls.product_id = product.id

    def test_delete_product(self):
        view = ProductViewSets.as_view({'post': 'create', 'put': 'update', 'get': 'list', 'delete': 'destroy'})
        factory = APIRequestFactory()
        request = factory.delete(f'/products/{self.product_id}')
        response = view(request, pk=self.product_id)
        self.assertEqual(401, response.status_code)

        force_authenticate(request, user=self.user)
        response = view(request, pk=self.product_id)
        self.assertEqual(204, response.status_code)

        product = Product.objects.get(id=self.product_id)
        self.assertIsNotNone(product.deleted_at)