import os
import sys
import logging
import vertica_python

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.captureWarnings(True)


class VerticaConnector:
    def __init__(self, connection_info):
        """ pass params to connector"""
        if "backup_server_node" not in connection_info:
            raise BaseException(
                "Error. You should specify backup_server_node list in connection_info"
            )
        elif len(connection_info["backup_server_node"]) == 0:
            raise BaseException(
                "Error. backup_server_node list has to contain at least one backup node"
            )
        if (
            "connection_load_balance" not in connection_info
            or not connection_info["connection_load_balance"]
        ):
            raise BaseException(
                "Error. You have to specify connection_load_balance=True param"
            )
        for param in ["host", "port", "user", "password", "database"]:
            if param not in connection_info:
                raise BaseException("Error. You have to specify {} param".format(param))
        self.connection_info = connection_info

    def __str__(self):
        return "VerticaConnector to {}".format(self.connection_info["database"])

    def __del__(self):
        self.cnx.close()
        logging.info("Vertica connection closed")

    def __enter__(self):
        """ point to connect """
        logging.info("Connecting to Vertica...")
        self.cnx = vertica_python.connect(**self.connection_info)
        cur = self.cnx.cursor("dict")
        cur.execute(
            "SELECT node_name, client_hostname, session_id, login_timestamp, transaction_id, client_version FROM CURRENT_SESSION"
        )
        row = cur.fetchone()
        params = []
        for key, value in row.items():
            params.append(str(key) + ": " + str(value))

        logging.info(
            "Connected to Vertica: {current_session_info}".format(
                current_session_info=", ".join(params)
            )
        )

        return self.cnx

    def __exit__(self, type, value, traceback):
        self.cnx.close()
        logging.info("Vertica connection closed")
