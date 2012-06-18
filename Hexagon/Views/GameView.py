'''
Created on Jun 16, 2012

@author: ryanwitko
'''
from Models.Board import Board
from Models.Game import Game
from GameLogic.Exceptions import WrongTurnException

class GameView():
    
    def __init__( self, **kwargs ):
        
        if "gameid" in kwargs:
            self._initExisting( kwargs[ "gameid" ] )
        else:
            self._initNew( kwargs[ "player1" ], kwargs[ "player2" ] )
        
    def _initNew( self, player1, player2 ):
        ## Create empty board
        self.board = Board()
        
        ## Save player info
        self.player1 = str( player1 )
        self.player2 = str( player2 )
        
        ## Save status
        self.status = "CHALLENGE"
        self.winner = 0
        self.turn = 1

        ## Create new Game instance
        self.game = Game( player1 = self.player1, player2 = self.player2,
                          status = self.status, board = self.board.serialize(),
                          turn = self.turn, winner = self.winner, parent = Game.games_key() )
        
        ## Save new game to database
        key = self.game.put()
        self.gameid = key.id()
        
    def _initExisting( self, gameid ):
        
        self.gameid = gameid
        
        ## Retrieve game from database
        self.game = Game.by_id( int( gameid ) )

        ## Load up player info
        self.player1 = self.game.player1
        self.player2 = self.game.player2
        self.status = self.game.status
        self.turn = self.game.turn

        ## Create a new board instance        
        self.board = Board( self.game.board )
        
    def update_game( self, user, row, col ):
        
        ## Make sure the correct user is making the move
        player_to_move = self.player1 if self.turn == 1 else self.player2
        
        ## If the wrong player moved, raise an exception
        if str( user.key().id() ) != str( player_to_move ):
            raise WrongTurnException( "It is not your turn to move" )
        
        ## Update the board
        self.board.update_board( row, col, self.turn )
        
        ## Check if game is now finished
        if self.board.is_finished():
            self.winner = self.turn
            self.status = "COMPLETE"
        else:
            ## Flip who's turn it is to move
            self.turn = ( self.turn % 2 ) + 1
            self.status = "ACTIVE"
            self.winner = 0
    
        ## Update the underlying Game
        self.game.update_state( self.turn, self.board.serialize(), self.status, self.winner )
        
        ## Save underlying Game to the database
        self.game.put()
