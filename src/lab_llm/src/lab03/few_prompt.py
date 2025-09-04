from http.client import responses

from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    client = OpenAI(api_key = get_openai_api_key())
    responses = client.chat.completions.create(
        model = 'gpt-4o-mini',
        temperature = 0.9,
        # few-shot prompting: 원하는 답변을 유도하기 위해서 예시를 여러 번 전달하는 것.
        messages = [
            {'role': 'system', 'content': '너는 유치원생이야. 유치원생처럼 대답해줘.'},
            {'role': 'user', 'content': '참새'},
            {'role': 'assistant', 'content':'짹짹'},
            {'role':'user', 'content': '개구리'},
            {'role': 'assistant', 'content': '개굴개굴'},
            {'role': 'user', 'content': '소'},
            {'role': 'assistant', 'content': '음머~'},
            {'role': 'user', 'content': '오리'}
        ]
    )
    print(responses.choices[0].message.content)

if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab03\few_prompt.py 
꽥꽥!

종료 코드 0(으)로 완료된 프로세스
```
