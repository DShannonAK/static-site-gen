class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __repr__(self):
        return self.to_html()

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        attributes = ""
        if self.props is not None:
            for atr in self.props.items():
                attributes += f' {atr[0]}="{atr[1]}"'
        return attributes
    