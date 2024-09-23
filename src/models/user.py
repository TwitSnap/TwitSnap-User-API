from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty() 
    email = StringProperty(unique_index = True)
    country = StringProperty(default = '')
    phone = StringProperty()
    description = StringProperty(default = '')
    account_type = StringProperty ()
    followers = RelationshipTo('User', 'FOLLOWER')
    following = RelationshipTo('User', 'FOLLOWING')
