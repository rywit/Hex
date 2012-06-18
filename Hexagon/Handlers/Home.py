from BaseHandler import BaseHandler
from Models.Game import Game

class Home( BaseHandler ):

    def get( self ):
        
        ## Make sure the user is logged in
        if not self.user:
            self.redirect( "/login" )
            return

        ## Query out current games
        current = self._get_current()
        
        ## Query out pending games
        pending = self._get_pending()
        
        self.render( "home.html", current = current, pending = pending )

    def _get_current( self ):
        games1 = Game.all().filter('player1 =', self.user ).filter( "status =", "ACTIVE" ).fetch( limit = 10 )
        games2 = Game.all().filter('player2 =', self.user ).filter( "status =", "ACTIVE" ).fetch( limit = 10 )
        return list( games1 ) + list( games2 )
    
    def _get_pending( self ):
        games1 = Game.all().filter('player1 =', self.user ).filter( "status =", "CHALLENGE" ).fetch( limit = 10 )
        games2 = Game.all().filter('player2 =', self.user ).filter( "status =", "CHALLENGE" ).fetch( limit = 10 )
        return list( games1 ) + list( games2 )
