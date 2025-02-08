class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __repr__(self):
         return f"{self.__class__.__name__}({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        attributes = ""
        if self.props is not None:
            for atr in self.props.items():
                attributes += f' {atr[0]}="{atr[1]}"'
        return attributes

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def __repr__(self):
        return self.to_html()

    def to_html(self):
        if self.value is None or len(self.value) < 1:
            raise ValueError("Leaf nodes must have a value")
        elif self.tag is None or len(self.tag) < 1:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def __repr__(self):
        return self.to_html()

    def to_html(self):
        if self.tag is None or len(self.tag) < 1:
            raise ValueError("Parent nodes must have a tag")
        elif self.children is None or len(self.children) < 1:
            raise ValueError("Parent nodes must have children")
        else:
            html = f'<{self.tag}{self.props_to_html()}>'
            for child in self.children:
                html += child.to_html()
            html += f'</{self.tag}>'
            return html