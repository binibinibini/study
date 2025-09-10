```python
import json
from openai import OpenAI

from src.utils import get_openai_api_key
from src.lab07.time_util import tools, get_current_time

def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = messages,
        tools = tools,  # GPT가 필요로 할 때 호출할 수 있는 도구 목록
    )
    return response     # response.choices[0].message.content

def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key = get_openai_api_key())

    # 초기 메시지 프롬프트
    messages = [{'role':'system', 'content':'너는 사용자의 질문에 답하는 유능한 AI비서야.'}]

    while True:     # 무한 루프
        user_input = input('사용자>>> ')
        if user_input.strip() == '':
            continue    # 루프를 다시 반복
        if user_input.strip() == 'exit':
            break   # 무한 루프를 종료

        messages.append({'role':'user', 'content':user_input})
        response = get_gpt_response(client, messages)
        print(response)

        tool_calls = response.choices[0].message.tool_calls # None일수도 있고 아닐수도 있음.
        if tool_calls:  # tool_calls가 있으면 (if tool_calls != None).
            # GPT가 여러 함수를 차례로 실행하려고 요청을 했을 때
            for tool_call in tool_calls:    # tool_calls 리스트의 아이템들을 순서대로 반복하면서
                tool_call_id = tool_call.id     # 도구 호출 목록의 아이디
                function_name = tool_call.function.name     # 도구 호출 목록의 함수 이름.
                # json.loads(str) -> dict: 역직렬화(de-serialization)
                arguments = json.loads(tool_call.function.arguments)    # 함수를 호출할 때 필요한 아규먼트들.(arguments는 문자열)
                # get_current_time 함수 호출을 요청한 경우
                if function_name == 'get_current_time': # GPT가 호출한 함수 이름이 get_current_time인 경우
                    # 도구 목록의 함수를 호출해서 그 실행 결과를 메시지에 추가.
                    messages.append({
                        'role':'function',
                        'tool_call_id':tool_call_id,    # GPT한테 받은 id
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

```
<결과> -> 반복문 4번돌아간거
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab07\function_call.py 
사용자>>> 서울, 런던, 뉴욕, 베이징 현재 시간?
ChatCompletion(id='chatcmpl-CE4QbNkJlmRxarQ83OIlTHjnvu1mU', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_1plY5kH1E8FsEBmSCq7kJFYq', function=Function(arguments='{"timezone": "Asia/Seoul"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_JnLa7Gixtq7arLFf1UsdeqvL', function=Function(arguments='{"timezone": "Europe/London"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_eEQySj27zeCPa5WB2uwjqXce', function=Function(arguments='{"timezone": "America/New_York"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_92HAmnv9UtzNQe0qrZ42eqBZ', function=Function(arguments='{"timezone": "Asia/Shanghai"}', name='get_current_time'), type='function')]))], created=1757469649, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=86, prompt_tokens=100, total_tokens=186, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
ChatCompletion(id='chatcmpl-CE4QdaT6uGf6kX5Flxb0F6vc86N2z', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='현재 각 도시의 시간은 다음과 같습니다:\n\n- 서울: 2025-09-10 11:00:49\n- 런던: 2025-09-10 03:00:49\n- 뉴욕: 2025-09-09 22:00:49\n- 베이징: 2025-09-10 10:00:49', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1757469651, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=83, prompt_tokens=200, total_tokens=283, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
```
