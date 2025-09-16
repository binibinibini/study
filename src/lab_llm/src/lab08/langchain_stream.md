```python
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.lab08.langchain_tools import tools, tool_dict
from src.lab08.langchain_tools import get_current_time, get_yf_stock_history
```
```python
load_dotenv()   # .env 파일의 api_key 정보를 환경 변수로 로딩.
```
<img width="45" height="24" alt="image" src="https://github.com/user-attachments/assets/02547550-2586-41ca-90a8-e7c7ae02aabf" />

<br>

# 한 번에 출력하기

<br>

## 언어 모델만 있는 경우
```python
model = ChatOpenAI(model = 'gpt-4o-mini')
```
```python
parser = StrOutputParser()
```
```python
chain = model | parser
```
```python
messages = [HumanMessage('한강 작가의 채식주의자를 1000자 이내로 요약해줘')]
```
```python
ai_message = chain.invoke(input = messages)
```
```python
print(ai_message)
```
<img width="1650" height="253" alt="image" src="https://github.com/user-attachments/assets/bee6b2b6-8e03-48cf-951f-0d0c2ac6179b" />

<br>

# 도구를 설정한 경우 한 번에 출력하기

<br>

```python
# AI 모델과 도구 목록을 바인딩.
model_with_tools = model.bind_tools(tools = tools)
```
```python
messages = [HumanMessage('서울, 부산, LA의 현재 시간을 비교해줘.')]
```
```python
ai_message = model_with_tools.invoke(input = messages)  # 도구를 가지고 있는 모델 호출
```
```python
ai_message.pretty_print()
```
<img width="660" height="381" alt="image" src="https://github.com/user-attachments/assets/a5ccb7e5-8f23-48af-83b0-1b6382c5e972" />

```python
messages.append(ai_message) # tool_calls를 가지고 있는 AIMessage를 대화 리스트에 추가!
```
```python
for tool_call in ai_message.tool_calls:
    print(tool_call['name'], tool_call['args'])
    fn = tool_dict[tool_call['name']]   # tool_dict.get(tool_call['name'])
    tool_msg = fn.invoke(input = tool_call) # invoke 메서드 호출 -> fn(args) 실행.
    messages.append(tool_msg)
```
<img width="648" height="74" alt="image" src="https://github.com/user-attachments/assets/28623b07-4554-43e0-abad-49fb37c8e2d2" />

```python
for m in messages:
    m.pretty_print()
```
<img width="663" height="722" alt="image" src="https://github.com/user-attachments/assets/77429b0c-8d5e-4f0c-aacf-19fbc625b408" />

```python
ai_message = model_with_tools.invoke(input = messages)
```
```python
ai_message.pretty_print()
```
<img width="659" height="215" alt="image" src="https://github.com/user-attachments/assets/b7bfcd43-0958-4546-86df-6ef2117472e5" />

<br>

# 스트리밍 방식으로 출력하기

<br>

## 언어 모델만 있는 경우 스트리밍 출력

<br>

```python
messages = [HumanMessage('한강 작가의 채식주의자를 1000자 이내로 요약해줘.')]
```
```python
response = model.stream(input = messages)
```
```python
type(response)  # generator: for-in 구문에서 반복할 때마다 어떤 값을 yield(반환)하는 객체.
```
<img width="96" height="24" alt="image" src="https://github.com/user-attachments/assets/8e30b978-828a-4d43-98f3-6785f9e4bd0c" />

```python
for r in response:
    print(r.content, end = '')
```
<img width="747" height="321" alt="image" src="https://github.com/user-attachments/assets/fca47131-7ccf-4c60-b627-824f4e32355b" />

```python
# model과 parser가 연결된 체인을 사용하는 경우
response = chain.stream(input = [HumanMessage('해리포터와 비밀의 방의 내용을 1000자 이내로 요약해줘.')])
for r in response:
    print(r, end = '')
```
<img width="750" height="429" alt="image" src="https://github.com/user-attachments/assets/764c5839-4566-4106-8f1d-49da0d33c97f" />


<br>

# 도구를 포함하는 모델의 스트리밍 출력

<br>

