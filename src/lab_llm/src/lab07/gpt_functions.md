```python
from datetime import datetime
import pytz
import yfinance as yf


def get_current_time(timezone='Asia/Seoul'):
    # 시간대(timezone) 문자열을 아규먼트로 주면 timezone 클래스 객체 타입을 생성 리턴.
    tz = pytz.timezone(timezone)
    # 현재 시간 정보를 원하는 문자열 포맷으로 변환
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return f'{now} {timezone}'


def get_yf_stock_info(ticker):
    """ticker 문자열을 아규먼트로 받아서 Ticker 객체를 생성하고, 그 기업의 정보(info)를 문자열 형태로 리턴."""
    stock = yf.Ticker(ticker)   # ticker 문자열을 사용해서 Ticker 객체 생성.
    info = stock.info   # dict
    return str(info)    # dict 객체를 문자열로 변환해서 리턴.


# 주가가 어떻게 변하고 있는지 함수 만들기
def get_yf_stock_history(ticker, period):
    """ticker 문자열과 주가 정보를 조회할 period 문자열을 아규먼트로 전달받아서
    해당 기간 동안의 매일 주가 정보를 Markdown 형식의 문자열로 리턴."""
    stock = yf.Ticker(ticker)   # Ticker 객체 생성
    history = stock.history(period=period)  # 현재 시점을 기준으로 지난 period 동안의 매일 추가 DataFrame.
    return history.to_markdown()    # DataFrame을 Markdown 형식의 문자열로 변환해서 리턴.

# 추천하는지 추천하지 않은지
def get_yf_stock_recommendations(ticker):
    """ticker에 해당하는 기업의 지난 4개월간 애널리스트들의 추천(매수, 매도, 유지) 데이터를 리턴."""
    stock = yf.Ticker(ticker)   # Ticker 객체 생성
    return stock.recommendations.to_markdown()  # recommendations 데이터프레임을 Markdown 형식의 문자열로 변환해서 리턴.


# chat.completion 메시지를 요청할 때 함께 보내는 툴(도구) 리스트.
# GPT에서 필요할 때 호출할 수 있도록 선언한 도구 리스트
tools = [
    # get_current_time 정보
    {
        'type': 'function',  # 도구 타입: 함수
        'function': {
            'name': 'get_current_time',  # 함수 이름
            'description': '해당 시간대의 현재 날짜와 시간을 문자열로 리턴.',  # 함수 설명
            'parameters': {
                'type': 'object',
                'properties': {
                    'timezone': {'type': 'string',
                                 'description': '현재 날짜와 시간을 반환하기 위한 시간대(예: Asia/Seoul)'},  # timezone 파라미터
                },  # 파라미터들의 dict
                'required': ['timezone'],  # parameters.properties 중에서 필수 파라미터의 목록.
            },  # 파라미터들에 대한 설명
        }  # 함수 설명
    },

    # get_yf_stock_info 정보
    {
        'type': 'function',
        'function': {
            'name': 'get_yf_stock_info',
            'description': 'Yahoo Finance 기업 정보를 반환.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {'type': 'string',
                               'description': 'Yahoo Finance 기업 정보를 반환하기 위해 필요한 종목 ticker 문자열. (예: AAPL, AMZN)'}
                },
                'required': ['ticker'],
            }
        }
    },

    # get_yf_stock_history 정보
    {
        'type': 'function',
        'function': {
            'name': 'get_yf_stock_history',
            'description': 'Yahoo Finance에서 기업의 해당 기간 동안의 주가 정보(시가, 고가, 저가, 종가, 거래량, ...)를 반환.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {'type': 'string',
                               'description': '주가 정보를 반환하기 위한 종목의 ticker 문자열. (예: AAPL, AMZN)'},
                    'period': {'type': 'string',
                               'description': '주가 정보를 조회할 기간. (예: 1d, 5d, 1mo, 1y)'}
                },
                'required': ['ticker', 'period']
            }
        }
    },

    # get_yf_stock_recommendation 정보
    {
        'type': 'function',
        'function': {
            'name': 'get_yf_stock_recommendations',
            'description': 'Yahoo Finance의 해당 종목에 대한 애널리스트들의 추천 정보(매수, 매도, 유지, ...)를 반환.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {'type': 'string',
                               'description': '애널리스트들의 추천 정보를 조회하기 위한 종목 ticker 문자열. (예: AAPL, AMZN)'},  # timezone 파라미터
                },
                'required': ['ticker'],
            }
        }
    }
]


if __name__ == '__main__':
    # print(get_current_time())
    # print(get_current_time('Europe/London'))
    # print(get_current_time('America/New_York'))
    # print(get_current_time('America/Los_Angeles'))

    # stock_info = get_yf_stock_info('GOOGL')
    # print(stock_info)

    # stock_history = get_yf_stock_history('GOOGL','3d')
    # print(stock_history)

    stock_recommendations = get_yf_stock_recommendations('GOOGL')
    print(stock_recommendations)
```

