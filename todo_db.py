import os
import psycopg2
import psycopg2.extras
import urllib.parse

class TodoDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createTodoTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, todo VARCHAR(255))")
        self.connection.commit()

    def createTodo(self, todo):
        self.cursor.execute('INSERT INTO todos (todo) VALUES (%s)', (todo,))
        self.connection.commit()

    def retrieveTodo(self, id):
        self.cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        rows = self.cursor.fetchone()
        return rows

    def idInDatabase(self, id):
        self.cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        rows = self.cursor.fetchall()
        # print(rows)
        if not rows:
            return False
        else:
            return True

    def getTodo(self):
        self.cursor.execute('SELECT * FROM todos')
        rows = self.cursor.fetchall()
        return rows

    def deleteTodo(self, id):
        self.cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        self.connection.commit()

    def updateTodo(self, todo, id):
        self.cursor.execute('UPDATE todos SET todo = %s WHERE id = %s', (todo, id))
        self.connection.commit()

class UserDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()


    def __del__(self):
        self.connection.close()

    def createUserTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fname VARCHAR(50), lname VARCHAR(50), email VARCHAR(50), password VARCHAR(255))")
        self.connection.commit()

    def createUser(self, fname, lname, email, password):
        self.cursor.execute('INSERT INTO users (fname, lname, email, password) VALUES (%s, %s, %s, %s)', (fname, lname, email, password))
        self.connection.commit()

    def retrieveUser(self, id):
        self.cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        rows = self.cursor.fetchone()
        return rows

    def idInDatabase(self, id):
        self.cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        rows = self.cursor.fetchall()
        # print(rows)
        if not rows:
            return False
        else:
            return True

    def emailInDatabase(self, email):
        # self.cursor.execute('SELECT * FROM users WHERE email = %s', [email])
        self.cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        rows = self.cursor.fetchone()
        print(rows)
        if not rows:
            return None
        else:
            return rows
    def passwordInDatabase(self, email):
        self.cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
        row = self.cursor.fetchone()
        return row


    def getUser(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return rows

    def deleteUser(self, id):
        self.cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        self.connection.commit()

    def updateUser(self, fname, lname, email, password, id):
        self.cursor.execute('UPDATE users SET fname = %s, lname = %s, email = %s, password = %s WHERE id = %s', (fname, lname, email, password, id))
        self.connection.commit()
