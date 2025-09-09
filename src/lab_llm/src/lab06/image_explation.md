## GPT로 이미지 설명 만들기

```python
import base64
from openai import OpenAI
from src.utils import get_openai_api_key
```
```python
 client = OpenAI(api_key = get_openai_api_key())
```

## [Lorem Picsum](https://picsum.photos) 이미지 설명 요청

```python
# 이미지 설명을 요청하는 메시지 프롬프트 작성
messages = [  # API 요청에 포함될 대화 메시지 목록을 정의
   {
       'role':'user', # 메시지를 보낸 주
       'content': [
           {'type': 'text', 'text': '이 이미지를 설명해줘.'},
           {'type': 'image_url', 
            'image_url':{'url':''https://fastly.picsum.photos/id/866/200/300.jpg?hmac=rcadCENKh4rD6MAp6V_ma-               AyWv641M4iiOpe1RyFHeI'}}, # API가 접근할 수 있는 이미지의 웹 주소(이 주소를 통해 GPT 모델이 이미지를 직접 다운로드해서 분석함)
      ],
   },
]
```
```python
response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = messages
)
```
```python
response
```
<img width="1522" height="150" alt="image" src="https://github.com/user-attachments/assets/08b7e525-c793-4de2-9d33-cbd72491e222" />

```python
response.choices[0].message.content
```
<img width="1524" height="53" alt="image" src="https://github.com/user-attachments/assets/c1ac241d-b612-4083-98db-6904263a84c2" 
/>


## 로컬 이미지 파일의 설명 요청하기

```
*   이미지 바이너리 데이터를 텍스트 형식으로 변환해서 GPT chat.completions 요청을 보내야 함.
*   base64 라이브러리: 이진(binary) 데이터를 아스키(ASCII) 문자로 인코딩(변환).
    *   전송/저장 호환성
    *   데이터 손상 방지
    *   프로토콜 호환성
```
```python
def base64encode_image(image_file):
    with open(file = image_file, mode = 'rb') as f: # 이미지 파일을 오픈.
        data = f.read()  # 이미지 파일의 이진 데이터를 읽음.

        # 이진 데이터를 base64 인코딩을 해서 ASCII 문자열로 변환, UTF-8로 변환해서 리턴.
        return base64.b64encode(data).decode(encoding = 'utf-8')
```
```python
image_path_1 = 'images/image_4.jpg'
image_path_2 = 'images/image_5.jpg'
```
```python
base64_image_1 = base64encode_image(image_path_1) # 문자열 리턴
```
```python
base64_image_1[:100] # base64로 인코딩된 문자열들 중에서 앞에서 100개만 출력.
```
<img width="828" height="29" alt="image" src="https://github.com/user-attachments/assets/af43afe3-82e5-4ad8-9c90-7d775634ba55" />

```python
# GPT에게 보낼 메시지 프롬프트 작성
messages = [
  {
      'role': 'user',
      'content': [
          {},

       ],
  },
]
```


















```
두 디저트의 차이점을 설명해드릴게요.

1. **마카롱 (Macaron)**:
   - **재료**: 주로 아몬드 가루, 설탕, 달걀 흰자 등으로 만들어집니다.
   - **구조**: 두 개의 얇고 바삭한 외피 사이에 크림이나 잼을 넣어 완성됩니다.
   - **텍스처**: 겉은 바삭하고 속은 부드러운 조화로운 식감을 제공합니다.
   - **맛**: 다양한 색상과 맛으로, 프랑스의 전통적인 디저트입니다.

2. **케이크 (Cake)**:
   - **재료**: 밀가루, 설탕, 계란, 버터 등의 반죽이 기본입니다.
   - **구조**: 일반적으로 여러 겹의 시트로 이루어진 크림 케이크이며, 다양한 토핑과 장식이 가능합니다.
   - **텍스처**: 부드럽고 촉촉한 식감을 가지며, 크림이나 아이싱으로 장식되어 시각적으로도 매력적입니다.
   - **맛**: 각종 맛과 스타일이 있으며, 특히 특별한 날에 자주 만들어집니다.
```
<img width="666" height="439" alt="image" src="https://github.com/user-attachments/assets/86d686af-84a9-47e1-a15d-7710ba20b40c" />
