# Decorator 디자인 패턴

```python
def hello():
    print('--- hello 시작 ---')   # 로그 기능
    print('안녕...')  # hello 함수의 주된 기능
    print('--- hello 종료 ---')   # 로그 기능
```
```python
hello()
```
<img width="163" height="77" alt="image" src="https://github.com/user-attachments/assets/c91867c4-0d0a-4179-a060-86a362f90e5f" />

```python
def world():
    print('--- world 시작 ---')
    print('World...')
    print('--- world 종료 ---')
```
```python
world()
```
<img width="163" height="75" alt="image" src="https://github.com/user-attachments/assets/4c0b6537-21a4-489b-8f67-d1b8d0fb693b" />

```
hello() 함수와 world() 함수는 주된 기능만을 작성, 부가적인 기능(로깅, 아규먼트 검사, ...)들은 공통으로 작성하는 기법.
```

```python
def trace(func):
    # 지역 함수(local function) 선언
    def wrapper():
        print(f'===== {func.__name__} =====')   # 함수의 이름을 리턴해주는 __name__ 속성
        func()  # trace 함수의 아규먼트인 함수 func를 실행.
        print(f'===== {func.__name__} 종료 =====')
        # 여기까지 지역함수

    return wrapper  # 지역 함수 "객체"를 리턴.
```
```python
def hello():
    print('안녕...')
```
```python
def world():
    print('World...')
```
```python
hello_trace = tracee(hello)  # hello를 아규먼트로
```
```python
type(hello_trace)
```
<img width="81" height="24" alt="image" src="https://github.com/user-attachments/assets/ef76b691-159a-4211-9ce6-6c1fd90a22aa" />

```python
hello_trace()
```
<img width="194" height="66" alt="image" src="https://github.com/user-attachments/assets/3df1979d-6320-4143-85ec-482871c55662" />

```python
world_trace = trace(world)
world_trace()
```
<img width="186" height="68" alt="image" src="https://github.com/user-attachments/assets/e22abb96-e274-4572-84c0-bd577a179019" />

```
trace() 함수를 데코레이터(decorator) 함수라고 함.

`@decorator` 애너테이션을 호출하고자 하는 함수 선언 부분에 사용하면 더 편리하게 이용할 수 있음.
```

```python
def hello2():
    print('hello2...')
```
```python
hello2()
```
<img width="94" height="27" alt="image" src="https://github.com/user-attachments/assets/2a6c1ede-44d8-407c-8ca9-30f015d56709" />

```python
@trace
def hello2():
    print('hello2...')
```
```python
hello2()
```
<img width="198" height="67" alt="image" src="https://github.com/user-attachments/assets/aac4e68c-370c-4209-820d-29023bef9553" />

```python
@trace
def world2():
    print('world2...')
```
```python
world2()
```
<img width="196" height="68" alt="image" src="https://github.com/user-attachments/assets/0423b72b-3e62-432a-aa82-26d49c78a8f2" />


```
함수에 데코레이터를 여러 개 지정할 수도 있음.
```

```python
def deco1(func):
    def wrapper():
        print('--- deco1 시작 ---')
        func()
        print('--- deco1 종료 ---')
    return wrapper  # ()를 쓰면 함수를 호출하는거라서 return이 없어 None이 출력됨
```
```python
def deco2(func):
    def wrapper():
        print('--- deco2 시작 ---')
        func()
        print('--- deco2 종료 ---')
    return wrapper
```
```python
@deco1
@deco2
def hello_world():
    print('Hello, world!')

# hello_world()가 deco2에 들어가고, deco2가 deco1에 들어감
```
```python
hello_world()
```
<img width="162" height="121" alt="image" src="https://github.com/user-attachments/assets/9818a8bc-61dd-4872-9337-fc9a718da71c" />

<br>

<img width="460" height="477" alt="image" src="https://github.com/user-attachments/assets/4d4ef58e-1e56-42e9-b496-1cb6b5700da8" />


# 파라미터와 반환값을 처리하는 데코레이터

```python
def add(x, y):
    return x + y
```
```python
def trace(func):    # 데코레이터에서 호출할 함수를 아규먼트로 전달받음
    def wrapper(x, y):    # 호출할 함수 func()과 동일하게 파라미터들을 선언.
        r = func(x, y)    # 함수 func에게 파라미터 x와 y를 아규먼트로 전달하면서 호출.
        print(f'{func.__name__}(x = {x}, y = {y} -> {r})')
        return r    # func의 리턴 값을 반환.
    return wrapper
```
```python
@trace
def add(x, y):  # add 함수가 trace로 들어감
    return x + y
```
```python
result = add(1, 2)
```
<img width="191" height="25" alt="image" src="https://github.com/user-attachments/assets/545ca766-7da3-47fd-9af5-215902885070" />

