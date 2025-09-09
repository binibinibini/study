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
       'role':'user', # 메시지를 보낸 주체
       'content': [
           {'type': 'text', 'text': '이 이미지를 설명해줘.'},
           {'type': 'image_url', 
            'image_url':{'url':''https://fastly.picsum.photos/id/866/200/300.jpg?hmac=rcadCENKh4rD6MAp6V_ma-AyWv641M4iiOpe1RyFHeI'}}, # API가 접근할 수 있는 이미지의 웹 주소(이 주소를 통해 GPT 모델이 이미지를 직접 다운로드해서 분석함)
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
            {'type': 'text', 'text': '이미지에 대해서 설명해줘.'},
            {
                'type': 'image_url',
                'image_url':{'url': f'data:image/jpeg;base64, {base64_image_1}'},
            },
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
response.choices[0].message.content
```
```
'이미지에는 다섯 개의 마카롱이 나열되어 있습니다. 상단에는 분홍색 마카롱이 있으며, 그 아래에는 보라색, 녹색 마카롱이 차례로 쌓여 있습니다. 옆에는 노란색 마카롱이 위치해 있습니다. 배경은 연한 분홍색으로 부드러운 느낌을 주며, 전체적으로 아기자기하고 달콤한 분위기를 형성하고 있습니다. 마카롱들은 각각의 색상이 뚜렷하고 조화롭게 배열되어 있습니다.'
```

### 이미지 2장을 비교/설명 요청하는 메시지 프롬프트를 작성하고, 실행 결과를 확인해 보세요.

```python
base64_image_2 = base64encode_image(image_path_2)   # cafe2.jpg를 base64 인코딩
base64_image_2[:100]
```
<img width="837" height="33" alt="image" src="https://github.com/user-attachments/assets/3dc47acf-674e-4f5b-b453-02a67e9cd841" />

```python
# 이미지 비교를 요청하는 메시지 프롬프트 작성
message = [
    {
        'role': 'user',
        'content': [
            {'type': 'text', 'text': '두 디저트의 차이점을 설명해줘.'},
            {
                'type': 'image_url',
                'image_url': {'url': f'data:image/jpeg;base64, {base64_image_1}'},
            },
            {
                'type': 'image_url',
                'image_url': {'url': f'data:image/jpeg;base64, {base64_image_2}'},
            },
        ],
    },
]
```
```python
response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = message
)
```
```python
print(response.choices[0].message.content)
```
<img width="741" height="341" alt="image" src="https://github.com/user-attachments/assets/7eb1e5cd-06c2-4356-84c2-c1c15ec27c5c" />
