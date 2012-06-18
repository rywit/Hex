from Handlers.Home import Home
from Handlers.Login import Login
from Handlers.Logout import Logout
from Handlers.NewChallenge import NewChallenge
from Handlers.PlayGame import PlayGame
from Handlers.Register import Register

import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([( "/", MainPage ),
                               ( "/login", Login ),
                               ( "/logout", Logout ),
                               ( "/play", PlayGame ),
                               ( "/challenge", NewChallenge ),
                               ( "/register", Register ),
                               ( "/home", Home )
                               ],
                              debug=True)