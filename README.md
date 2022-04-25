# [퀀트마그넷(quantmag.net)](http://quantmag.net)

> - [기술 스택](#기술-스택)
> - [제공 서비스 및 설명](#제공-서비스-및-설명)
>   1. [종목스크리너](#종목스크리너)
>   2. [자산가치 계산기](#자산가치-계산기)
>   2. [CAGR 계산기](#cagr복합-연평균-성장률-계산기)
<!-- > - [아키텍처](#아키텍처) -->

>**퀀트마그넷**은 퀀트(수학·통계 지식을 이용해 투자를 행하는 사람)와 자석의 합성어로 퀀트로 자산을 자석처럼 끌어 모으겠다는 뜻을 가지고 있습니다. 

>해당 프로젝트는 복잡한 주식 데이터를 다양한 형태로 쉽게 서비스하는 것을 목적으로 합니다.

---
## 기술 스택
Backend
- Django
- Django Rest Framework
- Docker
- nginx
- ~~uwsgi~~
- gunicorn 

frontend
- ~~bootstrap~~
- React
- ~~jquery~~
- react-router-dom
- axios
- Chart.js

Database
- ~~MongoDB~~
- Postgresql

---
## API 명세서
https://documenter.getpostman.com/view/15790299/UyrBjw6m

---
## 제공 서비스 및 설명

### 종목스크리너
주식을 조금 공부하다보면 "저PER, 저PBR인 저평가 주식을 사라"와 같은 말을 들어 볼 수 있습니다. 하지만 국내 2400여개 이상의 주식(코스피+코스닥) 종목들을 일일이 확인하는 것은 쉽지않은 일입니다.
<br>...

### 자산가치 계산기
매월 10만원씩 10년간 **저축**을 하면 10년 후 자산은 1200만원으로 쉽게 계산이 가능하지만, 매월 10만원씩 매년 10% 수익을 낼 수 있을 때 10년 후의 자산을 계산하는 것은 조금 복잡해집니다. **투자**의 경우는 발생하는 수익으로 인해 복잡한 **복리계산**을 해야하고 **자산가치 계산기**는 간단히 계산해주고 차트형태로 제공합니다.

### CAGR(복합 연평균 성장률) 계산기
[자산가치 계산기](#자산가치-계산기)에서 사용되는 연이율은 단순 매년 수익률이 아니라 *오랜 기간 수익률과 손실률을 포함한 수익률*의 평균(**CAGR**) 을 사용해야 합니다. 
<br>CAGR을 설명하기 위한 예로 2000년 코스피 지수는 504에서 2020년 2873이 되었습니다. 20년동안 크고 작은 낙폭이 있었지만 결과적으로 **20년간 수익률은 약 470%** 가 되었습니다.

<p style="background-color:white" align="center"><img sytle="color:#ffffff" src="https://render.githubusercontent.com/render/math?math=504%20\times%20(1.0909)^{20}%20\approx%202873"></p>

위 식을 살펴보면 매년 9.09% 수익률을 얻을 수 있다면 20년 후에 2873가 됩니다. 이때 매년 평균적으로 발생하는 9.09%의 수익률을 **CAGR** (복합 연평균 성장률)이라고 합니다. 



<!-- 
## 아키텍처
[전체 구성 이미지]
### Docker
[도커 구성 이미지]

### Nginx
Nginx 설정 코드 이미지

##  -->