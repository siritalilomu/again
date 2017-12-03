import base64, os

class SessionStore:
    def __init__(self):
        self.sessionStore = {}
        return

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessionStore[sessionId] = {}
        return sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessionStore:
            return self.sessionStore[sessionId]
        else:
            return None
