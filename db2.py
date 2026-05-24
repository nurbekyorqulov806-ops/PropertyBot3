from pymysql import connect, Connection
from pymysql.cursors import DictCursor
import os

class Database:
    def __init__(self,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_host: str,
                 db_port: int
        ) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def get_connection(self) -> Connection:
        return connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=DictCursor
        )

    def execute(self, sql: str, args: tuple = (), commit = False, fetchone = False, fetchall = False):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query=sql, args=args)

        if commit:
            connection.commit()

        if fetchall and fetchone:
            raise ValueError("Fetchall va Fetchone bir vaqtda yuborilishi mumkin emas")

        if fetchone:
            return cursor.fetchone()

        if fetchall:
            return cursor.fetchall()
        
    def create_users_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id VARCHAR(100) UNIQUE NOT NULL,
                fullname VARCHAR(100) NOT NULL
            )
        """
        self.execute(sql=sql)

    def create_address_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS address(
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT  NOT NULL,
                address VARCHAR(100) NOT NULL,
                choise1 VARCHAR(100) NOT NULL,
                rooms INT NOT NULL,
                choise2 VARCHAR(100) NOT NULL,
                cost INT NOT NULL
            )
        """
        self.execute(sql=sql)



    def register_user(self, telegram_id: str, fullname: str):
        sql = f"""
            INSERT INTO users(telegram_id, fullname)
            VALUES (%s, %s)
        """
        self.execute(sql=sql, args=(telegram_id, fullname), commit=True)


    def add_datas1(self, user_id: int,address: str,choise1:str,rooms:int,choise2:str,cost:int):
        sql = """
            INSERT INTO address(user_id,address,choise1,rooms,choise2,cost)
            VALUES (%s, %s,%s,%s,%s,%s)
        """
        self.execute(sql=sql, args=(user_id,address,choise1,rooms,choise2,cost), commit=True)


    def get_user_orders(self,user_id:int):
        sql="""
            SELECT id,address,choise1,rooms,choise2,cost FROM address WHERE user_id=%s  
        """
        return self.execute(sql=sql,args=(user_id,),fetchall=True)



    def delete_user(self,user_id: str):
        sql = f"""
            DELETE FROM address WHERE user_id = %s
        """
        self.execute(sql=sql, args=(user_id,), commit=True)





db = Database(
    db_name=os.getenv("DB_NAME", "n82_bot2"),
    db_user=os.getenv("DB_USER", "root"),
    db_password=os.getenv("DB_PASSWORD", "0109"),
    db_host=os.getenv("DB_HOST", "localhost"),
    db_port=int(os.getenv("DB_PORT", 3306))
)


