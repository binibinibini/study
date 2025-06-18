```python
import oracledb

user = 'scott'
password = 'tiger'
dsn = 'localhost/xe'

def get_connection():
    return oracledb.connect(user = user, password = password, dsn = dsn)

def close_connection(connection):
    connection.close()

if __name__ = '__main__':
    conn = get_connection()
    print('conn =', conn)
    close_connection(conn)
```
