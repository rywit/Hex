import json

class BoardBuilder:
    
    @classmethod
    def get_new_board( cls ):
        return [ [ 0 for x in range( 10 ) ] for x in range( 10 ) ] #@UnusedVariable
    
    @classmethod
    def serialize_board( cls, board ):
        return json.dumps( board )
        
        