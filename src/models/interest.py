from neomodel import StructuredNode, StringProperty


class Interest(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
