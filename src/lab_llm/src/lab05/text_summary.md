```python
from openai import OpenAI

from src.utils import get_openai_api_key


def file_to_txt(filename, mode = 'rt', encoding = 'utf-8'):
    """ 파일 filename을 읽어서 그 내용을 문자열로 리턴. """
    with open(filename, mode = 'rt', encoding = 'utf-8') as f:
        txt = f.read()
    return txt

def get_gpt_response(message):
    client = OpenAI(api_key = get_openai_api_key())
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        temperature=0.1,
        messages = [{'role': 'system', 'content': message}]
    )
    return response.choices[0].message.content

def write_summary(filename, summary, mode = 'wt', encoding = 'utf-8'):
    """파일 filename에 summary를 텍스트 파일로 작성."""
    with open(filename, mode = mode, encoding = encoding) as f:
        f.write(summary)    # 리턴할게 없음


def main():
    # 기사가 저장된 파일 이름과 경로
    article_file = './data/AI_article.txt'
    # GPT가 요약한 내용을 저장할 파일 이름과 경로
    article_summary_file = './output/AI_article_summary.txt'

    txt = file_to_txt(article_file)
    # print(txt)    # 제대로 읽는지 확인

    # GPT에게 요청할 요약 방법
    system_promt = f'''너는 글을 요약하는 비서야.
    아래의 글을 읽고 저자의 주장과 내용을 요약해줘.
    작성해야 하는 포맷은 다음과 같아.
    # 제목
    ## 부제목
    ## 저자의 주장(10문장 이내)
    ## 저자 소개
    
    ===== 이하 텍스트 ===
    
    {txt}
    '''

    summary = get_gpt_response(system_promt)
    print(summary)

    # 요약 내용을 파일 저장
    write_summary(article_summary_file, summary)


if __name__ == '__main__':
    main()
```
```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab05\text_summary.py 
# 인공지능, 어떻게 쓸 것인가
## 부제목
곽노건의 미래 사용설명서
## 저자의 주장
저자는 인공지능(AI)이 이미 많은 데이터를 학습하여 유용하게 활용될 수 있는 도구임을 강조한다. 직장인들은 AI를 통해 반복적인 업무를 줄이고, 더 중요한 판단과 창의적인 작업에 집중할 수 있다. 자영업자와 프리랜서도 AI를 활용하여 홍보 문구 작성, 계약서 작성, 강의 준비 등을 효율적으로 할 수 있다. 전문직 종사자들 역시 AI의 도움으로 진료 기록 정리, 판례 검색, 논문 초안 작성 등을 통해 본질적인 업무에 더 집중할 수 있다. 중요한 것은 AI와 인간의 역할을 구분하는 것이며, AI를 어떻게 활용할지를 고민해야 한다. AI는 우리의 경쟁자가 아니라, 업무의 질과 생산성을 높여주는 동료가 되어야 한다.
## 저자 소개
곽노건은 한양대학교와 동국대학교의 겸임교수이며, 비피엠지 이사로 활동하고 있다.

종료 코드 0(으)로 완료된 프로세스
```
