from BaseHandler import BaseHandler
from Models import User

class Login( BaseHandler ):
    def get(self):
        self.render( "login-form.html" )

    def post(self):
        username = self.request.get( 'username' )
        password = self.request.get( 'password' )

        u = User.login( username, password ) #@UndefinedVariable
        if u:
            self.login(u)
            self.render( "welcome.html", username = username )
        else:
            msg = 'Invalid login'
            self.render( "login-form.html", error = msg )
