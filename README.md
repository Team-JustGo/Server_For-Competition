# 문화데이터 활용 경진대회를 위한 서버
## 개요
- 각 서버별 역할을 분담하여 Node.js, Flask로 분업화
- 데이터베이스로는 MongoDB를 사용
- 두 서버를 호스팅하여 기능별로 구분하거나 Redirect를 이용할 것으로 예상됨

## Flask

### 파일 구성
    └ static
    └ templates
    └ __init__.py
    
### 이번 개발을 진행할 때의 다짐
- 아직 개발 경험이 별로 없어 미숙한 점 양해 부탁드립니다.
- 틀린 부분이 있더라도 너그럽게 봐 주시면 정말 감사하겠습니다.
- 몰라서 못하는 게 아닌, 모르더라도 무엇이든 최선을 다해서 하는 자세를 갖추겠습니다.

## Node.js

### 파일 구성
- 추후 작성

## URL

### GET api/docs

- Description: Swagger API Docs
- Request Body


### POST api/user/login

- Description: 페이스북 및 카카오 계정으로 로그인하기(웹 메인 페이지 통합)
- Request Body
```
userId(사용자 식별 가능한 고유번호)
```
- 성공시
```
StatusCode : 200
{
    profileUrl: String
    메인애티비티에 들어갈 것들
    추후작성
    
}
```
- 실패시  
```
{
    추후작성
}
```

### POST api/contact

- Description: 웹 메인 페이지의 건의사항
- Request Body 
```
userId
```
- 성공시
```
StatusCode : 200
{
    profileUrl: String
    
}
```
- 실패시  
```
{

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

### GET api/travel/tour-info

- Description: 관광지 정보 얻기(API 활용)
- Request Body 
```

```
- 성공시
```
StatusCode : 200
{
    추후 작성
}
```
- 실패시  
```
{
    나중에
}
```

### POST api/travel/tour-info/:id

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

### [POST] api/user/tour-spot

- Description: 유저가 갔다온 장소 저장
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

### [PUT] api/user/profile-image/:id

- Description: 프로필 이미지 변경
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

### [PUT] api/user/profile-name/:id

- Description: 프로필 네임 변경
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
