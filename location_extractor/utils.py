def flatten(lst):
    result = []
    for element in lst: 
        if isinstance(element, (list, tuple)):
            result.extend(flatten(element))
        else:
            for e in element.split(","):
                e = e.strip()
                if e:
                    result.append(e)
    return result

def read_lines(f):
    return f.read().strip().split("\n")

def isJavaScript(inputString):
    numberOfCharacters = len(inputString)
    if numberOfCharacters != 0:
        countOfSpecial = inputString.count(";") + inputString.count("=") + inputString.count("var") + inputString.count("{") + inputString.count("}") + inputString.count(":") + inputString.count("\"")
        percentage = float(countOfSpecial) / float(numberOfCharacters)
        if percentage > .01:
            return True
    return False