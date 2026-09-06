from pymysql import connect
def connection():
    connection = connect(
        host="localhost",
        user="root",
        password="Karthik#03",
        database="lost_foundd"
    )
    return connection