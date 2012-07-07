from google.appengine.api import mail
import Handlers.BaseHandler

class HexEmail:

    sender = "Hexagon <noreply@hecksagonal.appspotmail.com>"
    
    @classmethod
    def sendChallenge( cls, to, challenger ):

        ## If there is no email address provided, just leave
        if not to:
            return

        subject = "You have been challenged to a game of Hexagon"
        
        body = """
You have been challenged to a game of Hexagon by your friend %s!

Log in to Hexagon to see your pending challenges:
http://hecksagonal.appspot.com 
        """ % challenger
        
        html = Handlers.BaseHandler.render_str( "email-challenge.html", challenger = challenger )

        mail.send_mail( cls.sender, to, subject, body, html = html )
    
    @classmethod
    def sendInvite( cls, to, inviter ):
        
        ## If there is no email address provided, just leave
        if not to:
            return
        
        subject = "You have been invited to play Hexagon"
        
        body = """
You have been invited to play Hexagon by your friend %s!

Sign up to play Hexagon at http://hecksagonal.appspot.com
        """ % inviter

        html = Handlers.BaseHandler.render_str( "email-invite.html", inviter = inviter )
        
        mail.send_mail( cls.sender, to, subject, body, html = html )

    @classmethod
    def sendMoveNotice( cls, to, opponent ):
        
        ## If there is no email address provided, just leave
        if not to:
            return
        
        subject = "It's your turn to move in Hexagon game against %s" % opponent
        
        body = """
Your friend %s just moved and it is now your turn!

Check out your current games at at http://hecksagonal.appspot.com
        """ % opponent

        html = Handlers.BaseHandler.render_str( "email-move.html", opponent = opponent )
        
        mail.send_mail( cls.sender, to, subject, body, html = html )
