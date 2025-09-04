from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    client = OpenAI(api_key = get_openai_api_key())
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        temperature = 0.9,
        # one-shot prompting: user-assistant 프롬프트를 한 번 작성한 것.
        # GPT가 사용자가 원하는 패턴에 맞춰서 답변하도록 예시를 한 번 제시해서 답변을 유도.
        messages=[
            {'role':'system', 'content':'너는 유치원생이야. 유치원생처럼 대답해줘.'},
            {'role':'user', 'content':'참새'},
            {'role':'assistant', 'content': '짹짹'},
            {'role':'user', 'content': '오리'}    # 오리에 대한 대답을 듣기 위해서 위에 두 줄 문맥들을 전달함. 유도한거
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab03\one_shot_prompt.py 
꽥꽥! 오리 귀여워! 물에 헤엄치고 싶어!

종료 코드 0(으)로 완료된 프로세스
```
