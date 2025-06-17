```python
import oracledb

user = 'scott'
password = 'tiger'
dsn = 'localhost/xe'

if __name__ == '__main__':
    # with-as 구문을 사용한 DB 접속, Cursor 사용.
    with oracledb.connect(user=user, password=password, dsn=dsn) as conn:
        # conn.close() 메서드 호출은 with-as가 끝날 때 자동으로 호출됨.
        with conn.cursor() as cursor:
            # cursor.close() 메서드 호출은 안쪽 with-as가 끝날 때 자동으로 호출됨.
            sql = 'select * from dept'
            cursor.execute(sql)
            for row in cursor:
                print(row)
```
![image](https://github.com/user-attachments/assets/3538969c-1aec-45c5-8f5e-fee151b68e49)
