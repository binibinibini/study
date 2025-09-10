# yfinance 패키지 예제

설치한 패키지 이름
```
pip install -U yfinance
```

```python
import yfinance as yf
```
```python
msft = yf.Ticker(ticker = 'MSFT')  # 마이크로소프트(Microsoft)의 Ticker 객체 생성
```


회사 - 티커
*   아마존 - AMZN
*   구글 - GOOGL
*   메타(페이스북) - META
*   삼성 - 005930.KS
*   하이닉스 - 000660.KS


```python
print(type(msft))
```
<img width="273" height="29" alt="image" src="https://github.com/user-attachments/assets/a769617d-9dae-4a6b-bd1c-f60d105d9e71" />

```python
msft.info
```
<img width="1509" height="318" alt="image" src="https://github.com/user-attachments/assets/0d15f56f-d0f1-4be9-bd74-567df53beeef" />

```python
msft.info.keys()
```
<img width="1508" height="444" alt="image" src="https://github.com/user-attachments/assets/351b9604-b478-422d-ba76-5a5feaa0b6c7" />

```python
# Ticker.history(): 주가 데이터를 반환.
# period 파라미터: '2mo': 2 months, '3y': 3 years
hist_5d = msft.history(period = '5d')   # 지난 5일 간의 주가 데이터
```
```python
print(type(hist_5d))
```
<img width="326" height="33" alt="image" src="https://github.com/user-attachments/assets/73b31982-9a36-49dd-a281-12efe8f80c7a" />

```python
hist_5d # pandas.DataFrame. 지난 5일 출력
```
<img width="755" height="235" alt="image" src="https://github.com/user-attachments/assets/d3bfc3ca-9d1e-4ae3-9070-55e7e0cd3c64" />

```python
hist_1mo = msft.history(period = '1mo')
```
```python
hist_1mo
```
<img width="140" height="32" alt="image" src="https://github.com/user-attachments/assets/e7abd543-6906-4704-a71b-05f524cea85f" />

```python
msft.recommendations    # 지난 4개월 동안의 애널리스트들의 분석(추천). -1m은 한달전, -2m은 두달전..
```
<img width="348" height="171" alt="image" src="https://github.com/user-attachments/assets/4990869a-ac33-434a-a360-8d33aedfd84d" />

```
# 강하게 추천, 주식사는거 추천, 유지, 팔아라, 강하게 팔아라고 추천
```
```python
hynix.recommendations
```
<img width="352" height="167" alt="image" src="https://github.com/user-attachments/assets/891b93aa-e00e-4567-88eb-ba34b9ed69d1" />
