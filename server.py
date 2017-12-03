import sys
from http import cookies
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from todo_db import TodoDB, UserDB
from passlib.hash import bcrypt
from session_store import SessionStore

gSessionStore = SessionStore()

class MyServerHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        # add standard headers
        self.send_cookie() # send all cookie values to client
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        return

    def do_GET(self):
        self.load_session() # self.session is now ready
        todos_db = TodoDB()
        users_db = UserDB()
        print("GET path:", self.path) # if 'userId' not in self.session: self.handle401 return # else:
        if self.path.startswith("/todos/"):
            if 'userId' in self.session:
                splitPath = self.path.split("/")#check to see if id in self.session if not return 401 if true go on
                if len(splitPath) >= 3 and splitPath[1] == 'todos':
                    id = int(splitPath[2])
                    if not todos_db.idInDatabase(id):
                        self.handle404()
                    # elif 'userId' not in self.session:
                    #     self.handle401()
                    else:
                        self.handleTodoRetrieve(id)
            else:
                self.handle401()
        elif self.path.startswith("/users/"):
            # if 'userId' in self.session:
            splitPath = self.path.split("/")#check to see if id in self.session#if not return 401#if true go on
            if len(splitPath) >= 3 and splitPath[1] == 'users':
                id = int(splitPath[2])# if userId not in self.session:#     self.handle401()# return
                if not users_db.idInDatabase(id):
                    self.handle404()
                # elif 'userId' not in self.session:
                #     self.handle401()
                else:
                    self.handleUserRetrieve(id)
            else:
                self.handle401()
        elif self.path.startswith("/todos"):# if userId not in self.session:#self.handle401#return
            if 'userId' not in self.session:
                self.handle401()
                return
            self.handleTodoList()
        elif self.path.startswith("/users"):
            # if 'userId' not in self.session:
            #     self.handle401()
            #     return
            self.handleUserList()
        elif self.path.startswith("/me"):
            if 'userId' not in self.session:
                self.handle401()
                return

            self.handleUserRetrieve(self.session['userId'])

        else:
            self.handle404()

    def do_POST(self):
        self.load_session() # self.session is now ready
        if self.path == "/todos":
            if 'userId' not in self.session:
                self.handle401()
                return
            self.handleTodoCreate()
        if self.path == "/users":
            # if 'userId' not in self.session:
            #     self.handle401()
            #     return
            self.handleUserCreate()
        if self.path == "/session":
            self.handleSessionCreate()
        else:
            self.handle404()

    def do_DELETE(self):
        self.load_session()
        todos_db = TodoDB()
        users_db = UserDB()
        splitPath = self.path.split("/")
        # /todos/3  = ["", "todos", "3"]
        if len(splitPath) >= 3 and splitPath[1] == 'todos':
            id = int(splitPath[2])
            # if 'userId' not in self.session:
            #     self.handle401
            #     return
            if not todos_db.idInDatabase(id):
                self.handle404()
            else:
                self.handleTodoDelete(id)
        elif len(splitPath) >= 3 and splitPath[1] == 'users':
            id = int(splitPath[2])
            if 'userId' not in self.session:
                self.handle401()
                return
            if not users_db.idInDatabase(id):
                self.handle404()
            else:
                self.handleUserDelete(id)
        elif self.path == '/session':
            # print('logout from server')
            self.logout()
            return
        else:
            self.handle404()

    def do_PUT(self):
        self.load_session()
        todos_db = TodoDB()
        users_db = UserDB()
        splitPath = self.path.split("/")
        if len(splitPath) >= 3 and splitPath[1] == 'todos':
            id = int(splitPath[2])
            if 'userId' not in self.session:
                self.handle401()
                return
            if not todos_db.idInDatabase(id):
                self.handle404()
            else:
                self.handleTodoUpdate(id)
        elif len(splitPath) >= 3 and splitPath[1] == 'users':
            id = int(splitPath[2])
            if 'userId' not in self.session:
                self.handle401()
                return
            if not users_db.idInDatabase(id):
                self.handle404()
            else:
                self.handleUserUpdate(id)
        else:
            self.handle404()

    def handleTodoList(self):
        db = TodoDB()
        todos = db.getTodo()
        json_string = json.dumps(todos)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes (json_string, "utf-8"))

    def handleUserList(self):
        db = UserDB()
        users = db.getUser()
        json_string = json.dumps(users)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes (json_string, "utf-8"))

    def handleTodoRetrieve(self, id):
        db = TodoDB()
        todos = db.retrieveTodo(id)
        json_string = json.dumps(todos)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes (json_string, "utf-8"))

    def handleUserRetrieve(self, id):
        db = UserDB()
        users = db.retrieveUser(id)
        json_string = json.dumps(users)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes (json_string, "utf-8"))

    def handleTodoCreate(self):
        # step 1
        length = int(self.headers["Content-length"])
        # step 2
        body = self.rfile.read(length).decode("utf-8")
        # step 3
        parsed_body = parse_qs(body)
        # step 4
        todo = parsed_body['todo'][0]

        db = TodoDB()
        db.createTodo(todo)

        self.send_response(201)
        self.end_headers()
        self.wfile.write(bytes ("Todo Created", "utf-8"))

    def handleUserCreate(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)

        fname = parsed_body['fname'][0]
        lname = parsed_body['lname'][0]
        email = parsed_body['email'][0]
        password = parsed_body['password'][0]
        hash = bcrypt.encrypt(password)
        password = hash

        db = UserDB()
        checkEmail = db.emailInDatabase(email)
        json_string = json.dumps(checkEmail)

        if checkEmail:
            self.handle422()
        else:
            db = UserDB()
            db.createUser(fname, lname, email, password)

            checkEmail = db.emailInDatabase(email)
            json_string = json.dumps(checkEmail)
            self.session["userId"] = checkEmail['id']
            self.send_response(201)
            self.end_headers()
            self.wfile.write(bytes (json_string, "utf-8"))

    def handleTodoDelete(self, id):
        db = TodoDB()
        todos = db.deleteTodo(id)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes ("Todo Deleted", "utf-8"))

    def handleUserDelete(self, id):
        users_db = UserDB()
        users = users_db.deleteUser(id)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes ("User Deleted", "utf-8"))

    def handleTodoUpdate(self, id):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        todo = parsed_body['todo'][0]

        db = TodoDB()
        db.updateTodo(todo, id)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes ('Todo has been Updated', "utf-8"))

    def handleUserUpdate(self, id):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)

        fname = parsed_body['fname'][0]
        lname = parsed_body['lname'][0]
        email = parsed_body['email'][0]
        password = parsed_body['password'][0]

        users_db = UserDB()
        users_db.updateUser(fname, lname, email, password, id)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes ('User has been Updated', "utf-8"))

    def handle200(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes ("<h1>OK</h1>", "utf-8"))
    def handle401(self):
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes ("<h1>Unauthorized</h1>", "utf-8"))
    def handle404(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes ("<h1>Page Not Found</h1>", "utf-8"))
    def handle422(self):
        self.send_response(422)
        self.end_headers()
        self.wfile.write(bytes ("<h1>Opps Try Again</h1>", "utf-8"))

    def handleSessionCreate(self):
        # do authentication stuffs
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)

        email = parsed_body['email'][0]
        password = parsed_body['password'][0]
        # print(email)
        # print(password)
        db = UserDB()
        checkEmail = db.emailInDatabase(email)
        if checkEmail:
            match = bcrypt.verify(password, checkEmail['password'])
            # print('this is my password after verify', bcrypt.verify(password, checkEmail['password']))
            if match:
                self.session["userId"] = checkEmail['id']
                self.send_response(201)
                print('session with id', self.session["userId"])
                # print('session with no key', self.session)
                json_string = json.dumps(checkEmail)
                # print("JSON string:", json_string)
                self.end_headers()
                self.wfile.write(bytes (json_string, "utf-8"))

            else:
                self.handle401()
        else:
            self.handle401()

        # return

    def load_session(self):
        # load the cookie object
        self.load_cookie()
        # find if session_id exists in cookie?
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            # go to the store to see if the id is in it
            sessionData = gSessionStore.getSession(sessionId)
            # find if session_id exists in session store?
            if sessionData is not None:
                # load the session data
                self.session = sessionData
            else:
                # create new session_id with empty session data
                sessionId = gSessionStore.createSession()
                # assign session_id in cookie
                self.cookie["sessionId"] = sessionId
                # load the session data
                self.session = gSessionStore.getSession(sessionId)
        else:
            # create new session_id with empty session data
            sessionId = gSessionStore.createSession()
            # assign session_id in cookie
            self.cookie["sessionId"] = sessionId
            # load the session data
            self.session = gSessionStore.getSession(sessionId)

    def logout(self):
        self.load_session()
        del self.session["userId"]
        self.send_response(200)
        self.end_headers()

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def in_session(self):
        self.load_session()
        if 'userId' not in self.session:
            self.handle401()
            return False
        else:
            return True

def run():
    db_todo = TodoDB().createTodoTable()
    db_user = UserDB().createUserTable()

    db_todo = None # disconnect
    db_user = None # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyServerHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()

run()
