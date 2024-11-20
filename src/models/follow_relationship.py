from neomodel import StructuredNode, DateTimeProperty, StructuredRel


class FollowRelationship(StructuredRel):
    created_at = DateTimeProperty(default_now=True)
