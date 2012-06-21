from google.appengine.ext import db

class Game( db.Model ):
    player1 = db.IntegerProperty( required = True )
    player2 = db.IntegerProperty( required = True )
    status = db.StringProperty( required = True )
    board = db.StringProperty( required = True )
    turn = db.IntegerProperty( required = True )
    winner = db.IntegerProperty( required = False )

    @classmethod
    def by_id( cls, gameid ):
        return Game.get_by_id( gameid, parent = cls.games_key() )
    
    @classmethod
    def games_key( cls, group = "default" ):
        return db.Key.from_path( "games", group )
    
    def update_state( self, player_num, board, status, winner ):
        self.turn = player_num
        self.board = board
        self.status = status
        self.winner = winner
