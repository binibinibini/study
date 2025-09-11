### return 문을 사용하는 함수

```python
def test_1():
    for i in range(5):
        return i
```
```python
# return 문장 만나면 종료
result = test_1()
```
```python
print(result)
```
<img width="28" height="24" alt="image" src="https://github.com/user-attachments/assets/59e74f4f-e275-4747-b5c0-92e7f0d060e8" />

```python
print(type(result))
```
<img width="128" height="27" alt="image" src="https://github.com/user-attachments/assets/07c93480-b547-40ed-a0ee-a316aa80b0cb" />

```
test_1() 함수는 내부에서 반복문으로 작성되어 있지만, 한 번 리턴한 후에는 함수가 종료가 됨.
```

### yield를 사용하는 함수

```python
def my_generator():
    for i in range(5):
        yield i  # 대기하고 있다가 반복하는 과정에서 '요청 들어오면' 한 단계 실행
```
```python
result = my_generator()
```
```python
print(result)
```
<img width="437" height="30" alt="image" src="https://github.com/user-attachments/assets/2bedf915-d62b-4938-9044-256f7b09571c" />

```python
# generator 타입의 객체는 for-in 구문에서 사용할 수 있음.
for x in result:
    print(x)
```
<img width="31" height="114" alt="image" src="https://github.com/user-attachments/assets/93f0cbcc-5848-4a6e-9b5b-cf634801c24d" />

```python
# 위에서 전부 소진해서 리턴 받을 값이 없음
for x in result:
    print(x)
```
```
결과 없음
```
```python
def my_generator2():
    values = ['OpenAI', 'Google', 'Meta']
    for x in values:
        print('*' * 10)
        yield x
```
```python
result = my_generator2()
```
```python
print(result)
```
<img width="452" height="24" alt="image" src="https://github.com/user-attachments/assets/dc88d108-d73d-4377-bf50-d3f7b1425451" />

```python
for x in result:
    print(x)
```
<img width="108" height="139" alt="image" src="https://github.com/user-attachments/assets/861ec9a7-e9c8-49f7-a44c-e63f7ebd7db6" />


