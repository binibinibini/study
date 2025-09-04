from openai import OpenAI

from src.utils import get_openai_api_key

if __name__ == '__main__'  # 현재 파일을 메인으로 실행할 때
    # OpenAI 클라이언트 객체 생성(OpenAI에서 발급받은 API 키를 아규먼트로 전달)
    client = OpenAI(api_key = get_openai_api_key())

    # 클라이언트 객체를 사용해서 chat completions 요청을 보냄.
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',  # OpenAI에서 제공하는 LLM 모델(gpt-4o, gpt-4o-mini, gpt-5, gpt-5-mini, ...)
        temperature = 0.5,  # temperature: 온도가 높으면 창의적이지만 일관되지 않은 답변이 생성.
        # 온도가 낮으면 일관된(비슷한) 답변이 생성.

        # messages: 프롬프트(prompt). 역할(role)과 내용(content)을 가지고 있는 dict를 아이템으로 하는 리스트.
        # role(역할): system(ChatGPT), user(사용자), assistant(비서)
        messages = [
          {
              'role': 'system',
              'content': '너는 나를 도와주는 비서야.',
          },
          {
              'role': 'user',
              'content': '나는 지금 누구랑 대화하고 있어?'
          }
        ]
    )
    print(response)     # ChatCompletion 객체
    print('-' * 10)
    print(response.choices[0])  # Choice 객체
    print('-' * 10)
    print(response.choices[0].message)  # ChatCompletionMessage 객체
    print('-' * 10)
    print(response.choices[0].message.content)  # GPT가 생성한 답변



```결과
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab01\basic.py 
ChatCompletion(id='chatcmpl-CBxFKLNhoBZmKQHuBbfAuBArzePac', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='당신은 AI 비서와 대화하고 있습니다. 제가 도와드릴 수 있는 것이 있다면 말씀해 주세요!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1756965386, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_560af6e559', usage=CompletionUsage(completion_tokens=26, prompt_tokens=31, total_tokens=57, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
----------
Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='당신은 AI 비서와 대화하고 있습니다. 제가 도와드릴 수 있는 것이 있다면 말씀해 주세요!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))
----------
ChatCompletionMessage(content='당신은 AI 비서와 대화하고 있습니다. 제가 도와드릴 수 있는 것이 있다면 말씀해 주세요!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)
----------
당신은 AI 비서와 대화하고 있습니다. 제가 도와드릴 수 있는 것이 있다면 말씀해 주세요!

종료 코드 0(으)로 완료된 프로세스
```
