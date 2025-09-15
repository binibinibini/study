# LCEL(LangChain Expression Language)

- LangChain에서 복잡한 작업의 흐름을 간단하게 만들고 관리할 수 있는 도구
- Chain(체인): 작업의 흐름을 연결하는 것.
- LCEL를 이용하면 여러 줄로 표현해야 하는 작업 단계를 읽기 쉽게 축약할 수 있고, 스트리밍 출력 등 여러 작업을 병렬로 처리할 수 있음.



```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser   # 답변 출력
from langchain_core.prompts import ChatPromptTemplate   # 프롬프트 템플릿
```

# 출력 파서(Output Parser)

- 출력 파서: LLM이 반환하는 결과에서 원하는 형식의 데이터를 추출하는 도구.
    - 텍스트, JSON, 숫자 등 특정 형식을 처리할 수 있음.
- `StrOutputParser`: LLM이 반환하는 결과에서 텍스트(content)만 추출하는 객체.
    - `model.invoke()` 메서드의 반환 값을 `parser.invoke()` 메서드에 아규먼트로 전달하면, 답변 텍스트(content)만 추출할 수 있음.


 
```python
load_dotenv()   # api_key를 OS 환경 변수에 로딩.
```
<img width="56" height="27" alt="image" src="https://github.com/user-attachments/assets/b5d431c0-d18c-4d50-ab1a-4704f85f2e3c" />

```python
model = ChatOpenAI(model = 'gpt-4o-mini')   # LLM 모델 선택
```
```python
messages = [
    SystemMessage('너는 미녀와 야수의 미녀 역할이야. 캐릭터에 맞게 대화해줘.'),    # 인공지능에게 역할 부여
    HumanMessage('안녕하세요, 저는 가스통입니다. 저랑 저녁이나 같이 먹을까요?'),
]
```
```python
ai_message = model.invoke(input = messages)
```

`AIMessage` 객체에서 content를 직접 추출해서 화면에 출력.


```python
print(ai_message)
```
<img width="1472" height="139" alt="image" src="https://github.com/user-attachments/assets/6e7ee9a5-38ba-493b-94c3-537cb8645450" />

```python
print(ai_message.content)
```
<img width="1485" height="62" alt="image" src="https://github.com/user-attachments/assets/60d48ae8-437b-4440-8c7d-4397f685fdbc" />

```python
parser = StrOutputParser()  # Parser 객체 생성
```
```python
parser.invoke(ai_message)   # Parser에게 AIMessage를 분석해서 텍스트만 추출하고 리턴. (답변만 추출 가능)
```
<img width="1480" height="53" alt="image" src="https://github.com/user-attachments/assets/42248f89-2229-4fa6-b46b-8355a3928c27" />



체인 연산자(chain operator, `|`)


```python
chain = model | parser
```
```python
result = chain.invoke(input = message)
```
```python
print(result)
```
<img width="1350" height="36" alt="image" src="https://github.com/user-attachments/assets/faee2de4-c905-4e14-8000-9a2ba69c6a81" />

```python
result = chain.stream(input = messages)
for msg in result:
    print(msg, end = '')
```
<img width="1250" height="29" alt="image" src="https://github.com/user-attachments/assets/a3d53b8a-c193-4264-aa4b-2a6f6625c0b5" />


# Prompt Template

AI 모델을 호출(invoke)할 때 전달하는 메시지 형식이 매번 비슷할 때, 미리 템플릿을 작성해 두고 필요한 부분만 수정하면서 실행하는 방법.


```python
system_prompt = '너는 {story}에 나오는 {assistant_character}야. 역할에 맞게 사용자와 대화해줘.'
human_prompt = '안녕? 나는 {user_character}야. 오늘 시간 있으면 {activity} 같이 할까?'
prompt_template = ChatPromptTemplate([
    ('system', system_prompt),    # 문자열, 템플릿 문자열
    ('human', human_prompt),
])
# argument: ('role', prompt_message) 아이템으로 갖는 리스트
```
```python
# 프롬프트 템플릿의 {variable}의 값을 채움.
# -> ChatPromptTemplate을 메시지들(SystemMessage, HumanMessage)의 리스트(list)로 변환.
messages = prompt_template.invoke({     # key:value 로 전달
    'story': '미녀와 야수',
    'assistant_character': '벨',
    'user_character': '가스통',
    'activity': '저녁',
})
```
```python
print(messages)    # messages는 리스트 -> [SystemMessage, HumanMessage]
```
<img width="1573" height="48" alt="image" src="https://github.com/user-attachments/assets/7da21d81-39df-408c-ad62-a39234284946" />

```python
response = model.invoke(input = messages)
```
```python
print(response.content)    # content를 찾아서 출력
```
<img width="1412" height="27" alt="image" src="https://github.com/user-attachments/assets/2e4389e5-8147-4cec-b12e-4ca1ccf8bdd3" />

```python
type(response)
```
<img width="304" height="31" alt="image" src="https://github.com/user-attachments/assets/28d38fb8-5e1c-47c3-b091-719207cdd89e" />

```python
response.pretty_print()    # pretty_print() -> 헤더도 넣어주고, content만 찾아서 출력해줌
```
<img width="1419" height="75" alt="image" src="https://github.com/user-attachments/assets/ba653e2e-37b0-454f-8615-48c31dd1bf75" />

```python
messages = prompt_template.invoke({
    'story':'미녀와 야수',
    'assistant_character': '벨',
    'user_character': '야수',
    'activity': '저녁',
})
```
```python
response = model.invoke(input = messages)
```
```python
response.pretty_print()
```
<img width="784" height="81" alt="image" src="https://github.com/user-attachments/assets/f3fb3e78-4300-4308-bd24-4d1d64eae57f" />

## chain을 사용한 프롬프트 템플릿

```python
chain = prompt_template | model
```
```python
response = chain.invoke({
    'story': '배트맨',
    'assistant_character': '조커',
    'user_character': '할리 퀸',
    'activity': '은행 털기'
})
```
```python
response.pretty_print()
```
<img width="1616" height="96" alt="image" src="https://github.com/user-attachments/assets/e50099bb-6f46-452d-9a03-44526b356887" />

