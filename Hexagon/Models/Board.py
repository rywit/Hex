import json
from GameLogic.Traversal import Traversal

class Board():
    
    def __init__( self, existing = None ):
        
        ## If an existing board was passed in, decode it
        if existing:
            self.grid = json.loads( existing )
        ## Otherwise, create a new empty board
        else:
            self.grid = [ [ 0 for x in range( 10 ) ] for x in range( 10 ) ] #@UnusedVariable
        
    def serialize( self ):
        return json.dumps( self.grid )
    
    def update_board( self, row, col, player_num ):
        self.grid[ row ][ col ] = player_num

    def is_finished( self ):
        return Traversal.checkForTraversal( self.grid )
