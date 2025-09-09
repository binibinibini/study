## GPT로 이미지 설명 만들기

```python
import base64
from openai import OpenAI
from src.utils import get_openai_api_key
```
```python
 client = OpenAI(api_key = get_openai_api_key())
```

## [Lorem Picsum](https://picsum.photos) 이미지 설명 요청

