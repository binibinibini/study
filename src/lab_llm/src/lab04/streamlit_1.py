# streamlit 사용 방법 보기(터미널에 작성)
streamlit --help

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

# 페이지 열기
streamlit run ./src/lab04/streamlit_1.py

```
<결과>
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.31.11:8501
```

# 192.168.31.11 건물을 찾을 수 있는 번호. 8501 건물에 들어갈 수 있는 번호(포트번호)


# 사이드와 두개의 패널을 갖는 사이트
streamlit run ./src/lab04/streamlit_2.py





<img width="1064" height="558" alt="Image" src="https://github.com/user-attachments/assets/3538fbec-110e-48af-8f53-274a5df7d94d" />


