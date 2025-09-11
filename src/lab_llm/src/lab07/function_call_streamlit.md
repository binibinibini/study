```python
import json
from collections import defaultdict

import streamlit as st
from openai import OpenAI

from src.lab07.gpt_functions import tools, get_current_time
from src.lab07.gpt_functions import get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from src.utils import get_openai_api_key


def mylog(msg=''):
    print(msg)
    print('-' * 100)
    print()  # 줄바꿈


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,  # GPT가 호출할 수 있는 도구 목록
        stream=True,
    )
    # stream=True로 설정한 경우, GPT 응답은 generator 패턴(반복iteration을 할 때마다 순서대로 반환)으로 작성해야 함.
    # return 대신 yield를 사용함.
    for chunk in response:
        yield chunk


def delta_tool_calls_to_obj(tools):
    tools_dict = defaultdict(lambda: {'id': None,
                                      'function': {'arguments': '', 'name': None},
                                      'type': None})
    for tool in tools:
        # function calling 아이디, 함수 이름, 타입('function')은 첫번째 청크에서만 값이 있기 때문에.
        if tool.id is not None:
            tools_dict[tool.index]['id'] = tool.id
        if tool.function.name is not None:
            tools_dict[tool.index]['function']['name'] = tool.function.name
        if tool.type is not None:
            tools_dict[tool.index]['type'] = tool.type
        # 파편화된(조각난) 아규먼트(문자열)들을 합쳐서 아규먼트 문자열을 JSON 형식으로 완성.
        tools_dict[tool.index]['function']['arguments'] += tool.function.arguments

    tools_dict_list = list(tools_dict.values())

    return {'tool_calls': tools_dict_list}


def main():
    client = OpenAI(api_key=get_openai_api_key())

    st.title('My Chatbot')  # Streamlit 앱 페이지 상단의 타이틀.

    # st.session_state: Streamlit 앱이 실행되는 동안 유지되어야 할 값들을 dict 형태로 저장하기 위한 객체.
    # session_state에 'messages' 키가 없으면 시스템 초기 메시지를 설정.
    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'system', 'content': '너는 유능한 AI 비서야.'},  # dict
        ]

    # session_state에 저장된 messages(기존의 대화 내용들)를 화면에 출력.
    for msg in st.session_state.messages:
        # 시스템 메시지는 출력하지 않고, 사용자(user)와 비서(assistant) 메시지만 화면에 출력.
        if msg['role'] in ('user', 'assistant'):
            st.chat_message(msg['role']).write(msg['content'])

    user_input = st.chat_input('무엇을 도와드릴까요?')
    if user_input:  # 사용자가 입력한 내용이 있으면
        # 사용자의 입력 내용을 session_state.messages 리스트에 추가(append)
        st.session_state.messages.append({'role': 'user', 'content': user_input})

        # 사용자의 입력 내용을 화면에 출력
        st.chat_message('user').write(user_input)

        # GPT chat.completion 요청을 보냄.
        response = get_gpt_response(client, st.session_state.messages)
        # mylog(response)  #> response: generator 객체.

        content = ''  # chunk(답변 조각) 안에 content들을 합쳐서 저장하기 위한 문자열 변수.
        delta_tool_calls = []  # ChoiceDeltaToolCall 객체들을 저장하기 위한 리스트.
        with st.chat_message('assistant').empty():  # 비어있는 assistant 채팅 메시지를 만듦.
            for chunk in response:  # generator를 iteration함.
                mylog(chunk)  #> generator는 ChatCompletionChunk 객체를 반환.
                chunk_delta = chunk.choices[0].delta  #> ChoiceDelta 객체

                delta_content = chunk_delta.content  #> str
                if delta_content:  # 답변 조각이 있으면
                    content += delta_content  # iteration을 할 때마다 그때까지 합쳐진 컨텐트를
                    st.markdown(content)  # 비어있었던 assistant 채팅 창에 마카다운 형식으로 텍스트를 채움.

                if chunk_delta.tool_calls:  # 청크에서 도구 호출이 있으면
                    delta_tool_calls.extend(chunk_delta.tool_calls)

        # 파편화된 도구 호출 목록을 합침.
        tool_obj= delta_tool_calls_to_obj(delta_tool_calls)
        mylog(tool_obj)

        tool_calls = tool_obj['tool_calls']  # function calling list
        # if tool_calls is not null:
        if tool_calls:  # GPT가 (클라이언트에서 제공한 도구 목록 중에서) 함수 호출이 필요하다고 판단했을 때
            for tool in tool_calls:
                tool_id = tool['id']
                function_name = tool['function']['name']
                arguments = json.loads(tool['function']['arguments'])  # JSON 문자열 -> dict

                # GPT에서 필요로 하는 함수를 호출해서 결과값을 반환받음.
                function_result = None
                if function_name == 'get_current_time':
                    function_result = get_current_time(arguments['timezone'])
                elif function_name == 'get_yf_stock_info':
                    function_result = get_yf_stock_info(arguments['ticker'])
                elif function_name == 'get_yf_stock_history':
                    function_result = get_yf_stock_history(arguments['ticker'], arguments['period'])
                elif function_name == 'get_yf_stock_recommendations':
                    function_result = get_yf_stock_recommendations(arguments['ticker'])

                # session_state의 messages 리스트에서 'function' 역할(role)의 메시지를 추가
                st.session_state.messages.append({
                    'role': 'function',
                    'tool_call_id': tool_id,
                    'name': function_name,
                    'content': function_result,
                })

            # 반복문(for-in)이 끝난 다음에, function 메시지들이 모두 append된 다음에,
            st.session_state.messages.append({'role': 'system', 'content': '주어진 결과를 바탕으로 답변을 생성해줘.'})

            # 함수 호출을 요청한 GPT에게 함수 호출 결과를 메시지로 보냄.
            response = get_gpt_response(client, st.session_state.messages)
            mylog(response)
            content = ''
            with st.chat_message('assistant').empty():
                for chunk in response:
                    chunk_delta = chunk.choices[0].delta
                    delta_content = chunk_delta.content
                    if delta_content:
                        content += delta_content
                        st.markdown(content)

        # assistant 메시지를 session_state의 messages 리스트에 추가
        st.session_state.messages.append({'role': 'assistant', 'content': content})


if __name__ == '__main__':
    main()
```
<img width="997" height="956" alt="image" src="https://github.com/user-attachments/assets/6861029d-990a-4a31-ae00-9ba37e93fa7f" />
