# from .connect import get_connection
# from .connect import close_connection

# from .connect import *  # 모든거 import. 변수도 다 들고옴

from src.myproj.db_util.connect import get_connection, close_connection
from src.myproj.db_util.ddl import create_table, drop_table
from src.myproj.db_util.dql import select_dept,sql_select_by_deptno,select_dept_by_dname
from src.myproj.db_util.dml import insert_table,update_dept, delete_dept
