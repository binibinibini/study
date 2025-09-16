# LangChain`@tool` 데코레이터

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
<img width="700" height="92" alt="image" src="https://github.com/user-attachments/assets/e664df36-b2ba-4033-a3f6-6cc670b00177" />

```
도구(tool)을 AI에게 제공하고, AI는 tool 목록에 있는 함수 호출(function calling)을 요청해서 에이전트가 함수 호출 결과를 다시 AI에게 전송하면 AI는 함수 호출 결과를 바탕으로 답변을 생성할 수 있음.

사용자 질문(도구 목록 제공) -> AI 도구 호출 -> 사용자 함수 호출 결과 -> AI 답변 생성.
```

```python
@tool
def get_current_time(timezone: str, location: str) -> str:
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
    fn = tool_dict[tool_call['name']]   # AIMessage에 포함된 함수 이름으로 함수 객체를 찾음.
    tool_msg = fn.invoke(tool_call) # @tool 데코레이터로 포장 -> invoke가 가능.
    # invoke: tool_call에서 args를 찾고 fn를 호출할 때 아규먼트를 전달. 리턴값을 이용해서 ToolMessage 객체 반환.
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



## 2개 이상의 도구 호출을 포함하는 tool_calls 리스트

```python
messages = [
    SystemMessage('사용자의 질문에 답하기 위해서 도구를 사용할 수 있어.'),
    SystemMessage('도시 이름과 타임존은 일치하지 않을 수도 있으니, 정확한 타임존을 선택해줘.'),
    HumanMessage('서울, 부산, 런던의 현재 시간은?'),
]
```
```python
ai_message = model_with_tools.invoke(input = messages)
```
```python
messages.append(ai_message)
```
```python
for m in messages:
    m.pretty_print()
```
<img width="683" height="588" alt="image" src="https://github.com/user-attachments/assets/80555e9c-f9df-4db3-994c-07edc72744ca" />

```python
for tool_call in ai_message.tool_calls:
    fn = tool_dict[tool_call['name']]
    tool_msg = fn.invoke(tool_call)
    messages.append(tool_msg)
```
```python
for m in messages:
    m.pretty_print()
# 다시 한번 메시지를 보내기 전 상태
```
<img width="666" height="839" alt="image" src="https://github.com/user-attachments/assets/279ced30-a188-46de-8e55-7d2555eecc20" />

```python
ai_message = model_with_tools.invoke(input = messages)
```
```python
ai_message.pretty_print()
```
<img width="656" height="164" alt="image" src="https://github.com/user-attachments/assets/2f888768-a24c-41bf-8ec1-3229b35a3a2a" />

# Pydantic

입력된 데이터의 유효성과 형식을 검증하고 특정 데이터 형식으로 명확히 표현하는 라이브러리.


```python
def subtract(x: int, y: int) -> int:    # subtract() 이 함수가 int를 리턴한다는거
    return x - y
```
```python
subtract(1, 2)
```
<img width="35" height="23" alt="image" src="https://github.com/user-attachments/assets/70bb9f57-ff6f-4682-b7c0-d882842e1cf1" />

```python
subtract(1.1, 2.5)
```
<img width="51" height="26" alt="image" src="https://github.com/user-attachments/assets/68b9c533-050b-4eec-ba52-775ab725cdb1" />

<br>
Python은 파라미터의 타입 검사를 하지 않고, 리턴 타입도 힌트대로 반환하는 것은 아님.
<br>


```python
subtract('a', 'b')  # 타입 에러가 아니라 +이면 문제 없는데 - 이 연산자 때문에 에러난거
```
<img width="703" height="225" alt="image" src="https://github.com/user-attachments/assets/b486ae43-c6bc-4d47-b29a-a73c96c79027" />

```python
class Person:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
```
```python
person = Person(id = 1, name = '오쌤')
```
```python
print(person.id)
```
<img width="27" height="24" alt="image" src="https://github.com/user-attachments/assets/cc15e035-9ad1-4529-bce3-4c589b6a5779" />

```python
person2 = Person(id = 'abc123', name = 123)
```
```python
print(person2.id)
```
<img width="63" height="26" alt="image" src="https://github.com/user-attachments/assets/d0d60b76-0243-48e5-b2f1-b20603388f1a" />

<br>
Python은 객체를 생성할 때 속성(property)들의 타입 검사를 수행하지 않음.
<br>

```python
from pydantic import BaseModel, ValidationError, PositiveInt
```
```python
# 클래스 이름 안에 클래스 이름 들어있는건 상속임
class Person(BaseModel):    # Person 클래스는 BaseModel 클래스를 상속(확장).
    id: PositiveInt     # 양의 정수
    name: str   # 문자열
