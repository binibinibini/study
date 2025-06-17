```python
import oracledb  # oracledb 설치 되어있어야 함

# 접속할 때 이 세가지 있어야 함
user = 'scott'  # DB 접속 사용자 아이디
password = 'tiger'  # DB 접속 비밀번호
dsn = 'localhost/xe'  # DB 서버 정보(주소, SID)

if __name__ == '__main__':
    print('oracledb version =', oracledb.__version__)  # oracledb에 __version__라는 변수가 있음

    # Oracle DB에 접속. 성공하면 conn 객체가 생성됨(DB 연결된 상태)
    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    print(conn)  # 접속 성공 여부 확인용으로 출력

    sql = 'select * from emp'  # DB에서 실행할 SQL 문장 - 끝에 세미콜론을 사용하면 안됨(자동으로 붙여준다고 생각하면 됨)

    # Cursor 객체: DB에 SQL 문장을 전송/실행, 그 결과처리를 할 수 있는 객체.
    cursor = conn.cursor()  # DB에 연결되어 있어야 cursor 객체를 만들 수 있음
    print('cursor =', cursor)  # 커서 객체가 잘 만들어졌는지 출력

    result = cursor.execute(sql)  # (cursor가 있으면)SQL 문장 실행.
    print('result =', result)
    # Cursor 객체는 iterable 타입 -> for-in 반복문에서 사용할 수 있음.
    # row: select 결과에서 1개 행에 저장된 값들로 이루어진 tuple.
    for row in cursor:
        print(row)

    cursor.close()  # 사용이 모두 끝난 커서 객체는 반드시 닫아야 함.
    print('커서 해제 성공')

    # DB 접속 해제.
    conn.close()
    print('DB 접속 해제 성공')
```
![image](https://github.com/user-attachments/assets/541d3fec-cb2d-4a30-a89b-94f7d8ee5211)
![image](https://github.com/user-attachments/assets/b05735eb-b9ce-4679-b333-f9ad4763d2df)
<br>
![image](https://github.com/user-attachments/assets/a55b39d0-e3d0-46df-99bf-7d4c157c70de)
<br>
```python
for row in cursor:
        print(row)
```
![image](https://github.com/user-attachments/assets/b337dfcd-0e1e-416d-be77-fba301181ec3)
