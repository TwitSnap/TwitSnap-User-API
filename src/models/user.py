# src/models/user.py
from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty
    mail = StringProperty
    country = StringProperty(default='')
    phone = StringProperty()
    description = StringProperty(default='')

    followers = RelationshipTo('User', 'FOLLOWER')
    following = RelationshipTo('User', 'FOLLOWING')
