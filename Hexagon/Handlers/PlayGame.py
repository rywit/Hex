from BaseHandler import BaseHandler
from Models.User import User
from Views.GameView import GameView
import logging
from GameLogic.Exceptions import WrongTurnException
from GameLogic.Email import HexEmail

class PlayGame( BaseHandler ):

    def get( self ):
        "Display board ready to be played"
        
        ## Pull out the requested game ID
        gameid = self.request.get( "gameid" )
        
        ## Make sure a game ID was actually provided
        if not gameid:
            self.redirect( "/error" )
        
        ## Initialize the game view
        game = GameView( gameid = gameid )
        board = game.board.serialize()
        
        ## Look up player names
        player1 = User.by_id( int( game.player1 ) )
        player2 = User.by_id( int( game.player2 ) )
        
        user_id = self.user.key().id()
        
        ## It's my turn if the game is active and i'm the player to move
        is_my_turn = game.is_my_turn( user_id )
        
        status = game.get_detailed_status( user_id )
        
        ## Display the game to the user
        self.render( "play-game.html",
                     player1 = player1.name,
                     player2 = player2.name,
                     board = board,
                     turn = game.turn,
                     is_my_turn = is_my_turn,
                     status = status )
        
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
                
                ## Send email to opponent telling them it's their turn
                player1_name = User.get_user_name( game.player1 )
                player2 = User.by_id( game.player2 )
                
                if player2.email and player2.move_emails:
                    HexEmail.sendMoveNotice( player2.email, player1_name )
                
                ## Redirect to homepage
                self.redirect( "/home" )
            else:
                logging.error( "That's not a valid game" )
                self.redirect( "/" )
                
    def _cancel_move( self, gameid ):
        self.redirect( "/play?gameid=%s" % gameid )
