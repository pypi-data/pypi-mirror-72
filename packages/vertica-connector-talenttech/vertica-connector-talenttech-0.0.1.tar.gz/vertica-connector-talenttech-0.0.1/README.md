Customized vertica connector 
==========

The Python Wrapper to vertica_python lib for reconnectiong across server nodes

Credentials
-------------
```sh
connection_info = {'host': os.getenv("VERTICA_HOST"),
                   'port': os.getenv("VERTICA_PORT"),
                   'user': os.getenv("VERTICA_USER_),
                   'password': os.getenv("VERTICA_PASSWORD"),
                   'database': os.getenv("VERTICA_DATABASE"),
                   'connection_load_balance': True,
                   'backup_server_node': ['vertica-db-1', 'vertica-db-2', 'vertica-db-3']
                  }
```

Usage
```sh
vertica-connector-talenttech
```

```python
from vconnector.vertica_connector import VerticaConnector
with VerticaConnector(connection_info) as cnx:
      cur = cnx.cursor()
      sql = "SELECT 1"
      cur.execute(sql)
