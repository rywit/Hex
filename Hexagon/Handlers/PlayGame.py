from BaseHandler import BaseHandler
from Models.User import User
from Views.GameView import GameView
import logging
from GameLogic.Exceptions import WrongTurnException

class PlayGame( BaseHandler ):

    def get( self ):
        "Display board ready to be played"
        
        ## Pull out the requested game ID
        gameid = self.request.get( "gameid" )
        
        ## Make sure a game ID was actually provided
        if not gameid:
            self.redirect("/error" )
        
        ## Initialize the game view
        game = GameView( gameid = gameid )
        board = game.board.serialize()
        
        ## Look up player names
        player1 = User.by_id( int( game.player1 ) )
        player2 = User.by_id( int( game.player2 ) )
        
        is_my_turn = self.user.key().id() == game.player_to_move()
        
        self.render( "play-game.html",
                     player1 = player1.name,
                     player2 = player2.name,
                     board = board,
                     turn = game.turn,
                     is_my_turn = is_my_turn,
                     status = game.status )
        
    def post( self ):
        
        ## Make sure the user is logged in
        if not self.user:
            self.redirect( "/login" )
            return

        cancel = self.request.get( "cancel" )
        gameid = self.request.get( "gameid" )
        
        ## If the user hit "cancel" then refresh the board
        if cancel:
            self._cancel_move( gameid )
            return
        else:
            ## Retrieve this game from the database
            game = GameView( gameid = gameid )
            
            if game:
                
                ## Grab the move
                row = self.request.get( "row" )
                col = self.request.get( "col" )
                
                try:
                    game.update_game( user = self.user, row = int( row ), col = int( col ) )
                except WrongTurnException as e:
                    self.render( "/play?gameid=%s" % gameid, error = e.message )
                    return
                
                ## Check game status and redirect accordingly
                
                self.redirect( "/home" )
            else:
                logging.error( "That's not a valid game" )
                self.redirect( "/" )
                
    def _cancel_move( self, gameid ):
        self.redirect( "/play?gameid=%s" % gameid )
