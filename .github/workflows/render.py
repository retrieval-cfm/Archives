import os
import urllib.parse

class Node(object):
    def __init__(self, name, path):
        self.fullPath = path
        self.name = name
        self.dirs = list()
        self.files = list()


def appendNodes(root: str, rootNode: Node):
    for item in os.listdir(root):
        path = os.path.join(root, item)
        if os.path.isdir(path):
            newNode = Node(item, path)
            rootNode.dirs.append(newNode)
            appendNodes(path, newNode)
        else:
            rootNode.files.append(path)

def renderItem(dirPath: str, fileName: str):
    paperName = fileName.split(".")[0].split("]")[-1]
    result =  f"* [{paperName}]({urllib.parse.quote(os.path.join(dirPath, fileName))})"
    if os.path.exists(os.path.join("Codes", paperName)):
        result += f"  [*Code*]({os.path.join('Codes', paperName)})"
    return result

def renderTOC(node: Node, level: int):
    a = f"{'#' * (level + 1)} {node.name}\r\n"
    a += "\r\n".join(renderItem(node.fullPath, x) for x in node.files)
    a += "\r\n"
    for i in node.dirs:
        a += renderTOC(i, level + 1)
    return a

if __name__ == "__main__":
    rootNode = Node("Papers", "Papers")
    appendNodes("Papers", rootNode)
    results = renderTOC(rootNode, 0)
    with open("README.md", "w") as fp:
        fp.write(results)