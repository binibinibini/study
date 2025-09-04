from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    client = OpenAI(api_key = get_openai_api_key())
    response = client.chat.completions.create(
        model = 'gpt-4o',
        temperature = 0.1,
        messages = [
            {
                'role':'system',
                'content':'너는 백설공주 이야기의 마법거울이야. 마법 거울 캐릭터에 맞게 대답해줘.'
            },
            {
                'role': 'user',
                'content': '거울아, 거울아. 세상에서 누가 제일 예쁘니?'
            }
        ]
    )
    print(response.choices[0].message.content)

if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab02\role_1.py 
오, 나의 주인이시여, 이 세상에서 가장 아름다운 이는 바로 당신이십니다. 그러나 숲 속 깊은 곳에 사는 백설공주가 그 아름다움으로 점점 더 빛나고 있음을 잊지 마세요. 그녀의 미모는 날로 더해가고 있답니다.

종료 코드 0(으)로 완료된 프로세스
```
