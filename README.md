# 문화데이터 활용 경진대회를 위한 서버
## 개요
- 각 서버별 역할을 분담하여 Node.js, Flask로 분업화
- 데이터베이스로는 MongoDB를 사용
- 두 서버를 호스팅하여 기능별로 구분하거나 Redirect를 이용할 것으로 예상됨

## Flask

### 파일 구성
    └ Flask
    
### 이번 개발을 진행할 때의 다짐
- 아직 개발 경험이 별로 없어 미숙한 점 양해 부탁드립니다.
- 틀린 부분이 있더라도 너그럽게 봐 주시면 정말 감사하겠습니다.
- 몰라서 못하는 게 아닌, 모르더라도 무엇이든 최선을 다해서 하는 자세를 갖추겠습니다.

## Node.js

### 파일 구성
- 추후 작성

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

### ~~GET api/docs~~ (Deprecated)

- URL Description: Swagger API Docs
- Request Body
```
none
```
- Response Body
```
Response Desription: 성공
StatusCode: 200
{ Awesome-Swagger-UI }
```


### POST api/user/login

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

### POST api/contact

- Description: 웹 메인 페이지의 건의사항
- Request Body 
```
userName
userEmail
userPhone
Content
```
- Response Body
```
Response Description: 
StatusCode : 201
{
    result: 'success'
}
```

### GET api/travel/tour-list

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

---------------------------


### GET api/travel/:id/tour-info

- Description: 관광지 정보 얻기(API 활용)
- Request Body
```
none
```
- 성공시
```
StatusCode : 200
{
    result: 'success'
}
```
- 실패시  
```
{
    result: 'failure'
}
```

### POST api/travel/:id/tour-info

- Description: 관광지에 대한 후기 남기기
- Request Body
```
rate: Number
comment: String
```
- 성공시
```
나중에 할래요
```
- 실패시
```
나중에 할래요
```


~~신고기능은 추후구현~~

### [GET] api/travel/direction

- Description: 경로 얻기
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
- 성공시
```
StatusCode : 200
{
    그 관광지의 위도 경도같이 보내줘야함
}
```
- 실패시  
```
{
    나중에
}
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
