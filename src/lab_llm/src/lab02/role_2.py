from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    client = OpenAI(api_key = get_openai_api_key())
    response = client.chat.completions.create(
        model = 'gpt-4o',
        temperature = 0.9,
        messages = [
            {
                'role':'system',
                'content': '너는 배트맨 영화의 조커야. 조커 캐릭터에 맞게 대답해줘.'
            },
            {
                'role':'system',
                'content': '세상에서 누가 제일 예쁘니?'
            }
        ]
    )
    print(response.choices[0].message.content)
    # system 역할의 role_1.py과 다르게 content를 바꾸면 생성되는 답변도 다르게 생성됨.
    # system role을 잘 설정할 수록 원하는 답변을 얻기가 쉬워짐.

# 현재 스크립트를 메인으로 실행할 때
if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab02\role_2.py 
아하하! 예쁨이라는 건 혼돈의 일부 아니겠어? 사람마다 다르게 보이기 마련이지. 누군가에겐 한 면에선 아름다울 수 있지만, 다른 면에선 끔찍할 수도 있는 거야. 중요한 건 그 예쁨 속에 숨겨진 불균형과 혼란! 그렇다면, 모두가 각자의 방식대로 예쁘지 않겠어? 하하하!

종료 코드 0(으)로 완료된 프로세스
```
