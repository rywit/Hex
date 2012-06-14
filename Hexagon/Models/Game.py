from google.appengine.ext import db

def games_key( group = "default" ):
    return db.Key.from_path( "games", group )

class Game( db.Model ):
    player1 = db.StringProperty( required = True )
    player2 = db.StringProperty( required = True )
    status = db.StringProperty( required = True )
    board = db.StringProperty( required = True )

    @classmethod
    def get_by_id( self, gameid ):
        return Game.get_by_id( gameid, parent = games_key() )
