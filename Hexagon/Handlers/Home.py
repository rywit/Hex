from BaseHandler import BaseHandler
from Models.Game import Game
from Models.User import User

class Home( BaseHandler ):

    def get( self ):
        
        ## Make sure the user is logged in
        if not self.user:
            self.redirect( "/login" )
            return

        user_id = self.user.key().id()
        
        ## Query out current games
        current = self._get_current( user_id )
        
        ## Query out pending games
        pending = self._get_pending( user_id )
        
        self.render( "home.html", current = current, pending = pending )

    def _get_current( self, user_id ):
        parent = Game.games_key()
        games1 = Game.all().filter( 'player1 =', user_id ).filter( "status =", "ACTIVE" ).ancestor( parent ).fetch( limit = 10 )
        games2 = Game.all().filter( 'player2 =', user_id ).filter( "status =", "ACTIVE" ).ancestor( parent ).fetch( limit = 10 )
        
        ## Combine lists
        games = list( games1 ) + list( games2 )
        
        data = []
        for game in games:
            
            u1 = User.by_id( game.player1 )
            u2 = User.by_id( game.player2 )
            
            data.append( {
                "gameid": game.key().id(),
                "player1": u1.name,
                "player2": u2.name
            } )
            
        return data
    
    def _get_pending( self, user_id ):
        parent = Game.games_key()
        games1 = Game.all().filter('player1 =', user_id ).filter( "status =", "CHALLENGE" ).ancestor( parent ).fetch( limit = 10 )
        games2 = Game.all().filter('player2 =', user_id ).filter( "status =", "CHALLENGE" ).ancestor( parent ).fetch( limit = 10 )
        return list( games1 ) + list( games2 )
