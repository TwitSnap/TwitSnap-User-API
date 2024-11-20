from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipFrom,
    UniqueIdProperty,
    RelationshipTo,
    BooleanProperty,
    DateTimeProperty,
)
from config.settings import DEFAULT_PROFILE_PHOTO
from models.interest import Interest

from models.follow_relationship import FollowRelationship


class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(index=True)
    email = StringProperty(index=True)
    country = StringProperty(default="")
    phone = StringProperty()
    provider = StringProperty(default=None)
    description = StringProperty(default="")
    verified = BooleanProperty(default=False)
    photo = StringProperty(default=DEFAULT_PROFILE_PHOTO)
    is_banned = BooleanProperty(default=False)
    followers = RelationshipFrom("User", "FOLLOW", model=FollowRelationship)
    following = RelationshipTo("User", "FOLLOW", model=FollowRelationship)
    interests = RelationshipTo(Interest, "HAS_INTEREST")
    created_at = DateTimeProperty(default_now=True)
