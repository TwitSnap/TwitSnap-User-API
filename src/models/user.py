from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo, BooleanProperty

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(index = True) 
    email = StringProperty(unique_index = True)
    country = StringProperty(default = '')
    phone = StringProperty()
    description = StringProperty(default = '')
    verified = BooleanProperty(default = False)
    photo = StringProperty(default = '')
    followers = RelationshipTo('User', 'FOLLOWER')
    following = RelationshipTo('User', 'FOLLOWING')