```python
print(result)
```
<img width="25" height="22" alt="image" src="https://github.com/user-attachments/assets/9d353b28-9565-4a2f-8f58-9baa7c1ab29d" />

```python
@trace
def subtract(x, y):
    return x - y
```
```python
result = subtract(1, 2)
```
<img width="242" height="25" alt="image" src="https://github.com/user-attachments/assets/1750a674-df7b-4ca5-b656-77647937722b" />

```python
print(result)
```
<img width="28" height="24" alt="image" src="https://github.com/user-attachments/assets/7438e84d-087b-4d38-b1c9-9b04989ec85d" />


## 가변길이 인수 함수 데코레이터


```python
def trace(func):  # 실제로 호출할 함수를 아규먼트로 전달받음
    # 가변길이 함수는 *, 가변길이 키워드는 **. 언패킹연산자가 아니라 가변길이라고 선언해준거
    def wrapper(*args, **kwargs):  # 가변길이 인수로 파라미터를 선언.
        # func에는 함수를 호출하는거니깐 언패킹연산자
        r = func(*args, **kwargs)  # 함수 func에게 args와 kwargs를 "unpacking"해서 아규먼트로 전달.
        print(f'{func.__name__}(args = {args}, kwargs = {kwargs}) -> {r}')
        return r
    return wrapper
```
```python
@trace
def get_max(*args):  # 가변길이가 전달되어야 함
    return max(args)
```
```python
result = get_max(10, 20, 0, 1, 100, 55)
```
<img width="495" height="26" alt="image" src="https://github.com/user-attachments/assets/582b22c2-0ac3-48d9-9913-e6bed6680bcd" />

```python
print(result)
```
<img width="41" height="22" alt="image" src="https://github.com/user-attachments/assets/66391606-a8c8-4969-9550-e20e72ee589f" />

```python
result = get_max(1, 10, -1)
```
<img width="387" height="28" alt="image" src="https://github.com/user-attachments/assets/9b6c6efc-b6cb-41fe-af36-a2c1a2ff6f20" />

```python
print(result)
```
<img width="34" height="25" alt="image" src="https://github.com/user-attachments/assets/5d844776-18a2-4c67-b2a6-36c997b3b242" />


## unpacking 연산자


```python
def add_three_number(x, y, z):
    return x + y + z
```
```python
add_three_number(1, 2, 3)
```
<img width="23" height="26" alt="image" src="https://github.com/user-attachments/assets/67bb2886-0bb2-424a-9b43-428e1fbec377" />

```python
try:
    r = add_three_number((1, 2, 3))  # 튜플 한개를 아규먼트로 넣은거
    print(r)
except Exception as e:
    print(e)
```
<img width="579" height="30" alt="image" src="https://github.com/user-attachments/assets/314a0996-8909-494b-9d5c-6e1255611794" />

```python
try:
    r = add_three_number(*(1, 2, 3))  # *(1, 2, 3) -> 1, 2, 3  <언패킹 연산자> 3개의 값을 아규먼트로 넣은거
    print(r)
except Exception as e:
    print(e)
```
<img width="25" height="24" alt="image" src="https://github.com/user-attachments/assets/e9246ad2-e3ff-4099-ab09-a43f49802e1a" />

```python
def print_info(name, age):
    print(f'이름: {name}, 나이: {age}')
```
```python
print_info(name = '오쌤', age = 16)
```
<img width="164" height="28" alt="image" src="https://github.com/user-attachments/assets/c3195aae-8fb9-45a4-a5f8-c7629fbdb2e9" />

```python
try:
    print_info({'name': '홍길동', 'age': 20})  # dict를 name에 주는거라서 age에는 들어가는게 없음.
except Exception as e:
    print(e)
```
<img width="481" height="33" alt="image" src="https://github.com/user-attachments/assets/d97ef96b-89e7-4b92-bc9b-642d159c6977" />

```python
try:
    print_info(**{'name': '홍길동', 'age': 20})
    # unpacking 연산자: **{key1: value1, key2: value2} -> key1 = value1, key2 = value2
except Exception as e:
    print(e)
```
<img width="175" height="29" alt="image" src="https://github.com/user-attachments/assets/0ecb2b8a-6171-43ea-86cc-631789ddca05" />


# 파라미터를 갖는 데코레이터 작성


```python
def is_multiple(n): # 파라미터를 갖는 데코레이터
    def decorator(func):    # 호출할 함수를 아규먼트로 전달받음.
        def wrapper(x, y):  # 파라미터, x, y - 호출할 함수 func의 아규먼트로 사용.
            r = func(x, y)
            print(f'{func.__name__}(x = {x}, y = {y}) -> {r}')
            if r % n == 0:
                print(f'{func.__name__}의 리턴 값은 {n}의 배수입니다.')
            else:
                print(f'{func.__name__}의 리턴 값은 {n}의 배수가 아닙니다.')
            return r

        return wrapper

    return decorator     
```
```python
@is_multiple(2)
def add(x, y):
    return x + y
```
```python
result = add(1, 2)
```
<img width="262" height="46" alt="image" src="https://github.com/user-attachments/assets/b6ccf47c-3c4e-432f-835b-95e0a4f000d5" />

