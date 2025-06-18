```python
from oracledb import DatabaseError
# 전체 경로 다 쓰기
from src.myproj.db_util.connect import get_connection

# '''  ''' -> 여러줄로 작성할 때 사용
sql_create_table = '''
create table dept_ex
as select * from dept
'''

def create_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_create_table)
                print('테이블 dept_ex가 생성됨.')
            except DatabaseError as e:
                print('테이블 dept_ex 생성 실패 =', e)
            # cursor.close()는 자동 호출
          # conn.close()는 자동 호출



sql_drop_table = 'drop table dept_ex'

def drop_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_drop_tqble)
                print('테이블 dept_ex가 삭제됨.')
            except DatabaseError as e:
                print(e)

if __name__ == '__main__':
    create_table()
    drop_table()
```
- create_table() 실행했을 때<br>
![image](https://github.com/user-attachments/assets/2027b65c-d939-49d4-923e-992f40414330)
- drop_table() 실행했을 때 <br>
![image](https://github.com/user-attachments/assets/2ba9aa89-8867-4ea6-b0b6-40e0584fe21d)
