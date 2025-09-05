import streamlit as st

def main():
  st.title('챗봇 테스트')

  messages = [
      {'role': 'user', 'content': '무엇을 도와드릴까요?}
  ]

  for msg in messages:
      st.chat_message(msg['role']).write(msg['content'])

  user_input = st.chat_input