```
<결과>
C:\workspace\lab_llm\.venv\Scripts\python.exe C:\workspace\lab_llm\src\lab07\gpt_functions.py 
2025-09-10 16:01:02 Asia/Seoul
2025-09-10 08:01:02 Europe/London
2025-09-10 03:01:02 America/New_York
2025-09-10 00:01:02 America/Los_Angeles
-----
{'address1': '1600 Amphitheatre Parkway', 'city': 'Mountain View', 'state': 'CA', 'zip': '94043', 'country': 'United States', 'phone': '650-253-0000', 'website': 'https://abc.xyz', 'industry': 'Internet Content & Information', 'industryKey': 'internet-content-information', 'industryDisp': 'Internet Content & Information', 'sector': 'Communication Services', 'sectorKey': 'communication-services', 'sectorDisp': 'Communication Services', 'longBusinessSummary': 'Alphabet Inc. offers various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America. It operates through Google Services, Google Cloud, and Other Bets segments. The Google Services segment provides products and services, including ads, Android, Chrome, devices, Gmail, Google Drive, Google Maps, Google Photos, Google Play, Search, and YouTube. It is also involved in the sale of apps and in-app purchases and digital content in the Google Play and YouTube; and devices, as well as in the provision of YouTube consumer subscription services. The Google Cloud segment offers AI infrastructure, Vertex AI platform, cybersecurity, data and analytics, and other services; Google Workspace that include cloud-based communication and collaboration tools for enterprises, such as Calendar, Gmail, Docs, Drive, and Meet; and other services for enterprise customers. The Other Bets segment sells healthcare-related and internet services. The company was incorporated in 1998 and is headquartered in Mountain View, California.', 'fullTimeEmployees': 187103, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Sundar  Pichai', 'age': 51, 'title': 'CEO & Director', 'yearBorn': 1973, 'fiscalYear': 2024, 'totalPay': 10319413, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Ruth M. Porat', 'age': 66, 'title': 'President & Chief Investment Officer', 'yearBorn': 1958, 'fiscalYear': 2024, 'totalPay': 3023363, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Dr. Lawrence Edward Page II', 'age': 51, 'title': 'Co-Founder & Director', 'yearBorn': 1973, 'fiscalYear': 2024, 'totalPay': 1, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Sergey  Brin', 'age': 50, 'title': 'Co-Founder & Director', 'yearBorn': 1974, 'fiscalYear': 2024, 'totalPay': 1, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Anat  Ashkenazi', 'age': 51, 'title': 'Senior VP & CFO', 'yearBorn': 1973, 'fiscalYear': 2024, 'totalPay': 11455556, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. J. Kent Walker', 'age': 63, 'title': 'President of Global Affairs, Chief Legal Officer & Company Secretary', 'yearBorn': 1961, 'fiscalYear': 2024, 'totalPay': 3019696, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Philipp  Schindler', 'age': 53, 'title': 'Senior Vice President & Chief Business Officer of Google', 'yearBorn': 1971, 'fiscalYear': 2024, 'totalPay': 3051699, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': "Ms. Amie Thuener O'Toole", 'age': 49, 'title': 'Corporate Controller, Chief Accounting Officer & VP', 'yearBorn': 1975, 'fiscalYear': 2024, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Ellen  West', 'title': 'Vice President of Investor Relations', 'fiscalYear': 2024, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Fiona Clare Cicconi', 'age': 58, 'title': 'Chief People Officer', 'yearBorn': 1966, 'fiscalYear': 2024, 'exercisedValue': 0, 'unexercisedValue': 0}], 'auditRisk': 7, 'boardRisk': 9, 'compensationRisk': 10, 'shareHolderRightsRisk': 10, 'overallRisk': 10, 'governanceEpochDate': 1756684800, 'compensationAsOfEpochDate': 1735603200, 'executiveTeam': [], 'maxAge': 86400, 'priceHint': 2, 'previousClose': 234.04, 'open': 234.145, 'dayLow': 233.229, 'dayHigh': 240.47, 'regularMarketPreviousClose': 234.04, 'regularMarketOpen': 234.145, 'regularMarketDayLow': 233.229, 'regularMarketDayHigh': 240.47, 'dividendRate': 0.84, 'dividendYield': 0.35, 'exDividendDate': 1757289600, 'payoutRatio': 0.0864, 'beta': 1.011, 'trailingPE': 25.574173, 'forwardPE': 26.744421, 'volume': 37262691, 'regularMarketVolume': 37262691, 'averageVolume': 38246395, 'averageVolume10days': 44317440, 'averageDailyVolume10Day': 44317440, 'bid': 239.42, 'ask': 239.75, 'bidSize': 4, 'askSize': 4, 'marketCap': 2899762741248, 'fiftyTwoWeekLow': 140.53, 'fiftyTwoWeekHigh': 240.47, 'priceToSalesTrailing12Months': 7.8076754, 'fiftyDayAverage': 197.433, 'twoHundredDayAverage': 180.04715, 'trailingAnnualDividendRate': 1.01, 'trailingAnnualDividendYield': 0.0043155015, 'currency': 'USD', 'tradeable': False, 'enterpriseValue': 2844605284352, 'profitMargins': 0.31118, 'floatShares': 10836465880, 'sharesOutstanding': 5816999936, 'sharesShort': 59170664, 'sharesShortPriorMonth': 58227546, 'sharesShortPreviousMonthDate': 1752537600, 'dateShortInterest': 1755216000, 'sharesPercentSharesOut': 0.0049, 'heldPercentInsiders': 0.0025799999, 'heldPercentInstitutions': 0.80912, 'shortRatio': 1.6, 'shortPercentOfFloat': 0.010199999, 'impliedSharesOutstanding': 12101000192, 'bookValue': 29.983, 'priceToBook': 7.9921956, 'lastFiscalYearEnd': 1735603200, 'nextFiscalYearEnd': 1767139200, 'mostRecentQuarter': 1751241600, 'earningsQuarterlyGrowth': 0.194, 'netIncomeToCommon': 115572998144, 'trailingEps': 9.37, 'forwardEps': 8.96, 'lastSplitFactor': '20:1', 'lastSplitDate': 1658102400, 'enterpriseToRevenue': 7.659, 'enterpriseToEbitda': 20.197, '52WeekChange': 0.58527386, 'SandP52WeekChange': 0.1725707, 'lastDividendValue': 0.21, 'lastDividendDate': 1757289600, 'quoteType': 'EQUITY', 'currentPrice': 239.63, 'targetHighPrice': 300.0, 'targetLowPrice': 166.0, 'targetMeanPrice': 231.48, 'targetMedianPrice': 227.5, 'recommendationMean': 1.55385, 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 50, 'totalCash': 95147999232, 'totalCashPerShare': 7.867, 'ebitda': 140840992768, 'totalDebt': 41668001792, 'quickRatio': 1.72, 'currentRatio': 1.904, 'totalRevenue': 371399000064, 'debtToEquity': 11.481, 'revenuePerShare': 30.428, 'returnOnAssets': 0.16792, 'returnOnEquity': 0.34829, 'grossProfits': 218911997952, 'freeCashflow': 49786499072, 'operatingCashflow': 133707997184, 'earningsGrowth': 0.223, 'revenueGrowth': 0.138, 'grossMargins': 0.58943003, 'ebitdaMargins': 0.37922, 'operatingMargins': 0.32429, 'financialCurrency': 'USD', 'symbol': 'GOOGL', 'language': 'en-US', 'region': 'US', 'typeDisp': 'Equity', 'quoteSourceName': 'Nasdaq Real Time Price', 'triggerable': True, 'customPriceAlertConfidence': 'HIGH', 'shortName': 'Alphabet Inc.', 'longName': 'Alphabet Inc.', 'exchange': 'NMS', 'messageBoardId': 'finmb_29096', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EDT', 'gmtOffSetMilliseconds': -14400000, 'market': 'us_market', 'esgPopulated': False, 'regularMarketChangePercent': 2.38849, 'regularMarketPrice': 239.63, 'corporateActions': [], 'postMarketTime': 1757462390, 'regularMarketTime': 1757448001, 'marketState': 'PREPRE', 'epsForward': 8.96, 'epsCurrentYear': 9.95418, 'priceEpsCurrentYear': 24.073305, 'fiftyDayAverageChange': 42.197006, 'fiftyDayAverageChangePercent': 0.21372823, 'twoHundredDayAverageChange': 59.582855, 'twoHundredDayAverageChangePercent': 0.3309292, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'averageAnalystRating': '1.6 - Buy', 'cryptoTradeable': False, 'hasPrePostMarketData': True, 'firstTradeDateMilliseconds': 1092922200000, 'postMarketChangePercent': 0.133536, 'postMarketPrice': 239.95, 'postMarketChange': 0.319992, 'regularMarketChange': 5.59001, 'regularMarketDayRange': '233.229 - 240.47', 'fullExchangeName': 'NasdaqGS', 'averageDailyVolume3Month': 38246395, 'fiftyTwoWeekLowChange': 99.100006, 'fiftyTwoWeekLowChangePercent': 0.70518756, 'fiftyTwoWeekRange': '140.53 - 240.47', 'fiftyTwoWeekHighChange': -0.83999634, 'fiftyTwoWeekHighChangePercent': -0.003493144, 'fiftyTwoWeekChangePercent': 58.527386, 'dividendDate': 1757894400, 'earningsTimestamp': 1753300800, 'earningsTimestampStart': 1753300800, 'earningsTimestampEnd': 1753300800, 'earningsCallTimestampStart': 1753302600, 'earningsCallTimestampEnd': 1753302600, 'isEarningsDateEstimate': False, 'epsTrailingTwelveMonths': 9.37, 'trailingPegRatio': 1.6302}
-----
| Date                      |    Open |    High |     Low |   Close |      Volume |   Dividends |   Stock Splits |
|:--------------------------|--------:|--------:|--------:|--------:|------------:|------------:|---------------:|
| 2025-09-05 00:00:00-04:00 | 231.993 | 235.549 | 231.693 |  234.79 | 4.65889e+07 |        0    |              0 |
| 2025-09-08 00:00:00-04:00 | 235.47  | 238.13  | 233.67  |  234.04 | 3.24747e+07 |        0.21 |              0 |
| 2025-09-09 00:00:00-04:00 | 234.17  | 240.47  | 233.23  |  239.63 | 3.80128e+07 |        0    |              0 |
-----
|    | period   |   strongBuy |   buy |   hold |   sell |   strongSell |
|---:|:---------|------------:|------:|-------:|-------:|-------------:|
|  0 | 0m       |          12 |    41 |     12 |      0 |            0 |
|  1 | -1m      |          13 |    41 |     11 |      0 |            0 |
|  2 | -2m      |          13 |    43 |     12 |      0 |            0 |
|  3 | -3m      |          15 |    42 |     12 |      0 |            0 |

종료 코드 0(으)로 완료된 프로세스
```
