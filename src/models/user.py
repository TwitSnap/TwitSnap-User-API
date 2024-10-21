from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo, BooleanProperty

from config.settings import DEFAULT_PROFILE_PHOTO

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(index = True) 
    email = StringProperty(unique_index = True)
    country = StringProperty(default = '')
    phone = StringProperty()
    description = StringProperty(default = '')
    verified = BooleanProperty(default = False)
    photo = StringProperty(default = DEFAULT_PROFILE_PHOTO)
    is_banned = BooleanProperty(default = False)
    followers = RelationshipTo('User', 'FOLLOWER')
    following = RelationshipTo('User', 'FOLLOWING')
