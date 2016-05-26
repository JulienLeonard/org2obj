from basics           import *

def islinekeystart(line):
    return (line[0] == "*")

def linelevel(line):
    stars = line.split("*")
    nstars = 0
    for star in stars:
        if len(star) == 0:
            nstars += 1
        else:
            break
    level = nstars - 1
    # puts("linelevel",line,level)
    return level

def linetitle(line):
    result = line.strip("*").strip()
    # puts("linetitle",line,"title",result)
    return result

def islineparam(line):
    return (line[0] == ":")

def lineparam(line):
    strings = line.split(":")
    key = strings[1].strip("-").strip()
    value = ":".join(strings[2:]).strip()
    result = (key,value)
    puts("lineparam",result)
    return result

class OrgLevel:
    def __init__(self,title):
        self.mtitle    = title
        self.mparams   = {}
        self.mchildren = []
        self.mlines    = []

#
# format of result:
# list of OrgLevel,
# Example
#
# * Title1
#  param1: value1
#  param2: value2
#  ** Subtitle1
#  param1: value3
#  * Title2
#
# must give
# [(Title1, [(param1, value1),(param2,value2),(_children, [(Subtitle1, [(param1,value3)])])]),(Title2, [])]
#
def org2obj(filepath):
    result    = []
    cinstancestack = []
    
    for line in flines(filepath):
        line = line.strip()
        if len(line) > 0:
            if islinekeystart(line):
                newlevel = linelevel(line)

                cinstancestack = cinstancestack[0:newlevel]
                title = linetitle(line)
                neworglevel = OrgLevel(title)
                cinstancestack.append(neworglevel)

                if newlevel == 0:
                    result.append(neworglevel)
                else:
                    #puts("cinstancestack[-2]",cinstancestack[-2].tostringall())
                    #puts("cinstancestack[-1]",cinstancestack[-1].tostringall())
                    cinstancestack[-2].mchildren.append(neworglevel)
                # puts("stack len",len(cinstancestack)," templates"," ### ".join([t.tostringall() for t in cinstancestack]))
                
            else:
                if islineparam(line):
                    (key,value) = lineparam(line)
                    cinstancestack[-1].mparams[key] = value
                else:
                    cinstancestack[-1].mlines.append(line)
    return result


def test():
    result = org2obj("example.org")
    for level0 in result:
        puts("level0",level0.mtitle)
        for level1 in level0.mchildren:
            puts("- level1",level1.mtitle)

test()
