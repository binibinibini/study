from openai import OpenAI

from src.utils import get_openai_api_key

def main():
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=get_openai_api_key())

    # 무한 반복문
    while True:
        # 콘솔에서 사용자 입력을 받음
        user_input = input('사용자>>> ')

        # 만약 사용자 입력이 'exit'이면 반복문을 종료.
        if user_input == 'exit':
            break

        # 사용자의 입력을 메시지 user 역할의 content로 작성, 요청을 보냄.
        response = client.chat.completions.create(
            model = 'gpt-4o-mini',
            temperature = 0.9,
            messages=[
                { 'role': 'system', 'content': '너는 능력이 아주 뛰어난 비서야.' },
                {'role': 'user', 'content': user_input}
            ],
        )
        # 이 방식(single-turn)의 단점은 GPT가 이전의 대화 내용을 기억하지 못한다는 점.
        # 다음 질문에 대해서 이전 대화 내용의 문맥이 전혀 고려되지 못한 답변이 생성됨.
        # messages 리스트에 이전 GPT의 답변을 assistant 역할로 계속 추가하면서 채팅 요청을 보내면,
        # 이전 대화 내용을 기억하면서 문맥에 맞는 답변을 유도할 수 있음.
        # 이 문제점을 해결하는 코드는 multi_turn.py

        # GPT 답변을 출력
        print('MyGPT>>>',  response.choices[0].message.content)

if __name__ == '__main__':
    main()


```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab03\single_turn.py 
사용자>>> 참새가 뭐야
MyGPT>>> 참새는 작은 크기의 새로, 주로 도시와 농촌 지역에서 쉽게 볼 수 있는 조류입니다. 과학적으로는 '참새과(Passeridae)'에 속하며, 가장 잘 알려진 종은 집참새(Passer domesticus)입니다. 참새는 일반적으로 갈색 또는 회색의 깃털을 가지고 있으며, 짧은 날개와 튼튼한 몸체를 가지고 있습니다. 그들은 주로 곡물, 씨앗, 벌레 등을 먹으며, 사람들과 가까이 사는 경향이 있어 도시 환경에서도 자주 발견됩니다. 참새는 그들의 특유의 지저귀는 소리로도 잘 알려져 있습니다.
사용자>>> exit

종료 코드 0(으)로 완료된 프로세스
```