```python
result = add(10, 20)
```
<img width="231" height="52" alt="image" src="https://github.com/user-attachments/assets/157a5216-c568-4632-9656-e7a6dfbc0bab" />

```python
print(result)
```
<img width="34" height="22" alt="image" src="https://github.com/user-attachments/assets/8d00892b-57f1-4465-88d8-ec100abc4abd" />

```python
@is_multiple(3)
def subtract(x, y):
    return x - y
```
```python
result = subtract(10, 1)
```
<img width="268" height="52" alt="image" src="https://github.com/user-attachments/assets/42bd725b-5616-43bb-ae83-09a31558058b" />

```python
print(result)
```
<img width="30" height="29" alt="image" src="https://github.com/user-attachments/assets/f44831ca-b537-4407-8842-b4eef9bbd88a" />

```python
@is_multiple(2)
@is_multiple(3)
def add(x, y):
    return x + y
```
```python
result = add(2, 4)
```
<img width="264" height="93" alt="image" src="https://github.com/user-attachments/assets/c4629203-9526-4fde-bd13-5e9d07a54229" />


```
데코레이터(`@decorator`)를 여러 개 사용하면 데코레이터에서 반환된 wrapper 함수가 다른 데코레이터의 아규먼트로 전달됨. 그래서 두번째 데코레이터에서 `__name__` 속성의 값은 `wrapper`가 됨.

처음에 전달된 함수 이름을 그대로 출력하고 싶을 때 `functools` 모듈의 `wraps` 데코레이터를 사용하면 됨.
```

```python
import functools
```
```python
def is_multiple(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(x, y):  # x, y는 func이 쓰기 위한 아규먼트들
            r = func(x, y)
            print(f'{func.__name__}(x = {x}, y = {y}) -> {r}')
            if r % n == 0:
                print(f'{func.__name__}의 리턴 값은 {n}의 배수입니다.')
            else:
                print(f'{func.__name__}의 리턴 값은 {n}의 배수가 아닙니다.')

            return r

        return wrapper

    return decorator
```
```python
@is_multiple(2)
@is_multiple(3)
def subtract(x, y):
    return x - y
```
```python
result = subtract(10, 1)
```
<img width="307" height="96" alt="image" src="https://github.com/user-attachments/assets/ed14b0c7-a098-4a3c-a944-ff1d1a2fac2a" />

# 클래스로 데코레이터 작성

```python
class Square:
    def __init__(self):
        print('Square 객체 생성됨.')
    def __call__(self, n):
        return n ** 2
```
```python
square = Square()  # 생성자 호출 -> __init__ 메서드 호출
```
<img width="150" height="27" alt="image" src="https://github.com/user-attachments/assets/f7479e85-25d5-4087-b25d-2d6e41ed48d4" />

```python
square(3)  # 인스턴스를 함수처럼 호출 -> __call__ 메서드 호출
```
<img width="32" height="23" alt="image" src="https://github.com/user-attachments/assets/180ce3ca-f5fd-407a-b4b0-4ce0d756bbf8" />

```python
class Trace:
    def __init__(self, func):   # 호출할 함수를 아규먼트로 전달받음.
        self.func = func

    def __call__(self, *args):  # 데코레이터 함수에서 지역 함수 wrapper가 해야할 일.
        print(f'=== {self.func.__name__} 시작 ===')
        r = self.func(*args)    # *: unpacking 연산자
        print(f'{self.func.__name__}(args = {args} -> {r}')
        print(f'=== {self.func.__name__} 종료 ===')

        return r
```
```python
def multiply(x, y):
    return x * y
```
```python
trace = Trace(multiply)
```
```python
result = trace(2, 3)
```
<img width="234" height="68" alt="image" src="https://github.com/user-attachments/assets/a38a1d0b-f2b4-4796-a5f5-a17483f5f5c2" />

```python
print(result)
```
<img width="22" height="23" alt="image" src="https://github.com/user-attachments/assets/99cd1579-db6e-4f7e-b907-e567a07698a2" />

```python
@Trace
def divide(x, y):
    return x / y
```
```python
result = divide(1, 2)
```
<img width="235" height="74" alt="image" src="https://github.com/user-attachments/assets/1374a5da-c239-465a-97db-dbb9a95ac1aa" />

```python
print(result)
```
<img width="38" height="24" alt="image" src="https://github.com/user-attachments/assets/1c5047f7-5eb4-4791-9c7b-8439403ed788" />

