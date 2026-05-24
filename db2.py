import sqlite3

class Database:
    def init(self, db_name: str) -> None:
        self.db_name = db_name
        # Jadval yaratish funksiyalarini avtomatik ishga tushiramiz
        self.create_users_table()
        self.create_address_table()

    def get_connection(self):
        connection = sqlite3.connect(self.db_name)
        # Ma'lumotlarni xuddi DictCursor kabi dict (lug'at) ko'rinishida qaytarish uchun:
        connection.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }
        return connection

    def execute(self, sql: str, args: tuple = (), commit=False, fetchone=False, fetchall=False):
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(sql, args)

            if commit:
                connection.commit()

            if fetchall and fetchone:
                raise ValueError("Fetchall va Fetchone bir vaqtda yuborilishi mumkin emas")

            if fetchone:
                return cursor.fetchone()

            if fetchall:
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Baza bilan ishlashda xatolik: {e}")
        finally:
            cursor.close()
            connection.close()
        
    def create_users_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE NOT NULL,
                fullname TEXT NOT NULL
            )
        """
        self.execute(sql=sql)

    def create_address_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS address(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                address TEXT NOT NULL,
                choise1 TEXT NOT NULL,
                rooms INTEGER NOT NULL,
                choise2 TEXT NOT NULL,
                cost INTEGER NOT NULL
            )
        """
        self.execute(sql=sql)

    def register_user(self, telegram_id: str, fullname: str):
        sql = """
            INSERT OR IGNORE INTO users(telegram_id, fullname)
            VALUES (?, ?)
        """
        self.execute(sql=sql, args=(telegram_id, fullname), commit=True)

    def add_datas1(self, user_id: int, address: str, choise1: str, rooms: int, choise2: str, cost: int):
        sql = """
            INSERT INTO address(user_id, address, choise1, rooms, choise2, cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.execute(sql=sql, args=(user_id, address, choise1, rooms, choise2, cost), commit=True)

    def get_user_orders(self, user_id: int):
        sql = """
            SELECT id, address, choise1, rooms, choise2, cost FROM address WHERE user_id = ?  
        """
        return self.execute(sql=sql, args=(user_id,), fetchall=True)

    def delete_user(self, user_id: str):
        sql = """
            DELETE FROM address WHERE user_id = ?
        """
        self.execute(sql=sql, args=(user_id,), commit=True)

# Obyekt yaratishda to'g'ridan-to'g'ri nomini beramiz
db = Database(db_name="database.db")