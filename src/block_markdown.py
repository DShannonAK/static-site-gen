from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextType, text_node_to_html_node

class Block_Types:
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "blockquote"
    block_type_olist = "ordered_list"
    block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    block = block.split("\n")
    type = Block_Types.block_type_paragraph
    match block[0][0]:
        case "#":
            head = block[0].split()[0]
            if len(head) <= 6 and len(head.strip("#")) == 0:
                type = Block_Types.block_type_heading
        case "`":
            if block[0].startswith("```") and block[-1].startswith("```"):
                type = Block_Types.block_type_code
        case ">":
            if all(line.startswith(">") for line in block):
                type = Block_Types.block_type_quote
        case "*":
            if all(line.startswith("* ") for line in block):
                type = Block_Types.block_type_ulist
        case "-":
            if all(line.startswith("- ") for line in block):
                type = Block_Types.block_type_ulist
        case "1":
            for i in range(0, len(block)):
                if block[i].startswith(f"{i+1}. "):
                    if i == len(block)-1:
                        type = Block_Types.block_type_olist
                else:
                    break
    return type

def markdown_to_html_node(markdown):
    div = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        node = None
        match type:
            case Block_Types.block_type_paragraph:
                node = ParentNode("p", text_to_children(block.replace("\n", " ")))
            case Block_Types.block_type_heading:
                level = len(block) - len(block.lstrip("#"))
                if level < 1 or level > 6:
                     raise ValueError(f"invalid heading level: {level}")
                node = ParentNode(f"h{level}", text_to_children(block[level+1:]))
            case Block_Types.block_type_code:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                code = ParentNode("code", text_to_children(block[4:-3])) 
                node = ParentNode("pre", [code])
            case Block_Types.block_type_quote:
                lines = block.split("\n")
                lines = list(map(lambda line: line.lstrip(">").strip(), lines))
                node = ParentNode("blockquote", text_to_children(" ".join(lines)))
            case Block_Types.block_type_olist:
                node = ParentNode("ol", [])
                items = block.split("\n")
                for li in items:
                    li_node = ParentNode("li", text_to_children(li[3:]))
                    node.children.append(li_node)
            case Block_Types.block_type_ulist:
                node = ParentNode("ul", [])
                for li in block.split("\n"):
                    li_node = ParentNode("li", text_to_children(li[2:]))
                    node.children.append(li_node)
        div.children.append(node)
    return div
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes
                    