```
```python
person3 = Person(id = 12345, name = '홍길동')
```
```python
print(person3)  # Person@123456abcd
```
<img width="182" height="32" alt="image" src="https://github.com/user-attachments/assets/02add27d-42cc-4be2-9cc5-2d43113aec04" />

```python
person3.model_dump()    # 인스턴스의 속성(property) 이름과 값으로 dict를 생성해서 리턴.
```
<img width="251" height="29" alt="image" src="https://github.com/user-attachments/assets/bf823d29-570f-459b-b3b8-95269c88cf9b" />

```python
try:
    person4 = Person(id = 'abc123', name = 1_000)
    print(person4)
except ValidationError as e:
    print(e)
# error 메시지가 출력 됨
```
<img width="1040" height="159" alt="image" src="https://github.com/user-attachments/assets/81f80deb-ba19-49a2-baee-8e4e358133f2" />

```python
person5 = Person(**{'id': 123456, 'name': '길동이'})  # **: unpacking 연산자(dict를 key:value, key:value로 바꿔줌)
print(person5)
```
<img width="192" height="29" alt="image" src="https://github.com/user-attachments/assets/e4ac9402-55f2-40d6-8f2b-39ea3df63071" />


## Pydantic을 이용한 함수 파라미터 타입 객체 선언


```python
from pydantic import Field
```
```python
# 주식 가격 조회 함수의 파라미터 타입으로 사용할 클래스.
class StockHistoryArgs(BaseModel):
    ticker: str = Field(..., title = '주식 코드',
                        description='주식 데이터를 검색하기 위한 주식 코드(예: AAPL, AMZN)')
    period: str = Field(..., title = '기간',
                        description='주식 데이터 조회 기간(예: 1d, 1mo, 1y)')
```
```python
StockHistoryArgs.model_json_schema()
```
<img width="748" height="207" alt="image" src="https://github.com/user-attachments/assets/24fbe925-59e4-4498-a7de-6d49b3898eee" />

```python
import yfinance as yf
```
```python
@tool
def get_yf_stock_history(input: StockHistoryArgs):
    """해당 기간(period) 동안 주식 코드(ticker)의 데이터를 조회하는 함수."""
    ticker = yf.Ticker(input.ticker)
    history = ticker.history(period = input.period)
    return history.to_markdown()    # 조회한 데이터를 마크다운(Markdown) 형식의 문자열로 리턴.
```
```python
tools = [get_current_time, get_yf_stock_history,]
```
```python
tool_dict = {
    'get_current_time': get_current_time,
    'get_yf_stock_history': get_yf_stock_history,
}
```
```python
model_with_tools = model.bind_tools(tools = tools)  # 도구 목록을 포함하는 AI 모델 객체
```
```python
messages = [
    SystemMessage('답변을 생성하기 위해 도구를 사용할 수 있어.'),
    SystemMessage('도시 이름과 타임존은 일치하지 않을 수도 있어.'),
    SystemMessage('ticker는 실제 사용되는 주식 코드여야 해.'),
    HumanMessage('삼성전자는 한 달 전과 비교해서 주식이 올랐어? 내렸어?'),
]
```
```python
ai_message = model_with_tools.invoke(input = messages)
```
```python
messages.append(ai_message)
```
```python
for m in messages:
    m.pretty_print()
```
<img width="659" height="401" alt="image" src="https://github.com/user-attachments/assets/9bfa34f5-8312-474c-8f0c-6479cad33a56" />

```python
for tool_call in ai_message.tool_calls:
    fn = tool_dict[tool_call['name']]
    tool_msg = fn.invoke(tool_call)
    messages.append(tool_msg)
```
```python
for m in messages:
    m.pretty_print()
```
```
<결과>
================================ System Message ================================

답변을 생성하기 위해 도구를 사용할 수 있어.
================================ System Message ================================

도시 이름과 타임존은 일치하지 않을 수도 있어.
================================ System Message ================================

