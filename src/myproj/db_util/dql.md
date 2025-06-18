```python
from oracledb import DatabaseError

from src.myproj.db_util import get_connection


# dept_ex 테이블의 모든 레코드 검색
sql_select = 'select * from dept_ex order by deptno'

# sql_select를 실행하고 그 결과를 출력하는 함수
def select_dept():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_select)
                for row in cursor:
                    print(row)
            except DatabaseError as e:
                print(e)



# 부서번호로 부서 정보 검색 -> 파라미터를 갖는 sql 문장. dept_no는 sql 파라미터
sql_select_by_deptno = 'select * from dept_ex where deptno = :dept_no'  # dept_no가 변수라서 아무렇게 정해도 됨

# sql_select_by_deptno 문장을 실행하고 결과를 출력하는 함수
def select_dept_by_deptno(no):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                # 가변길이 키워드 아규먼트 방식(dept_no = no)으로 SQL 문장에 값을 설정하는 방법.
                cursor.execute(sql_select_by_deptno, dept_no = no)
                for row in cursor:
                    print(row)
            except DatabaseError as e:
                print(e)


# 부서 이름에 포함되는 문자열로 대/소문자 구분없이 검색하기
sql_select_by_dname = '''
select * from dept_ex
where upper(dname) like upper(:dept_name)
'''

# sql_select_by_dname 문장을 실행하고 결과를 출력하는 함수
def select_dept_by_dname(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                keyword = f'%{name}%'
                cursor.execute(sql_select_by_dname, dept_name = keyword)
                for row in cursor:
                    print(row)
            except DatabaseError as e:
                print(e)


if __name__ == '__main__':
    # dept_ex 테이블 전체 검색
    # select_dept()

    # dept_ex 테이블에서 부서번호로 검색하기
    dept_no = int(input('부서번호를 입력>>> '))
    select_dept_by_deptno(dept_no)

    # 부서 이름 검색
    dept_name = input('부서이름 입력>>> ')
    select_dept_by_dname(dept_name)
```
![image](https://github.com/user-attachments/assets/0c754975-90a3-43b1-b0fe-97dc89e7df2d)
