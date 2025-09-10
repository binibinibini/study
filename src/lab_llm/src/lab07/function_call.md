```python
import json
from openai import OpenAI

from src.utils import get_openai_api_key
from src.lab07.time_util import tools, get_current_time

def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = messages,
        tools = tools,
    )
    return response     # response.choices[0].message.content

def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key = get_openai_api_key())

    # 초기 메시지 프롬프트
    messages = [{'role':'system', 'content':'너는 사용자의 질문에 답하는 유능한 AI비서야.'}]

    while True:     # 무한 루프
        user_input = input('사용자>>> ')
        if user_input.strip() == '':    # 양 끝에 있는 공백 제거
            continue    # 루프를 다시 반복
        if user_input.strip() == 'exit':
            break   # 무한 루프를 종료

        messages.append({'role':'user', 'content':user_input})
        response = get_gpt_response(client, messages)
        print(response)

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:  # tool_calls가 있으면 (if tool_calls != None)
            # GPT에서 우리가 제공한 도구 목록 중에서 어떤 함수의 호출을 요청한 경우
            tool_call_id = tool_calls[0].id     # 도구 호출 첫번째 목록의 아이디
            function_name = tool_calls[0].function.name     # 도구 호출 첫번째 목록의 함수 이름
            arguments = json.loads(tool_calls[0].function.arguments)    # 역직렬화: JSON 형식의 문자열 -> dict
            if function_name == 'get_current_time':
                # 도구 목록의 함수를 호출해서 그 실행 결과를 메시지에 추가.
                messages.append({
                    'role':'function',
                    'tool_call_id':tool_call_id,
                    'name':function_name,
                    'content': get_current_time(arguments['timezone']),   # 함수 호출 -> 리턴 값을 'content'에 저장.
                })

                # 간혹 GPT가 불필요하게 도구 호출 요청을 반복하는 경우가 있음.
                # GPT의 이런 실수를 방지하기 위해서 system 프롬프트를 추가하는 트럭을 사용.
                messages.append({'role': 'system', 'content': '주어진 결과로 답변을 만들어줘.'})

                # 도구 호출 결과를 포함한 메시지 프롬프트를 사용해서 다시 GPT 요청을 보냄.
                # -> 함수 호출 결과(function 역할의 content)를 사용한 답변을 생성해서 보낼 줄 것으로 예상.
                response = get_gpt_response(client, messages)
                print(response)

        # 챗봇에서 이전 질문에 대한 답변들을 기억해서 문맥에 맞는 답변을 유도하기 위해서
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})

if __name__ == '__main__':
    main()
```
<img width="847" height="286" alt="image" src="https://github.com/user-attachments/assets/9f4fffa3-fb82-48ba-bdca-8f521a66d0e8" />

