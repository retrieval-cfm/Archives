import os
import urllib.parse
import datetime

class Node(object):
    def __init__(self, name, path):
        self.fullPath = path
        self.name = name
        self.dirs = list()
        self.files = list()
def getAllSubmodules():
    modules = { }
    with open(".gitmodules", "r") as fp:
        lines = fp.readlines()
        i = 0
        while True:
            if lines[i].startswith("[submodule"):
                value = None
                flag = True
                key = None
                while flag:
                    i += 1
                    if lines[i].strip().startswith("path"):
                        splits = lines[i].strip().split('=')[1:]
                        key = "".join(splits).strip()
                    elif lines[i].strip().startswith("url"):
                        splits = lines[i].strip().split('=')[1:]
                        value = "".join(splits).strip()
                    else:
                        raise Exception(f"Unexpected keys appeared. got {lines[i]}")
                    if key is not None and value is not None:
                        flag = False
                modules[key] = value
                i += 1
                if i >= len(lines):
                    break
        return modules

allSubmodules = getAllSubmodules()

def appendNodes(root: str, rootNode: Node, level: int, maxLevel: int):
    for item in os.listdir(root):
        path = os.path.join(root, item)
        if os.path.isdir(path):
            newNode = Node(item, path)
            rootNode.dirs.append(newNode)
            if level + 1 < maxLevel:
                appendNodes(path, newNode, level + 1, maxLevel)
        else:
            rootNode.files.append(path)

def determineIfSubmodule(path: str):
    if path.startswith("./"):
        path = path[2:]
    if path in allSubmodules:
        return allSubmodules[path]
    return path

def renderSinglePaper(fileName: str, codeBase: list):
    paperName = fileName.split(".")[0].split("]")[-1]
    year = int(fileName.split('[')[-1][0:2])
    base = datetime.date.today().year + 1
    prefix = base // 100 * 100
    if year + prefix > base:
        year += prefix - 100
    else:
        year += prefix
    result = f"* {year} - "
    if os.path.join("Codes", paperName) in codeBase:
        codePath = determineIfSubmodule(os.path.join("Codes", paperName))
        result += f"[**[Code]**]({codePath}) "
        codeBase.remove(os.path.join("Codes", paperName))
    result +=  f"[{paperName}]({urllib.parse.quote(fileName)})"
    return result, year

def renderSingleFolder(node: Node):
    return f"* [{node.name}]({urllib.parse.quote(node.fullPath)})"

def renderPapers(node: Node, level: int, codeBase: list):
    a = f"{'#' * (level + 1)} {node.name}\r\n"
    items = [renderSinglePaper(x, codeBase) for x in node.files]
    items.sort(key=lambda x: x[1])
    a += "\r\n".join(x[0] for x in items)
    a += "\r\n"
    for i in node.dirs:
        a += renderPapers(i, level + 1, codeBase)
    return a

def renderTutorials(node: Node, level: int):
    a = f"{'#' * (level + 1)} {node.name}\r\n"
    items = [renderSingleFolder(x) for x in node.dirs]
    return a + "\r\n".join(items)

def findOutAllCodeDir():
    rootNode = Node("Codes", "Codes")
    appendNodes("Codes", rootNode, 0, 2)
    result = []
    def appendResult(n: Node):
        for f in n.files:
            result.append(f)
        for node in n.dirs:
            if node.fullPath in allSubmodules:
                result.append(node.fullPath)
                continue
            appendResult(node)
        if len(n.dirs) == 0:
            result.append(n.fullPath)
    appendResult(rootNode)
    return result

def renderCodes(codeBase: list):
    result = "# Codes\r\n"
    codes = []
    for c in codeBase:
        fileName = os.path.basename(c)
        if c in allSubmodules:
            codes.append(f"* [{fileName}]({allSubmodules[c]})")
        else:
            codes.append(f"* [{fileName}]({c})")
    result += "\r\n".join(codes)
    return result

if __name__ == "__main__":
    with open("README.md", "w") as fp:
        fp.write("![Auto Render README.md](https://github.com/retrieval-cfm/Archives/workflows/Auto%20Render%20README.md/badge.svg)\r\n\r\n")
        fp.write("**NOTE**: *Push* or merge from *Pull Requests* will trigger to render this TOC automatically.\r\n\r\n")
        fp.write("**Please refer to [formatting guideline](GUIDE.md) to arrange files correctly**.\r\n\r\n")
        fp.write("# Table of Contents\r\n")
        
        rootNode = Node("Papers", "Papers")
        appendNodes("Papers", rootNode, 0, 10000)
        codeBase = findOutAllCodeDir()
        results = renderPapers(rootNode, 0, codeBase)
        fp.write(results)


        rootNode = Node("Tutorials", "Tutorials")
        appendNodes("Tutorials", rootNode, 0, 10000)
        resultsT = renderTutorials(rootNode, 0)
        fp.write(f"\r\n{resultsT}")

        fp.write("\r\n\r\n")
        resultsC = renderCodes(codeBase)
        fp.write(resultsC)
