# 페이히어 사전과제

### 환경세팅

1. `.env` 파일 수정 (편의상 정보 공개)
2. DB정보 입력

### 서버 구동

Docker 환경

```
./script/docker.build.sh
./script/docker.run.sh 
```

### 프로젝트 구성

1. product: 상품관련 API
2. user_auth: 로그인, 로그아웃, 회원가입 유저 관련
3. utils: 유틸모듈 모음
4. middleware: custom response 관련 middleware


### API
BASE_URL : `localhost:8000`

- `/auth/signup/` : 회원가입
```
curl --location 'localhost:8000/auth/signup' \
--header 'Content-Type: application/json' \
--data '{
    "phone_number": "010-1234-1234",
    "password": "qwer1234"
}'
```
- `/auth/token/` : 로그인
```
curl --location 'localhost:8000/auth/token' \
--header 'Content-Type: application/json' \
--data '{
    "phone_number": "010-1234-1234",
    "password": "qwer1234"
}'
```
- `/auth/revoke_token/` : 로그아웃
```
curl --location 'localhost:8000/auth/revoke_token' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk' \
--header 'Content-Type: application/json' \
--data '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzM4OTAzMiwiaWF0IjoxNjgzMzg1NDMyLCJqdGkiOiIwODkyOWE3Y2MwNzM0ODYxOTZlMjNiM2Y4MDkzYWUwOCIsInVzZXJfaWQiOjF9.8beW-S7jkP7XRRPFbVoO0-gc2P9ZR64qvvcm4pDi2iU"
}'
```
- `/products/` : 상품 입력, 상품 리스트

```
POST

curl --location 'localhost:8000/products/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk' \
--header 'Content-Type: application/json' \
--data '{
    "category": "1",
    "price": 10000,
    "cost": 5000,
    "name": "테스트 상품",
    "content": "내용",
    "barcode": "1234567890123",
    "expire": "2023-05-07",
    "size": "small"
}'
```


```
GET 

curl --location 'localhost:8000/products?query=%EB%9D%BC%EB%96%BC&page=1' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk'
```

- /products/<int:pk> : 상품 정보, 상품 정보 업데이트, 상품 삭제

```
GET

curl --location 'localhost:8000/products/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk'
```

```
PUT

curl --location --request PUT 'localhost:8000/products/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk' \
--header 'Content-Type: application/json' \
--data '{
    // "category": "1",
    "price": 10000,
    "cost": 6000,
    "name": "거북알",
    // "content": "contentcontent",
    // "barcode": "1234567890123",
    "expire": "2023-06-26",
    "size": "small"
}'
```
```
DELETE

curl --location --request DELETE 'localhost:8000/products/3/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzk0ODU2LCJpYXQiOjE2ODMzOTEyNTYsImp0aSI6ImY0MDRlZGQ3ZmI1MjQzNTVhOTAzMTQwNGQ1NDY5OTgxIiwidXNlcl9pZCI6MX0.3QzEFYBz1yL-P06tEJlXW3DHFGVZRO_IFN8DPokRNqk'
```
