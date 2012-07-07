from BaseHandler import BaseHandler

class Settings( BaseHandler ):
    
    def get( self ):
        
        user = self.user
        
        move_emails = "yes" if user.move_emails else "no"
        
        self.render( "user-settings.html", email = user.email, move_emails = move_emails )
        
    def post( self ):
        
        user = self.user
        
        email = self.request.get( "email" )
        move_emails = self.request.get( "move_emails" )
        
        user.email = email
        user.move_emails = move_emails and move_emails == "yes"

        user.put()

        ## Redirect to homepage
        self.redirect( "/home" )