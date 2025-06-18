```python
from src.myproj.db_util import get_connection
from oracledb import DatabaseError

# dept_ex 테이블에 데이터(부서번호, 이름, 위치)를 insert하는 SQL 문장과 함수를 작성하세요
sql_insert = '''
insert into dept_ex (deptno, dname, loc)
values (:dept_no, :dept_name, :location)
'''

def insert_table(dept_no, dept_name, location):
    # step 1. DB 연결
    with get_connection() as conn:
        # step 2. Cursor 객체 생성
        with conn.cursor() as cursor:
            # step 3. SQL 실행
            try:
                # positional arg 방식 -> list, tuple, dict

                # 튜플로 넣기
                cursor.execute(sql_insert, (dept_no, dept_name, location))

                # dic로 넣기
                cursor.execute(sql_insert, {
                    'dept_no':dept_no,
                    'dept_name':dept_name,
                    'location':location
                })

                # 가변길이 keyword arg 방식
                # cursor.execute(sql_insert, dept_no = dept_no, dept_name = dept_name, location = location)
                conn.commit()  # DML(insert, update, delete)의 결과를 저장. conn 객체가 commit을 가지고 있음
                print('테이블 삽입됨')
            except DatabaseError as e:
                print(e)


# dept_ex 테이블에서 특정 부서 번호의 이름과 위치를 업데이트하는 SQL 문장과 함수를 작성하세요.
sql_update = '''
update dept_ex
set dname = :dept_name, loc = :location
where deptno = :dept_no
'''

def update_dept(dept_no, dept_name, location):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_update,
                              dept_no = dept_no,
                              dept_name = dept_name,
                              location = location)
                conn.commit()
                print('update 성공')
            except DatabaseError as e:
                print(e)



# dept_ex 테이블에서 특정 부서 번호의 데이터를 삭제하는 SQL 문장과 함수를 작성하세요.
sql_delete = '''
delete from dept_ex
where deptno = :dept_no
'''

def delete_dept(dept_no):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_delete, dept_no = dept_no)
                conn.commit()
                print('delete 성공')
            except DatabaseError as e:
                print(e)


if __name__ == '__main__':
    # 위에서 선언한 함수들 테스트
    # insert 테스트
    no = int(input('부서 번호 입력>>> '))
    name = input('부서 이름 입력>>> ')
    loc = input('부서 위치 입력>>> ')
    insert_table(no, name, loc)

    # update 테스트
    no = int(input('부서번호 입력>>> '))
    name = input('부서이름 입력>>> ')
    loc = input('위치 입력>>> ')
    update_dept(no, name, loc)

    # delete 테스트
    no = int(input('삭제할 부서 번호 입력>>> '))
    delete_dept(no)
```

- insert<br>
![image](https://github.com/user-attachments/assets/3838e7d1-005d-404f-a3f3-b418b4ec1de6)
<br>
- 결과<br>
![스크린샷 2025-06-18 190755](https://github.com/user-attachments/assets/123df188-f465-4974-9573-d14ad21719a2)
<br>
- update<br>
![image](https://github.com/user-attachments/assets/72db1607-8cda-4a99-ad01-0bd6e1ed1fbd)
<br>
결과<br>
![image](https://github.com/user-attachments/assets/78de55a3-78e1-4fd7-a05d-2a2b107d56dc)
<br>
- delete<br>
![image](https://github.com/user-attachments/assets/e5f3e2f9-9cfd-4ba6-ba20-2ea76cb71d00)
<br>
결과<br>
![image](https://github.com/user-attachments/assets/5a5cfc4d-c469-46cc-9b54-220e268e007c)
<br>
![image](https://github.com/user-attachments/assets/4a5da4d5-b76e-4f2d-b802-ef0b50982489)
