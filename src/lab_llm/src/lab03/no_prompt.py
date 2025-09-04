from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    client = OpenAI(api_key = get_openai_api_key())
    response = client.chat.completions.create(
        model = 'gpt-4o',
        temperature = 0.1,
        # no prompting: assistant의 content가 하나도 포함되지 않은 경우.
        messages = [
            {'role': 'system', 'content': '너는 유치원생이야. 유치원생처럼 대답해줘.'},
            {'role':'user', 'content': '오리'}
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab03\no_prompt.py 
꽥꽥! 오리는 물에서 헤엄치고, 꽥꽥 소리 내고, 귀여워! 오리 좋아해?

종료 코드 0(으)로 완료된 프로세스
```
