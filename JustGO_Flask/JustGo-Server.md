저스트-고 서버 부문 협업 관련 내용 정리
--------------------------------
김원준, 김재훈(마지막 수정 시각 7/24 19:20)
# URL 관련

## Needed URL

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

~~7/25(수)에 request 및 세부 역할 분담, DB 상세 내용 상의~~