ticker는 실제 사용되는 주식 코드여야 해.
================================ Human Message =================================

삼성전자는 한 달 전과 비교해서 주식이 올랐어? 내렸어?
================================== Ai Message ==================================
Tool Calls:
  get_yf_stock_history (call_GXwIwwPbJ3N1MQ61yYonunzu)
 Call ID: call_GXwIwwPbJ3N1MQ61yYonunzu
  Args:
    input: {'ticker': '005930.KS', 'period': '1mo'}
================================= Tool Message =================================
Name: get_yf_stock_history

| Date                      |   Open |   High |   Low |   Close |      Volume |   Dividends |   Stock Splits |
|:--------------------------|-------:|-------:|------:|--------:|------------:|------------:|---------------:|
| 2025-08-18 00:00:00+09:00 |  71100 |  71200 | 70000 |   70000 | 1.35956e+07 |           0 |              0 |
| 2025-08-19 00:00:00+09:00 |  70400 |  70700 | 69700 |   70000 | 1.05331e+07 |           0 |              0 |
| 2025-08-20 00:00:00+09:00 |  70100 |  70700 | 69400 |   70500 | 1.74455e+07 |           0 |              0 |
| 2025-08-21 00:00:00+09:00 |  71500 |  71900 | 70600 |   70600 | 1.88438e+07 |           0 |              0 |
| 2025-08-22 00:00:00+09:00 |  71700 |  71800 | 70800 |   71400 | 9.27743e+06 |           0 |              0 |
| 2025-08-25 00:00:00+09:00 |  71700 |  71800 | 71000 |   71500 | 1.03452e+07 |           0 |              0 |
| 2025-08-26 00:00:00+09:00 |  70800 |  71100 | 70300 |   70300 | 1.47125e+07 |           0 |              0 |
| 2025-08-27 00:00:00+09:00 |  70100 |  70900 | 69800 |   70600 | 1.05234e+07 |           0 |              0 |
| 2025-08-28 00:00:00+09:00 |  70100 |  70400 | 69600 |   69600 | 1.1578e+07  |           0 |              0 |
| 2025-08-29 00:00:00+09:00 |  70100 |  70500 | 69700 |   69700 | 1.16823e+07 |           0 |              0 |
| 2025-09-01 00:00:00+09:00 |  68400 |  68600 | 67500 |   67600 | 1.20023e+07 |           0 |              0 |
| 2025-09-02 00:00:00+09:00 |  67800 |  69500 | 67800 |   69100 | 1.0604e+07  |           0 |              0 |
| 2025-09-03 00:00:00+09:00 |  69200 |  69800 | 68800 |   69800 | 1.0283e+07  |           0 |              0 |
| 2025-09-04 00:00:00+09:00 |  69500 |  70100 | 69300 |   70100 | 1.22844e+07 |           0 |              0 |
| 2025-09-05 00:00:00+09:00 |  70300 |  70400 | 69500 |   69500 | 1.15267e+07 |           0 |              0 |
| 2025-09-08 00:00:00+09:00 |  69800 |  70500 | 69600 |   70100 | 9.26314e+06 |           0 |              0 |
| 2025-09-09 00:00:00+09:00 |  70100 |  71500 | 70000 |   71500 | 1.48702e+07 |           0 |              0 |
| 2025-09-10 00:00:00+09:00 |  71800 |  72800 | 71600 |   72600 | 2.19286e+07 |           0 |              0 |
| 2025-09-11 00:00:00+09:00 |  73200 |  73600 | 72100 |   73400 | 2.07935e+07 |           0 |              0 |
| 2025-09-12 00:00:00+09:00 |  74600 |  75600 | 74200 |   75400 | 2.82197e+07 |           0 |              0 |
| 2025-09-15 00:00:00+09:00 |  77200 |  77600 | 75900 |   76500 | 1.99088e+07 |           0 |              0 |
| 2025-09-16 00:00:00+09:00 |      0 |  78300 | 76700 |   78200 | 1.25886e+07 |           0 |              0 |
```
```python
ai_message = model_with_tools.invoke(input = messages)
```
```python
ai_message.pretty_print()
```
<img width="654" height="251" alt="image" src="https://github.com/user-attachments/assets/e6731a55-1758-4b56-b058-0ccc02de51c6" />
