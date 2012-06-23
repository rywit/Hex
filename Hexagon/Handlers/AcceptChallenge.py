from Handlers.BaseHandler import BaseHandler
from Views.GameView import GameView

class AcceptChallenge( BaseHandler ):
    
    def get(self):
        ## Make sure the user is logged in
        if not self.user:
            self.redirect( "/login" )
            return
        
        ## Pull off the game id from the request
        gameid = self.request.get( "gameid" )
        if not gameid:
            self.render( "error.html", message = "Could not find game ID in request" )
            return
        
        ## Grab the game with this ID
        game = GameView( gameid = gameid )
        
        ## Update the status of the game to "ACTIVE"
        game.update_status( "ACTIVE" )
        
        ## Go to home page
        self.redirect( "/home" )
        