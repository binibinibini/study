```python
import streamlit as st

def main():
    st.title('Sidebar와 2개 패널을 갖는 앱')

    # 웹 페이지의 사이드바에 selectbox를 추가.
    select_box = st.sidebar.selectbox(
        '선택하세요...',
        ('이메일', '전화번호', '팩스')
    )

    # 사이드바에 slider를 추가.
    slider = st.sidbar.slider(
        '범위를 선택하세요',
        0, 100, (0, 50)
    )

    # 메인 페이지 영역을 2개의 컬럼으로 나눔.
    left, right = st.columns(2)

    # 컬럼에 요소를 추가하는 방법 1: 왼쪽 컬럼에 버튼을 추가.
    left.button('클릭하세요!')

    # 컬럼에 요소를 추가하는 방법 2: with 구문 사용
    with right:
        # 오른쪽 컬럼에 라디오버튼을 추가.
        choice = st.radio(
            '선택하세요.',
            ('인*', '너튜브', '까톡')
        )
        st.write(f'{choice} 중독자')

if __name__ == '__main__':
    main()
```

<img width="623" height="120" alt="image" src="https://github.com/user-attachments/assets/be272eb6-1a4c-4c7c-bc60-ad94b27abf5b" />




<img width="1066" height="461" alt="image" src="https://github.com/user-attachments/assets/f7490112-f184-4bb9-a14e-41951dc9c9b1" />
