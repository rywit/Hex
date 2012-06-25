from BaseHandler import BaseHandler
from Models.Game import Game
from Models.User import User
from Views.GameView import GameView

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
        waiting, pending = self._get_pending( user_id )
        
        ## Query out finished games
        finished = self._get_finished( user_id )
        
        self.render( "home.html",
                     current = current,
                     pending = pending,
                     waiting = waiting,
                     finished = finished )

    def _get_current( self, user_id ):
        parent = Game.games_key()
        games1 = Game.all().filter( 'player1 =', user_id ).filter( "status =", "ACTIVE" ).ancestor( parent ).fetch( limit = 10 )
        games2 = Game.all().filter( 'player2 =', user_id ).filter( "status =", "ACTIVE" ).ancestor( parent ).fetch( limit = 10 )
        games = list( games1 ) + list( games2 )
        return self._build_game_set( games ) 
    
    def _get_pending( self, user_id ):
        parent = Game.games_key()
        waiting = Game.all().filter('player1 =', user_id ).filter( "status =", "CHALLENGE" ).ancestor( parent ).fetch( limit = 10 )
        waiting = list( waiting )
        waiting_games = self._build_game_set( waiting )
        
        pending = Game.all().filter('player2 =', user_id ).filter( "status =", "CHALLENGE" ).ancestor( parent ).fetch( limit = 10 )
        pending = list( pending )
        pending_games = self._build_game_set( pending )
        
        return waiting_games, pending_games 

    def _get_finished( self, user_id ):
        parent = Game.games_key()
        games1 = Game.all().filter('player1 =', user_id ).filter( "status =", "COMPLETE" ).ancestor( parent ).fetch( limit = 10 )
        games2 = Game.all().filter('player2 =', user_id ).filter( "status =", "COMPLETE" ).ancestor( parent ).fetch( limit = 10 )
        games = list( games1 ) + list( games2 )
        return self._build_game_set( games ) 
    
    def _build_game_set( self, games ):
        data = []
        for game in games:
            
            gameid = game.key().id()
            view = GameView( gameid = gameid )
            
            user_id = self.user.key().id()
            
            player1_name = User.get_user_name( view.player1 )
            player2_name = User.get_user_name( view.player2 )
            
            data.append( {
                "gameid": gameid,
                "player1": player1_name,
                "player2": player2_name,
                "status": view.get_detailed_status( user_id )
            } )
            
        return data
    
    
