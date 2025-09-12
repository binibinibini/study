# LangChain 소개

- LLM에 기반한 AI 앱(에이전트)를 쉽게 개발할 수 있도록 도와주는 프레임워크
- 적은 코드 수정으로 다른 LLM 모델들을 쉽게 교체할 수 있다.
    - 구글 Gemini, 메타 Llama, 앤트로픽 Claude, Deepseek와 같은 모델들은 OpenAI GPT와 사용방식이 달라서, 다른 언어 모델로 변경하려면 코드 전반을 수정해야 함.
    - LangChain을 사용하면 LLM 선언 부분만 수정해서 다른 모델로 쉽게 교체할 수 있음.
    - 특정 LLM에 종속되지 않고 다양한 모델의 장점을 활용하는 앱을 개발할 수 있음.
- LangChain에서 미리 구축된 모듈들을 활용해서 개발 속도를 높일 수 있음.


```python
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
```
```python
dotenv.load_dotenv()    # .env 파일에 작성된 키-값을 OS 환경변수로 로딩.(자동으로 api를 읽음)
```
<img width="60" height="33" alt="image" src="https://github.com/user-attachments/assets/0f1c730f-ccbf-4066-af7e-c85a4a9b92d3" />

```python
# 모델 이름 설정
model = ChatOpenAI(model = 'gpt-4o-mini')   # ChatOpenAI 객체를 생성
# LangChain의 ChatOpenAI 클래스는 OS 환경변수에 로딩된 api_key 값을 스스로 찾음.
```
```python
response = model.invoke([HumanMessage(content = '안녕 난 오쌤이야. 넌 누구니?')])
# OpenAI를 사용할 때 {'role': 'user', 'content': 'user messages...'}와 비숫.
# model.invoke(): OpenAI의 client.chat.completions.create() 메서드 호출.
```
```python
print(type(response))   # AIMessage
```
<img width="387" height="36" alt="image" src="https://github.com/user-attachments/assets/a78ccd21-02d1-4f75-a78e-cc41abd81bc7" />

```python
print(response)
# content만 출력하면 간단한 채팅이 됨
```
<img width="1480" height="140" alt="image" src="https://github.com/user-attachments/assets/0d0e7932-20d3-4326-94eb-d0e599ed93b1" />

```python
response = model.invoke([HumanMessage(content = '내 이름은 뭐야?')])
```
```python
print(response.content)
```
<img width="778" height="32" alt="image" src="https://github.com/user-attachments/assets/f91b85d0-8f40-4e1d-a9c3-d2c371479add" />


LLM이 대화 내용을 기억하면서 문맥에 맞게 답변을 생성하도록 유도하려면 이전의 대화 내용들을 list와 같은 형식으로 계속 추가하면서 요청을 보내야 됨.



```python
messages = [HumanMessage('난 오쌤이야. 넌 누구니?')] # 초기 메시지
```
```python
ai_message = model.invoke(messages) # 대화 시작
```
```python
print(ai_message.content)   # 첫 번째 AI 응답 출력
```
<img width="927" height="35" alt="image" src="https://github.com/user-attachments/assets/7720922b-a43f-46cd-8f2e-08512bb5eed0" />

```python
messages.append(ai_message) # 메시지 리스트에 AIMessage 객체를 추가.
```
```python
messages.append(HumanMessage(content = '내 이름은 뭐야?'))    # 사용자 두번째 질문
```
```python
ai_message = model.invoke(messages)
```
```python
print(ai_message.content)
```
<img width="634" height="33" alt="image" src="https://github.com/user-attachments/assets/e81a740a-7e9c-406f-9009-d6ff80c11ca4" />

