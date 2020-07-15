import os
import urllib.parse
import datetime

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

def renderSinglePaper(fileName: str):
    paperName = fileName.split(".")[0].split("]")[-1]
    year = int(fileName.split('[')[-1][0:2])
    base = datetime.date.today().year + 1
    prefix = base // 100 * 100
    if year + prefix > base:
        year += prefix - 100
    else:
        year += prefix
    result = f"* {year} - "
    if os.path.exists(os.path.join("Codes", paperName)):
        result += f"[**[Code]**]({os.path.join('Codes', paperName)}) "
    result +=  f"[{paperName}]({urllib.parse.quote(fileName)})"
    return result, year

def renderSingleFolder(node: Node):
    return f"* [{node.name}]({urllib.parse.quote(node.fullPath)})"

def renderPapers(node: Node, level: int):
    a = f"{'#' * (level + 1)} {node.name}\r\n"
    items = [renderSinglePaper(x) for x in node.files]
    items.sort(key=lambda x: x[1])
    a += "\r\n".join(x[0] for x in items)
    a += "\r\n"
    for i in node.dirs:
        a += renderPapers(i, level + 1)
    return a

def renderTutorials(node: Node, level: int):
    a = f"{'#' * (level + 1)} {node.name}\r\n"
    items = [renderSingleFolder(x) for x in node.dirs]
    return a + "\r\n".join(items)

if __name__ == "__main__":
    with open("README.md", "w") as fp:
        fp.write("![Auto Render README.md](https://github.com/retrieval-cfm/Archives/workflows/Auto%20Render%20README.md/badge.svg)\r\n\r\n")
        fp.write("**NOTE**: *Push* or merge from *Pull Requests* will trigger to render this TOC automatically.\r\n\r\n")
        fp.write("* Please refer to [format guideline](GUIDE.md) to arrange files correctly.\r\n\r\n")
        fp.write("# Table of Contents\r\n")
        
        rootNode = Node("Papers", "Papers")
        appendNodes("Papers", rootNode)
        results = renderPapers(rootNode, 0)
        fp.write(results)


        rootNode = Node("Tutorials", "Tutorials")
        appendNodes("Tutorials", rootNode)
        resultsT = renderTutorials(rootNode, 0)
        fp.write(f"\r\n{resultsT}")
