# 문화데이터 활용 경진대회를 위한 서버

## 개요
- 여행을 랜덤으로 추천해주는 어플리케이션, JustGo 서버입니다.

## 기술

- Node.js / Flask
- MongoDb
- AWS EC2

## Flask

### 사용 모듈
- mongoengine
- pymongo

## Node.js

### 사용 모듈
- Express
- mongoose

## URL

### 공통 응답

```
Response Description: 모든 응답에 result
StatusCode: *
{
    result: ‘success’/’failure’
}

Response Description: 서버오류
StatusCode: 500
{
   result: ‘failure’
}
```

### ~~[GET] api/docs~~ (Not Sure)

- ~~URL Description: Swagger API Docs~~
- ~~Request Body~~
```
none
```
- ~~Response Body~~
```
Response Desription: 성공
StatusCode: 200
{ Awesome-Swagger-UI }
```


### [POST] api/user/login

- URL Description: 페이스북 및 카카오 계정으로 로그인하기(웹 메인 페이지 통합)
- Request Body
```
userId(사용자 식별 가능한 고유번호)
```
- Response Body
```
Response Description: 로그인 성공
StatusCode : 200
{
    result: 'success'
    profileUrl: String
    reqComment: Array (아이템은 아래 참고)
    {
        tourName: String
        tourImage: String (Link)
    }
    recommendSpot: Array (아이템은 아래 참고)
    {
        reqTime: Number (분 단위)
        theme: String (자연,힐링,평화)
    }
    reqShare: Array (아이템은 아래 참고)
    {
        tourName: String
    }
}
```

### [PUT] api/user/:id/profile-image

- Description: 프로필 이미지 변경
- Request Body 
```
파일
```
- Response Body
```
Response Description: 변경 성공 
StatusCode : 205
{
    result: 'success'
    profileUrl: String (변경된 사진 URL)
}

Response Description: 지원하지 않는 파일일 경우
StatusCode: 405
{
    result: 'failure'
}

Response Description: 유저를 찾을 수 없음
StatusCode: 404
{
    result: 'failure'
}
```

### [PUT] api/user/:id/profile-name

- Description: 프로필 네임 변경
- Request Body 
```
name (바꿀 닉네임)
```
- Response Body
```
Response Description: 변경 성공
StatusCode : 205
{
    result: 'success'
    profileName: String (변경된 이름)
}

Response Description: 닉네임 중복
StatusCode: 405
{
    result: 'failure'
}

Response Description: 유저를 찾을 수 없음
StatusCode: 404
{
    result: 'failure'
}
```

### [POST] api/user/:id/tour-spot

- Description: 유저가 갔다온 장소 저장
- Request Body 
```
tourId (다녀온 관광지 ID)
```
- Response Body
```
Response Description: 저장 성공
StatusCode: 201
{
    result: 'success'
}

Response Description: 유저를 찾을 수 없음
StatusCode: 404
{
    result: 'failure'
}
```

### [POST] api/contact

- Description: 웹 메인 페이지의 건의사항
- Request Body 
```
userName
userEmail
userPhone
content
```
- Response Body
```
Response Description: 작성 성공
StatusCode : 201
{
    result: 'success'
}
```

### [GET] api/travel/tour-list

- Description: 조건에 맞는 관광지들 얻기
- Request Body 
```
transport : Number
    - 도보: 0
    - 대중교통: 1
    - 자동차: 2
lat : Number
lng : Number
theme : String (ex. 자연,힐링,!사랑,먹거리장터,특화거리)
minTime: Number (분 단위)
maxTime: Number (분 단위)
```
- Response Body
```
Response Description: 성공
StatusCode : 200
{
    result:'success'
    list: Array (아이템은 아래 참고)
    {
        reqtime : Number (소요시간, 분단위)
        rate: Number (평점)
        theme : String (ex. 자연,힐링,먹거리장터,특화거리)
        comment: String 
    }
}

Response Description: transport가 지정된 번호가 아닐 경우
StatusCode : 405
{
    result: 'failure'
}
```

### [GET] api/travel/direction

- Description: 경로 얻기 **(Request 및 Response 확정 x)**
- Request Body 
```

```
- Response Body
```
Response Description: 길찾기 성공
StatusCode : 200
{
    
}
```

### [GET] api/travel/:id/tour-info

- Description: 관광지 정보 얻기(API 활용)
- Request Body
```
none
```
- Response Body
```
Response Description: 정보 획득 성공
StatusCode: 200
{
    result: 'success'
    name: String
    address: String
    info: String
    image: String (Link)
    theme: String
    nearSpot: Array (아이템은 아래 참고)
    {
        id: String
        title: String
        image: String (Link)
        rate: Number
        address: String
        theme: String
    }
    nearRestaurant: Array (아이템은 아래 참고)
    {
        name: String
        address: String
        image: String (Link)
        rate: Number
    }
    comment: Array (아이템은 아래 참고)
    {
        profileImage: String (Link)
        profileName: String
        rate: Number
        content: String
        date: String or Date
    }
}

Response Description: 존재하지 않는 관광지
StatusCode: 404
{
    result: 'failure'
}
```

### [POST] api/travel/:id/tour-info

- Description: 관광지에 대한 후기 남기기
- Request Body
```
writerId: String
rate: Number
comment: String
```
- Response Body
```
Response Description: 작성 성공
StatusCode: 201
{
    result: 'success'
}

Response Description: 존재하지 않는 관광지
StatusCode: 404
{
    result: 'failure'
}
```

### ~~[POST] api/travel/:id/tour-info/:id~~ (Not Sure)

- ~~Description: 후기 신고하기~~
- ~~Request Body~~
```
none
```
- ~~Response Body~~
```
none
```

## DB

```
user
{
    userId: 고유한 식별번호 - 있는지
    profileName: 닉네임
    profileImage: 프로필 사진 URL
    wentSpot:
    [{
        tourId: 갔던 관광지 아이디
    }]
}
contact
{
    date: 문의한 날짜
    name: 이름
    email: 이메일
    phone: 전화번호
    content: 내용
}
tourspot
{
    tourId: 관광지아이디
    comment:
    [{
        userId: 유저아이디
        date: 작성일자
        rate: 별점
        content: 내용
    }]
}
```