```python
messages = [HumanMessage('하이닉스의 지난 한 달 동안 주식 변동을 요약해줘.')]   # 질문만들기
```
```python
response = model_with_tools.stream(input = messages)    # ai에게 질문 주기
```
```python
# 파편화된 tool_calls 청크들을 하나로 합치기.
is_first = True
for chunk in response:
    print(type(chunk))  # AIMessageChunk
    if is_first:    # 첫번째 청크이면,
        is_first = False    # 다음 반복(iteration)부터는 첫번째 청크가 아니기 때문에
        gathered = chunk
    else:   # 두번째 이후 청크이면,
        gathered += chunk   # 이미 만들어진 청크의 뒤에 덧붙임(append).
    gathered.pretty_print() # 청크들이 합쳐지는 과정을 로그로 확인하기 위해서.
```
```
<결과>
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
    input: {}
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
    input: {}
<class 'langchain_core.messages.ai.AIMessageChunk'>
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
    input: {}
<class 'langchain_core.messages.ai.AIMessageChunk'> ....
```
```python
messages.append(gathered) # 하나로 합친 AI 답변을 메시지 리스트에 추가!
```
```python
# 하나로 합쳐진 tool_calls를 반복하면서 function calling을 수행.
for tool_call in gathered.tool_calls:
    fn = tool_dict.get(tool_call['name'])
    tool_msg = fn.invoke(tool_call)
    messages.append(tool_msg)   # function calling의 결과를 메시지 리스트에 추가.
```
```python
for m in messages:
    m.pretty_print()
```
```
<결과>
================================ Human Message =================================

하이닉스의 지난 한 달 동안 주식 변동을 요약해줘.
============================ Aimessagechunk Message ============================
Tool Calls:
  get_yf_stock_history (call_00dS3pAWG1jRS59ZFmLLeMV0)
 Call ID: call_00dS3pAWG1jRS59ZFmLLeMV0
  Args:
    input: {'ticker': '000660.KS', 'period': '1mo'}
================================= Tool Message =================================
Name: get_yf_stock_history

| Date                      |   Open |   High |    Low |   Close |      Volume |   Dividends |   Stock Splits |
|:--------------------------|-------:|-------:|-------:|--------:|------------:|------------:|---------------:|
| 2025-08-18 00:00:00+09:00 | 271608 | 271608 | 266615 |  267114 | 1.99322e+06 |           0 |              0 |
| 2025-08-19 00:00:00+09:00 | 268113 | 269611 | 261123 |  262621 | 1.70965e+06 |           0 |              0 |
| 2025-08-20 00:00:00+09:00 | 254133 | 256629 | 250638 |  255131 | 3.57154e+06 |           0 |              0 |
| 2025-08-21 00:00:00+09:00 | 246144 | 250638 | 244647 |  244647 | 6.30113e+06 |           0 |              0 |
| 2025-08-22 00:00:00+09:00 | 245146 | 252136 | 245146 |  250638 | 3.06406e+06 |           0 |              0 |
| 2025-08-25 00:00:00+09:00 | 255631 | 261123 | 253634 |  259126 | 3.18371e+06 |           0 |              0 |
| 2025-08-26 00:00:00+09:00 | 259126 | 262121 | 256629 |  261123 | 2.05062e+06 |           0 |              0 |
| 2025-08-27 00:00:00+09:00 | 258626 | 260624 | 255631 |  259625 | 2.80159e+06 |           0 |              0 |
| 2025-08-28 00:00:00+09:00 | 254000 | 268500 | 253000 |  268500 | 3.83602e+06 |         375 |              0 |
| 2025-08-29 00:00:00+09:00 | 268000 | 270000 | 266000 |  269000 | 1.89213e+06 |           0 |              0 |
| 2025-09-01 00:00:00+09:00 | 259500 | 261000 | 255000 |  256000 | 1.83705e+06 |           0 |              0 |
| 2025-09-02 00:00:00+09:00 | 256000 | 261500 | 256000 |  260500 | 1.58471e+06 |           0 |              0 |
| 2025-09-03 00:00:00+09:00 | 259500 | 265500 | 257750 |  262500 | 2.4379e+06  |           0 |              0 |
| 2025-09-04 00:00:00+09:00 | 267000 | 271000 | 264500 |  265500 | 2.18996e+06 |           0 |              0 |
| 2025-09-05 00:00:00+09:00 | 273000 | 275000 | 272000 |  273500 | 3.10343e+06 |           0 |              0 |
| 2025-09-08 00:00:00+09:00 | 278500 | 279000 | 274000 |  277000 | 2.0183e+06  |           0 |              0 |
| 2025-09-09 00:00:00+09:00 | 278000 | 288500 | 277000 |  288000 | 4.15834e+06 |           0 |              0 |
| 2025-09-10 00:00:00+09:00 | 294500 | 305000 | 293000 |  304000 | 5.26555e+06 |           0 |              0 |
| 2025-09-11 00:00:00+09:00 | 310000 | 315000 | 305500 |  307000 | 5.14809e+06 |           0 |              0 |
| 2025-09-12 00:00:00+09:00 | 322000 | 329500 | 319000 |  328500 | 4.24252e+06 |           0 |              0 |
| 2025-09-15 00:00:00+09:00 | 339500 | 341500 | 325000 |  331000 | 4.22126e+06 |           0 |              0 |
| 2025-09-16 00:00:00+09:00 |      0 | 354000 | 331500 |  348000 | 5.70331e+06 |           0 |              0 |
```
```python
response = model_with_tools.stream(input = messages)
```
```python
for r in response:
    print(r.content, end = '')
```
<img width="596" height="694" alt="image" src="https://github.com/user-attachments/assets/c62126ed-1d65-4c71-96fe-5b8b44c673a3" />
