# 무인점포 선도관리 시스템



## 프로젝트 소개

제품의 바코드와 유통기한 OCR을 통해 선도(유통기한)관리를 하는 프로젝트



## 사용 기술

* 프로그램 언어 : Python

* 웹 프레임워크(Client) : Streamlit

* 객체 검출 : Pytorch(Yolov5)

* OCR : Naver Clova OCR API

* API 구현 :  FastAPI

* DB : MySQL(SQLAlchemy)

* 배포 : AWS Lightsail

  

## 프로젝트 세부 소개

**Client**

* Client 구현은 Web보다 프로젝트에 집중할 수 있도록 App 구현이 용이한 Streamlit을 사용
* 바코드 인식률을 높이기 위해 비용 대비 높은 정확도를 가진 바코드 리더기를 통해 바코드 인식 
* 유통기한이 있는 부분을 촬영해 AI 서버로 전송
* 응답 받은 유통기한의 형태가 다양한 형태이기 때문에 후처리 코드를 통해 YYYY/MM/DD 형태로 결과를 통일
* AI 서버에서 응답 받은 유통기한을 유저에게 보여주고 등록(True)와 재촬영(False)를 통해 알맞는 행동을 AI 서버와 AP서버로 전송

**AI Server**

* 기존의 유통기한 이미지(1500개)로 학습된 Yolov5 모델에 마트에서 직접 수집한 유통기한 이미지 800장을 통해 추가 학습시켜 Object Detection을 수행
* OCR 정확도를 높이기 위해 이진화, 침식, 팽창을 적용
* Client에서 보낸 이미지 정보를 추론해 네이버 Clova OCR을 통해 유통기한을 구한 뒤 결과를 Client로 보내준다. 

**AP Server**

* DB는 데이터 유형이 규칙적이기 때문에 관계형 DB를 선택했고 그 중 AWS Lightsail에서 제공하는 MySQL 사용
* 객체 지향적 코드로 DB에 접근해 코드 재사용 및 유지보수 편리성이 높은 SQLAlchemy 사용
* 직관적이고 API 문서 자동 생성과 테스트가 가능한 FastAPI 사용
* Client에서 보내는 조회 요청과 DB INSERT 요청을 SQLAlchemy로 구현해 처리
* Client에서 재촬영 버튼을 눌렀을 때 인식이 잘 안된 이미지를 별도로 서버에 저장해 추후 재학습을 위한 이미지 데이터 확보
* 모든 서버들은 AWS Lightsail을 통해 배포



## 확장 가능성 및 보완점

* 재학습을 통한 Object detection 모델 정확도 개선
  * 유통기한이 제대로 인식되지 않았던 이미지만 골라 학습 가능
  * 라벨링 툴 개발 필요
* 자체 OCR 모델의 대체
  * 현재 네이버 Clova OCR을 통해 OCR을 수행하지만 추후 비용 문제가 생길 수 있어 자체 OCR모델로 대체 필요



