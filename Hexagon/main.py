from Handlers.AcceptChallenge import AcceptChallenge
from Handlers.Home import Home
from Handlers.Login import Login
from Handlers.Logout import Logout
from Handlers.NewChallenge import NewChallenge
from Handlers.PlayGame import PlayGame
from Handlers.Register import Register
from Handlers.BaseHandler import BaseHandler
import webapp2


class MainPage( BaseHandler ):
    def get(self):
        if self.user:
            self.redirect( "/home" )
        else:
            self.redirect( "/login" )

app = webapp2.WSGIApplication([( "/", MainPage ),
                               ( "/login", Login ),
                               ( "/logout", Logout ),
                               ( "/play", PlayGame ),
                               ( "/accept", AcceptChallenge ),
                               ( "/challenge", NewChallenge ),
                               ( "/register", Register ),
                               ( "/home", Home )
                               ],
                              debug=True)