from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipFrom,
    UniqueIdProperty,
    RelationshipTo,
    BooleanProperty,
)
from config.settings import DEFAULT_PROFILE_PHOTO
from models.interest import Interest


class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(index=True)
    email = StringProperty(unique_index=True)
    country = StringProperty(default="")
    phone = StringProperty()
    description = StringProperty(default="")
    verified = BooleanProperty(default=False)
    photo = StringProperty(default=DEFAULT_PROFILE_PHOTO)
    is_banned = BooleanProperty(default=False)
    followers = RelationshipFrom("User", "FOLLOW")
    following = RelationshipTo("User", "FOLLOW")
    interests = RelationshipTo(Interest, "HAS_INTEREST")
