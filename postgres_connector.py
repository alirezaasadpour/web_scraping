import psycopg2

class PostgreSQLConnector:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to the database!")
        except Exception as e:
            print(f"Error: Unable to connect to the database.\n{e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Error: Not connected to the database.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error executing query:\n{e}")
            return None
