```python
from oracledb import DatabaseError

from src.myproj.db_util import get_connection

# dept_ex 테이블에 데이터(부서번호, 이름, 위치)를 insert하는 SQL 문장과 함수를 작성하세요.
sql_insert ='''
insert into dept_ex
values (:dept_no, :dept_name, :location)
'''

def insert_dept(dept_no, dept_name, location):
    # step 1. DB 연결
    with get_connection() as conn:
        # step 2. Cursor 객체 생성
        with conn.cursor() as cursor:
            # step 3. SQL 실행
            try:
                # positional arg 방식 -> list, tuple, dict
                # result = cursor.execute(sql_insert, (dept_no, dept_name, location))
                # print('insert result =', result)
                cursor.execute(sql_insert, {
                    'dept_no': dept_no,
                    'dept_name': dept_name,
                    'location': location
                })
                # 가변길이 keyword arg 방식
                # cursor.execute(sql_insert, dept_no=dept_no, dept_name=dept_name, location=location)
                conn.commit()  # DML(insert, update, delte)의 결과를 commit.
                print('insert 성공')
            except DatabaseError as e:
                print(e)

# dept_ex 테이블에서 특정 부서 번호의 이름과 위치를 업데이트하는 SQL 문장과 함수를 작성하세요.
sql_upate = '''
update dept_ex
set dname = :dept_name, loc = :location
where deptno = :dept_no
'''

def update_dept(dept_no, dept_name, location):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_upate,
                               dept_no=dept_no,
                               dept_name=dept_name,
                               location=location)
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
                cursor.execute(sql_delete, dept_no=dept_no)
                conn.commit()
                print('delete 성공')
            except DatabaseError as e:
                print(e)


if __name__ == '__main__':
    # insert 테스트
    no = int(input('부서 번호 입력>>> '))
    name = input('부서 이름 입력>>> ')
    loc = input('부서 위치 입력>>> ')
    insert_dept(no, name, loc)

    # update 테스트
    no = int(input('업데이트할 부서 번호 입력>>> '))
    name = input('업데이트할 부서 이름 입력>>> ')
    loc = input('업데이트할 부서 위치 입력>>> ')
    update_dept(no, name, loc)

    # delete 테스트
    no = int(input('삭제할 부서 번호 입력>>> '))
    delete_dept(no)
```
