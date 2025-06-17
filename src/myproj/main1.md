```python
import sys  # sys라는 모듈을 가져옴
import myutil.plus as my_plus  # 폴더(myutil) = 패키지. plus 모듈(=파일)을 가져오겠다
import myutil.minus as my_minus
import myutil2

print('main1.py __name__ =', __name__)

# __name__: 모든 파이썬 모듈(.py 파일)이 갖고 있는 특별한 변수
#    (1) 현재 파일을 실행할 때는 __name__ 변수에 '__main__' 문자열이 할당.
#    (2) 다른 파일에서 import될 때는 __name__ 변수에는 파일 이름이 할당.
#    (목적) 단독으로 실행할 코드와 import될 때 실행할 코드를 구분하기 위해서.(직접 실행할 때만 실행되는 코드를 따로 둘 수 있음)
```
```
테스트용 코드를 __name == '__main__' 아래에 넣으면,
다른 파일에서 import 할 때는 테스트 코드가 실행되지 않아서 깔끔하게 재사용 가능함!
```
