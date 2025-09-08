from io import BytesIO

import requests
from PIL import Image
from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key = get_openai_api_key())

    # GPT 이미지 생성 요청을 보내고, 응답을 받음.
    response = client.images.generate(
        model = 'dall-e-3',  # 이미지 생성 인공지능 모델
        prompt = '디저트 먹고 있는 귀여운 곰돌이',  # 이미지를 생성하기 위한 프롬프트
        size = '1024x1024',  # 생성할 이미지의 크기
        quality = 'standard',  # 생성할 이미지 화질
        n = 1
    )
    # print(response)     # ImagesResponse 객체
    url = response.data[0].url  # GPT 생성한 이미지 URL
    print(url)

    # 생성된 이미지 URL 주소로 GET 방식 요청(request)을 보내고 응답을 받음.
    url_resp = requests.get(url)
    print(url_resp)     # requests.Response 객체, 응답 코드(200 - 성공).
    # 이미지는 텍스트가 아니므로 이진 데이터 형식으로 처리해야 함.
    img_data = BytesIO(url_resp.content)  # 응답에 포함된 컨텐트를 Bytes 객체로 읽음.
    img = Image.open




<img width="934" height="287" alt="image" src="https://github.com/user-attachments/assets/952d4231-35cc-4129-8d33-0992b2c9a268" />



<img width="676" height="694" alt="image" src="https://github.com/user-attachments/assets/9d103674-e920-4d1e-a15e-eb6ad4abd082" />
