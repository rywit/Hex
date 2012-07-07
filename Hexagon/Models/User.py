from google.appengine.api import mail, memcache
from google.appengine.ext import db
from string import letters
import hashlib
import random

def users_key( group = "default" ):
    return db.Key.from_path( "users", group )

def make_salt( length = 5 ):
    return ''.join( random.choice( letters ) for x in xrange( length ) ) #@UnusedVariable

def make_pw_hash( name, pw, salt = None ):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256( name + pw + salt ).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class User( db.Model ):
    name = db.StringProperty( required = True )
    pw_hash = db.StringProperty( required = True )
    email = db.StringProperty()
    move_emails = db.BooleanProperty()

    @classmethod
    def by_id( cls, uid ):
        return User.get_by_id( uid, parent = users_key() )

    @classmethod
    def by_name( cls, name ):
        u = User.all().filter( "name =", name ).get()
        return u

    @classmethod
    def register( cls, name, pw, email = None ):
        pw_hash = make_pw_hash( name, pw )
        
        return User( parent = users_key(),
                     name = name,
                     pw_hash = pw_hash,
                     email = email,
                     move_emails = True )

    @classmethod
    def login( cls, name, pw ):
        u = cls.by_name( name )
        if u and valid_pw( name, pw, u.pw_hash ):
            return u
        
    @classmethod
    def get_user_name( cls, user_id ):
        
        ## Look in memcache for this user name
        data = memcache.get( "USERNAME" + str( user_id ) ) #@UndefinedVariable
        
        ## If user name was found, return it
        if data is not None:
            return data
        else:
            ## Look up user from database
            user = cls.by_id( user_id )
            
            ## Grab user's name
            user_name = user.name
            
            ## Add this user name to memcache
            memcache.add( "USERNAME" + str( user_id ), user_name, 60 ) #@UndefinedVariable
            
            ## Return this user's name
            return user_name
        
    def send_email( self, sender, subject, body, html ):
        if not self.email:
            return
        
        mail.send_mail( sender, self.email, subject, body, html = html )
