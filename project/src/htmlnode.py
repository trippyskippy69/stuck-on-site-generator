class HTMLNode:
    def __init__(self, tag, value, children, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        if self.tag is None:
            return self.value

        props_str = ""
        if self.props:
            for key, value in self.props.items():
                props_str += f' {key}="{value}"'

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def props_to_html(self):
        if self.props is None:
            return ''


        props_str = ''
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props if props is not None else {})
        if not (value or tag == "img"):
            raise ValueError("LeafNode value cannot be empty")

    def to_html(self):
        if self.tag:
            props_str = ' '.join(f'{k}="{v}"' for k, v in self.props.items())
            props_part = f' {props_str}' if props_str else ''
            return f"<{self.tag}{props_part}>{self.value}</{self.tag}>"
        return self.value

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one child")

        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"

        children_html = "".join(child.to_html() for child in self.children)

        return f"{opening_tag}{children_html}{closing_tag}"
