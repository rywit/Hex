from BaseHandler import BaseHandler
from Views.GameView import GameView
from Models.User import User
from collections import namedtuple

class NewChallenge( BaseHandler ):
    def get(self):
        
        ## Make sure the user is logged in
        if not self.user:
            self.redirect( "/login" )
            return

        ## Query out the other users
        all_users = User.all().order( "-name" ).fetch( limit = 100 )
        all_users = list( all_users )

        ## Define a UserItem as a name and id
        UserItem = namedtuple( "UserItem", [ "name", "id" ] )
        
        users = []
        for user in all_users:
            if user.name != self.user.name:
                users.append( UserItem( user.name, user.key().id() ) )
        
        self.render( "new-challenge.html", users = users )

    def post(self):

        ## If the user is not logged in, boot them to the login page        
        if not self.user:
            self.redirect( "/login" )
            return

        ## Create new GameView
        player2 = self.request.get( "player2" )

        game = GameView( player1 = self.user.key().id(), player2 = player2 )
        
        self.redirect( "/play?gameid=%s" % game.gameid )
