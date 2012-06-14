from BaseHandler import BaseHandler
from GameLogic.BoardBuilder import BoardBuilder
from Models.Game import Game

class NewChallenge( BaseHandler ):
    def get(self):
        self.render( "new-challenge.html" )

    def post(self):

        ## If the user is not logged in, boot them to the login page        
        if not self.user:
            self.redirect( "/login" )
            return

        player2id = self.request.get( "player2" )
        board = BoardBuilder.get_new_board()
        
        game = Game( player1 = self.user.key(), player2 = player2id, status = "CHALLENGE", board = board )
        
        game.put()
        
        self.redirect( "/play?gameid=123" )
