from .entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, password, name, last_name, phone, address FROM users 
                     WHERE email = %s"""
            cursor.execute(sql, (user.email,))
            row = cursor.fetchone()
            if row is not None:
                if User.check_password(row[2], user.password):
                    return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, name, last_name, phone, address FROM users WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2], row[3], row[4], row[5])
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO users (email, password, name, last_name, phone, address) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            hashed_password = User.hash_password(user.password)
            cursor.execute(sql, (user.email, hashed_password, user.name, user.last_name, user.phone, user.address))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
