import xml.etree.ElementTree as ET
def etElem():
   mytree = ET.parse("../dataFiles/"+'check.xml')
   myroot = mytree.getroot()
   print(myroot.tag) # additional
   print(myroot.attrib) # {'{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/additional_file.xsd'}
   print(myroot[0].tag) # tlLogic
   maxGreenTime = {'0':  [30,3,30,3,30,3,30,3,30,1],
                   'Max':[55,3,55,3,55,3,55,3,55,1],
                   'Mid':[55,3,55,3,55,3,55,3,55,1],
                   'Low':[55,3,55,3,55,3,55,3,55,1]}
   print("maxGreenTime:",maxGreenTime['Low'][0])
   for s in maxGreenTime:
       print(s)
   list = [200,300,600,500,600]
   # i = 0
   for k in range(28):
       i = 0
       print("tllogic:",myroot[k].attrib)
       for scenario in maxGreenTime:
        if myroot[k].attrib['programID'] == scenario:
           for x in myroot[k]:
            print(x.tag, x.attrib) # phase {'duration': '60', 'state': 'GGggrrrrGGggrrrrrrrr'}
            print("Hello", x.attrib['duration'])
            x.attrib['duration'] = str(maxGreenTime[scenario][i])
            i = i+1
   mytree.write('new.tll.xml')

def writeDifferentProgramId(case):
    mytree = ET.parse("../dataFiles/" + 'fourPhasestll.tll.xml')
    myroot = mytree.getroot()
    print(myroot.tag)  # additional
    print(
        myroot.attrib)  # {'{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/additional_file.xsd'}
    print(myroot[0].tag)  # tlLogic
    maxGreenTime = {
                    'Low': [30, 3, 30, 3, 30, 3, 30, 3, 30, 1],
                    'Midium': [45, 3, 45, 3, 45, 3, 45, 3, 45, 1],
                    'High': [55, 3, 55, 3, 55, 3, 55, 3, 1, 1]}
    # print("maxGreenTime:", maxGreenTime['Low'][0])
    for s in maxGreenTime:
        print(s)
    list = [200, 300, 600, 500, 600]
    # i = 0
    for k in range(84):
        i = 0
        print("tllogic:", myroot[k].attrib)
        for scenario in maxGreenTime:
            if myroot[k].attrib['programID'] == scenario:
                # myroot[k].attrib['programID'] = case
                for x in myroot[k]:
                    print(x.tag, x.attrib)  # phase {'duration': '60', 'state': 'GGggrrrrGGggrrrrrrrr'}
                    print("Hello", x.attrib['duration'])
                    x.attrib['duration'] = str(maxGreenTime[scenario][i])
                    i = i + 1
        mytree.write("../dataFiles/" + 'fourPhasestllUpdated.tll.xml')


def allCasesInTll():
    mytree = ET.parse("../dataFiles/" + 'fourPhasestll.tll.xml')
    myroot = mytree.getroot()
    print(myroot.tag)  # additional
    print(
        myroot.attrib)  # {'{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/additional_file.xsd'}
    print(myroot[0].tag)  # tlLogic
    maxGreenTime = {'Low':    [30, 3, 30, 3, 30, 3, 30, 3, 1],
                    'Midium': [45, 3, 45, 3, 45, 3, 45, 3, 1],
                    'High':   [55, 3, 55, 3, 55, 3, 55, 3, 1]}
    print("maxGreenTime:", maxGreenTime['Low'][0])
    for s in maxGreenTime:
        print(s)
    list = [200, 300, 600, 500, 600]
    # i = 0
    for k in range(84):
        i = 0
        print("tllogic:", myroot[k].attrib)
        for scenario in maxGreenTime:
            if myroot[k].attrib['programID'] == scenario:
                # myroot[k].attrib['programID'] = case
                for x in myroot[k]:
                    print(x.tag, x.attrib)  # phase {'duration': '60', 'state': 'GGggrrrrGGggrrrrrrrr'}
                    print("Hello", x.attrib['duration'])
                    x.attrib['duration'] = str(maxGreenTime[scenario][i])
                    i = i + 1
    mytree.write("../dataFiles/" + 'fourPhasestllUpdated.tll.xml')


# etElem()

writeDifferentProgramId("Midium")

# allCasesInTll()