from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo, BooleanProperty

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty() 
    email = StringProperty(unique_index = True)
    country = StringProperty(default = '')
    phone = StringProperty()
    description = StringProperty(default = '')
    account_type = StringProperty ()
    verified = BooleanProperty(default = False)
    followers = RelationshipTo('User', 'FOLLOWER')
    following = RelationshipTo('User', 'FOLLOWING')
