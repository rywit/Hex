from BaseHandler import BaseHandler

class NewChallenge( BaseHandler ):
    def get(self):
        self.render( "new-challenge.html" )

    def post(self):
        pass
