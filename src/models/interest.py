from neomodel import StructuredNode, StringProperty, RelationshipFrom

class Interest(StructuredNode):
    name = StringProperty(unique_index=True, required=True) 