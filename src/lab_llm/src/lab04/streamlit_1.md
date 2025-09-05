```
# streamlit 사용 방법 보기(터미널에 작성)
streamlit --help
```

```
<결과>
(.venv) PS C:\workspace\lab_llm> streamlit --help  
Usage: streamlit [OPTIONS] COMMAND [ARGS]...

  Try out a demo with:

      $ streamlit hello

  Or use the line below to run your own script:

      $ streamlit run your_script.py

Options:
  --log_level [error|warning|info|debug]
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  activate  Activate Streamlit by entering your email.
  cache     Manage the Streamlit cache.
  config    Manage Streamlit's config settings.
  docs      Show help in browser.
  hello     Runs the Hello World script.
  help      Print this help message.
  init      Initialize a new Streamlit project.
  run       Run a Python script, piping stderr to Streamlit.
  version   Print Streamlit's version number.
```
## 코드 작성
```python
import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title('처음 만들어 본 Streamlit')
```


### 페이지 열기
<img width="665" height="127" alt="image" src="https://github.com/user-attachments/assets/cab20421-6144-4db4-8de3-0a4b672f40da" />

```
192.168.31.11 건물을 찾을 수 있는 번호. 8501 건물에 들어갈 수 있는 번호(포트번호)
```
<img width="957" height="532" alt="image" src="https://github.com/user-attachments/assets/66c48164-f41d-4779-b8a0-6ac0bf0c878b" />

```
# 종료 코드
Ctrl + c
```



<img width="1064" height="558" alt="Image" src="https://github.com/user-attachments/assets/3538fbec-110e-48af-8f53-274a5df7d94d" />


