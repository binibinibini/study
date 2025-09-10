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

        messages.append({'role':'user', 'content':user_input})    # 사용자의 역할
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


<img width="868" height="661" alt="image" src="https://github.com/user-attachments/assets/8daed8b4-c8fa-4d16-892a-882291e07407" />

```
<결과>

C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab07\function_call.py 
사용자>>> 너 누구니
ChatCompletion(id='chatcmpl-CE3jLWvl8TG9xDzhyDzsAM9jTBstu', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='저는 당신의 질문에 답하고 필요한 정보를 제공하는 AI 비서입니다. 무엇을 도와드릴까요?', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1757466967, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=26, prompt_tokens=88, total_tokens=114, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
사용자>>> 지금 몇시야
ChatCompletion(id='chatcmpl-CE3jRuZFEBjGt01DpligB4zWKF2zs', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='어떤 시간대의 현재 시간을 알고 싶으신가요? 예를 들어, "Asia/Seoul" 또는 "America/New_York"과 같은 형식으로 말씀해 주시면 됩니다.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1757466973, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=43, prompt_tokens=126, total_tokens=169, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
사용자>>> LA?
ChatCompletion(id='chatcmpl-CE3m7M70BoDIwjK3NgwM7njY7fZyF', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_CaSc6l2lUMBHyGBuqOtV9uKL', function=Function(arguments='{"timezone":"America/Los_Angeles"}', name='get_current_time'), type='function')]))], created=1757467139, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=19, prompt_tokens=178, total_tokens=197, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
ChatCompletion(id='chatcmpl-CE3m8LoKaepseaBGvmBvTjdLNhCpa', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='현재 로스앤젤레스의 시간은 2025년 9월 9일 오후 6시 18분입니다.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1757467140, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=30, prompt_tokens=215, total_tokens=245, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
사용자>>> 런던, 파리, 베이징의 현재 시간?
ChatCompletion(id='chatcmpl-CE3qN3lSVOUeVaJokOaRkElb65QvF', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_tmlLkybaBtmLbxeVlL6Vk8o9', function=Function(arguments='{"timezone": "Europe/London"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_z2F3UtOyohHgXra45D00cldY', function=Function(arguments='{"timezone": "Europe/Paris"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_cVwGNFfemnjTwmiW3ZhQtW8A', function=Function(arguments='{"timezone": "Asia/Shanghai"}', name='get_current_time'), type='function')]))], created=1757467403, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=67, prompt_tokens=265, total_tokens=332, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
ChatCompletion(id='chatcmpl-CE3qOs98Z1N8E0GuG5Zvm88ld0Qtc', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_WsjU0RXSQmmSllHJvoShxIBS', function=Function(arguments='{"timezone": "Europe/Paris"}', name='get_current_time'), type='function'), ChatCompletionMessageFunctionToolCall(id='call_LUdyOYLDgfFeYh61zwZcw8UN', function=Function(arguments='{"timezone": "Asia/Shanghai"}', name='get_current_time'), type='function')]))], created=1757467404, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_8bda4d3a2c', usage=CompletionUsage(completion_tokens=50, prompt_tokens=300, total_tokens=350, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
```
