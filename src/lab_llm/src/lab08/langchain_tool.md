# # LangChain`@tool` 데코레이터

```python
from datetime import datetime
from dotenv import load_dotenv
import pytz
from langchain_core.tools import tool   # decorator
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
```
```python
# .env 파일에 저장된 api_key를 OS 환경 변수로 로딩
load_dotenv()
```
<img width="46" height="24" alt="image" src="https://github.com/user-attachments/assets/30ddc5c1-6b58-45fe-b484-819529508488" />

```python
# OpenAI 클라이언트를 생성
model = ChatOpenAI(model = 'gpt-4o-mini')
```
```python
# AI에게 메시지 전달하고 실행(invoke).
messages = [
    SystemMessage(content = '너는 사용자의 질문에 답하는 AI 비서야.'),
    HumanMessage(content = '지금 현재 서울 시간?')
]
ai_message = model.invoke(input = messages)
```
```python
type(ai_message)
```
<img width="308" height="27" alt="image" src="https://github.com/user-attachments/assets/50c8abaf-2382-4413-8683-ca0b485196ec" />

```python
print(ai_message)
```
<img width="1495" height="120" alt="image" src="https://github.com/user-attachments/assets/aa482891-72c0-4c5d-ab8f-6b19690ff43c" />

```python
ai_message.pretty_print()
```
<img width="1360" height="163" alt="image" src="https://github.com/user-attachments/assets/75f95603-518a-4687-a229-843cc40bf382" />

```python
@tool
def get_current_time(timezone, location) -> str:
    """해당 timezone의 현재 날짜 시간을 문자열로 리턴.

    Args:
        timezone (str): 타임존, (예: Asia/Seoul)
        location (str): 지역명: 타임존은 모든 도시 이름에 대응되지 않기 때문에 LLM이 답변을 생성할 때 이용하도록제공
    Returns: '날짜 시간 타임존(지역명)' 형식의 문자열을 반환. (예: 2025-09-15 15:30:55 Asia/Seoul(부산))
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    result = f'{now} {timezone}({location})'

    return result
```
```python
# 도구 목록: @tool 데코레이터가 사용된 함수들의 리스트.
tools = [get_current_time,]
```
```python
# AI에서 도구 목록의 함수 호출을 요청했을 때 함수 객체를 쉽게 찾기 위해서 dict 선언.
# 함수 이름을 key로, 함수 객체를 value로 갖는 딕셔너리.
tool_dict = {
    'get_current_time': get_current_time,
}
```
```python
# AI 모델과 도구 목록을 binding(묶어줌).
model_with_tools = model.bind_tools(tools = tools)
```
```python
print(messages)
```
<img width="1542" height="29" alt="image" src="https://github.com/user-attachments/assets/a9dea0d8-64c2-4673-8de1-6eea6b7fccd1" />

```python
# 도구 목록을 가지고 있는 AI 모델을 호출
response = model_with_tools.invoke(input = messages)
```
```python
type(response)
```
<img width="308" height="30" alt="image" src="https://github.com/user-attachments/assets/5b17aa89-c33b-4f2e-bc3f-2afb64c32d44" />

```python
print(response)  # content가 없음. 대신 tool_calls가 있음.
```
<img width="1578" height="163" alt="image" src="https://github.com/user-attachments/assets/a261edc5-f2ed-4295-898c-82f724cfbfa2" />

```python
response.pretty_print()
```
<img width="653" height="158" alt="image" src="https://github.com/user-attachments/assets/c57c7d82-930c-4cf6-9b1b-af303f404c1f" />

```python
messages.append(response)   # AIMessage 객체를 리스트에 추가
```
```python
for m in messages:
    m.pretty_print()
```
<img width="670" height="292" alt="image" src="https://github.com/user-attachments/assets/47428974-639e-445e-899c-ea43f17eddb7" />

```python
for tool_call in response.tool_calls:
    fn = tool_dict[tool_call['name']]
    tool_msg = fn.invoke(tool_call) # @tool 데코레이터로 포장 -> invoke가 가능.
    messages.append(tool_msg)
```
```python
for m in messages:
    m.pretty_print()
```
<img width="663" height="393" alt="image" src="https://github.com/user-attachments/assets/dcdd9743-e200-4876-be4f-1a417b46f0e0" />

```python
ai_message = model_with_tools.invoke(input=messages)
```
```python
ai_message.pretty_print()
```
<img width="659" height="72" alt="image" src="https://github.com/user-attachments/assets/9ed3e799-c0c9-463e-94e2-696a57c405df" />

