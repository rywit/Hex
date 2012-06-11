import webapp2
from Handlers.Login import Login
from Handlers.Register import Register

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')




app = webapp2.WSGIApplication([( "/", MainPage ),
                               ( "/login", Login ),
                               ( "/register", Register )
                               ],
                              debug=True)