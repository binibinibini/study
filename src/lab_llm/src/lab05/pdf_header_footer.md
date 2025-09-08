## PDF 잘라서 텍스트 추출
<img width="644" height="447" alt="image" src="https://github.com/user-attachments/assets/9f5c74ff-8518-46a4-9a82-7691ab7d07ed" />

```python
import pymupdf

def main()
    pdf_file = './data/sample.pdf'  # PDF 파일 경로
    txt_file = './output/sample_2.txt'  # 추출한 텍스트를 저장할 파일 경로

    with pymupdf.open(pdf_file) as document:
        full_text = ''  # PDF 파일에서 추출한 텍스트를 저장하기 위한 변수.
        header_height = 80  # PDF 파일 헤더의 높이(세로 길이)
        footer_height = 80  # PDF 파일 푸터의 높이(세로 길이)
        for page in document:
            rect = page.rect  # 페이지의 크기(왼쪽 상단 좌표, 오른쪽 하단의 좌표, width, height, ...)
            # PDF 파일에서 잘라낼 영역, 텍스트를 추출할 영역.
            clip = (0, header_height, rect.width, rect.height - footer_height)
            # 잘려진 영역에서 텍스트를 추출
            text = page.get_text(clip = clip)
            # 추출한 텍스트를 full_text에 추가(append)
            full_text += text
            full_text += '\n\n' + '-' * 50 + '\n\n' # 페이지를 구분하기 위해서

        # 추출한 텍스트를 파일에 저장
                with open(file = txt_file, mode = 'wt', encoding = 'utf-8') as f:
            f.write(full_text)


if __name__ == '__main__':
    main()
```
<img width="798" height="76" alt="image" src="https://github.com/user-attachments/assets/9be6435e-4202-44c8-83c1-82d20ad949f2" />


```
(0,0) .----------------------------------. (rect.width, 0)
      |                                  |
      |             Header (높이: header_height)   |
      |                                  |
      .----------------------------------. (rect.width, header_height)
      |                                  |
      |                                  |
      |          본문 텍스트 추출 영역           |
      |                                  |
      |                                  |
      .----------------------------------. (rect.width, rect.height - footer_height)
      |                                  |
      |            Footer (높이: footer_height)   |
      |                                  |
(0, rect.height) '----------------------------------' (rect.width, rect.height)
```
