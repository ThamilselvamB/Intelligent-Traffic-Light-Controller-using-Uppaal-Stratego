
import sys
import os
import time
import string
import math
from os.path import expanduser
import numpy as np
import random
prevCmdOutputYellow = ('Options for the verification:\n  Generating no trace\n  Search order is breadth first\n  Using conservative space optimisation\n  Seed is 1586686604\n  State space representation uses minimal constraint systems\n\x1b[2K\nVerifying formula 1 at line 1\n -- Throughput: 201020 states/sec, Load: 100 iterations\x1b[K\n -- Throughput: 82174 states/sec, Load: 34 iterations\x1b[K\n -- Throughput: 75035 states/sec, Load: 7 iterations\x1b[K\n\x1b[2K -- Formula is satisfied.\n(2970 runs)\nLearning statistics for best strategy: \n\tNumber of resets: 0\n\tNumber of iterations in last reset: 27\n\tNumber of iterations in total: 27\n\n\x1b[2K\nVerifying formula 2 at line 2\n\x1b[2K -- Formula is satisfied.\n2 * yellow.North + 4 * yellow.East + 6 * yellow.South + 8 * yellow.West:\n[0]: (0,0) (0,0) (0,2) (0,2) (5,2) (5,0) (5,2) (10,2) (10,0) (10,2) (15,2) (15,0) (15,0) (15,8) (15,8) (20,8) (20,0) (20,4) (25,4) (25,0) (25,0) (25,8) (25,8) (30,8) (30,0) (30,2) (35,2) (35,0) (35,0) (35,6) (35,6) (40,6) (40,0) (40,6) (45,6) (45,0) (45,6) (50,6) (50,0) (50,6) (55,6) (55,0) (55,6) (60,6) (60,0) (60,6) (65,6) (65,0) (65,6) (70,6) (70,0) (70,6) (75,6) (75,0) (75,6) (80,6) (80,0) (80,6) (85,6) (85,0) (85,6) (90,6) (90,0) (90,6) (95,6) (95,0) (95,6) (100,6) (100,0) (100,6)\n')
prevCmdOutputExtendGreen = ('Options for the verification:\n  Generating no trace\n  Search order is breadth first\n  Using conservative space optimisation\n  Seed is 1571542488\n  State space representation uses minimal constraint systems\n\x1b[2K\nVerifying formula 1 at line 5\n -- Throughput: 123540 states/sec, Load: 100 iterations\x1b[K\n -- Throughput: 209962 states/sec, Load: 90 iterations\x1b[K\n -- Throughput: 198543 states/sec, Load: 73 iterations\x1b[K\n\x1b[2K -- Formula is satisfied.\n(1080 runs)\nLearning statistics for best strategy: \n\tNumber of resets: 1\n\tNumber of iterations in last reset: 3\n\tNumber of iterations in total: 15\n\n\x1b[2K\nVerifying formula 2 at line 7\n -- Throughput: 89 states/sec, Load: 1 runs\x1b[K\n -- Throughput: 146341 states/sec, Load: 1 runs\x1b[K\n\x1b[2K -- Formula is satisfied.\n2 * trafficLight_1.GREEN_A + 6 * trafficLight_1.YELLOW + 10 * trafficLight_1.GREEN_B:\n[0]: (0,0) (0,0) (0,10) (0,10) (5,10) (5,0) (5,10) (10,10) (10,0) (10,10) (15,10) (15,0) (15,0) (60,0) (60,0) (60,10) (60,10) (65,10) (65,0) (65,10) (70,10) (70,0) (70,0) (100,0) (100,0) (100,10) (100,10) (105,10) (105,0) (105,10) (110,10) (110,0) (110,0) (140,0) (140,0) (140,10) (140,10) (145,10) (145,0) (145,10) (150,10) (150,0) (150,0) (180,0) (180,0) (180,10) (180,10) (185,10) (185,0) (185,10) (190,10) (190,0) (190,0) (220,0) (220,0) (220,10) (220,10) (225,10) (225,0) (225,10) (230,10) (230,0) (230,0) (300,0)\n\x1b[2K\nVerifying formula 3 at line 8\n -- Throughput: 89 states/sec, Load: 1 runs\x1b[K\n -- Throughput: 150501 states/sec, Load: 1 runs\x1b[K\n\x1b[2K -- Formula is satisfied.\n2 * trafficLight_2.GREEN_A + 6 * trafficLight_2.YELLOW + 10 * trafficLight_2.GREEN_B:\n[0]: (0,0) (0,0) (15,0) (15,0) (15,10) (15,10) (20,10) (20,0) (20,10) (25,10) (25,0) (25,10) (30,10) (30,0) (30,0) (70,0) (70,0) (70,10) (70,10) (75,10) (75,0) (75,10) (80,10) (80,0) (80,0) (110,0) (110,0) (110,10) (110,10) (115,10) (115,0) (115,10) (120,10) (120,0) (120,0) (150,0) (150,0) (150,10) (150,10) (155,10) (155,0) (155,10) (160,10) (160,0) (160,0) (190,0) (190,0) (190,10) (190,10) (195,10) (195,0) (195,10) (200,10) (200,0) (200,0) (230,0) (230,0) (230,10) (230,10) (235,10) (235,0) (235,10) (240,10) (240,0) (240,0) (300,0)\n\x1b[2K\nVerifying formula 4 at line 9\n -- Throughput: 89 states/sec, Load: 1 runs\x1b[K\n -- Throughput: 151770 states/sec, Load: 1 runs\x1b[K\n\x1b[2K -- Formula is satisfied.\n2 * trafficLight_3.GREEN_A + 6 * trafficLight_3.YELLOW + 10 * trafficLight_3.GREEN_B:\n[0]: (0,0) (0,0) (30,0) (30,0) (30,10) (30,10) (35,10) (35,0) (35,10) (40,10) (40,0) (40,10) (45,10) (45,0) (45,0) (80,0) (80,0) (80,10) (80,10) (85,10) (85,0) (85,10) (90,10) (90,0) (90,0) (120,0) (120,0) (120,10) (120,10) (125,10) (125,0) (125,10) (130,10) (130,0) (130,0) (160,0) (160,0) (160,10) (160,10) (165,10) (165,0) (165,10) (170,10) (170,0) (170,0) (200,0) (200,0) (200,10) (200,10) (205,10) (205,0) (205,10) (210,10) (210,0) (210,0) (240,0) (240,0) (240,10) (240,10) (245,10) (245,0) (245,10) (250,10) (250,0) (250,0) (300,0)\n\x1b[2K\nVerifying formula 5 at line 10\n -- Throughput: 88 states/sec, Load: 1 runs\x1b[K\n -- Throughput: 158081 states/sec, Load: 1 runs\x1b[K\n\x1b[2K -- Formula is satisfied.\n2 * trafficLight_4.GREEN_A + 6 * trafficLight_4.YELLOW + 10 * trafficLight_4.GREEN_B:\n[0]: (0,0) (0,0) (45,0) (45,0) (45,2) (45,2) (50,2) (50,0) (50,2) (55,2) (55,0) (55,2) (60,2) (60,0) (60,0) (90,0) (90,0) (90,2) (90,2) (95,2) (95,0) (95,2) (100,2) (100,0) (100,0) (130,0) (130,0) (130,2) (130,2) (135,2) (135,0) (135,2) (140,2) (140,0) (140,0) (170,0) (170,0) (170,2) (170,2) (175,2) (175,0) (175,2) (180,2) (180,0) (180,0) (210,0) (210,0) (210,2) (210,2) (215,2) (215,0) (215,2) (220,2) (220,0) (220,0) (250,0) (250,0) (250,2) (250,2) (255,2) (255,0) (255,2) (260,2) (260,0) (260,0) (300,0)\n')
home = expanduser("~")
rootDir = os.path.abspath(os.getcwd())
pathToModels = rootDir+"/models/"
experimentId = ['unCoordinated',5,44,55,2]
phases = [1,2,3,4]
# define some parameters here
strategoTrafficLightModelExtendGreen = pathToModels + "unCoordinationExtendGreen.xml"
strategoQueryExtendGreen = pathToModels + "unCoordinationExtendGreen.q"
strategoTrafficLightModelYellow = pathToModels + "unCoordinationYellow.xml"
strategoQueryYellow = pathToModels + "unCoordinationYellow.q"


strategoLearningMet = "3"
strategoSuccRuns = "20" # 50
strategoGoodRuns = "20" # 50
strategoMaxRuns = "100" # 100
strategoEvalRuns = "10"
strategoMaxIterations = "200" # 200
def runStratego(get_stretego, args, query,extendGreen):
    # print ('calling stratego with command: ' + com + args + query )
    start_time = time.time()
    f = os.popen(get_stretego+args+query)
    out = f.read()
    if (" Formula is NOT satisfied" or "\nOut of memory" )in out:
        print("No strategy now, use previous output")
        if extendGreen:
            out = prevCmdOutputExtendGreen
        else:
            out = prevCmdOutputYellow
    total_time = time.time() - start_time
    return total_time, out

def listToStringWithoutBrackets(list1):
    return str(list1).replace('[','').replace(']','')
def listTodoubleArray(list1):
    newList = list1
    for i in range(len(list1[:-1])):
        newList[i] = (str(list1[i]).replace('[', '{').replace(']', '},'))
    newList[-1] = (str(list1[-1]).replace('[', '{').replace(']', '}'))
    l1 = newList[0] + newList[1] + newList[2] + newList[3]
    # print(l1)
    return l1

def createModel(master_model, experimentId, vehicleList, queLength, curGreenTime, maxGreenTime,extendGreen,curPhase,remainingPhases):
    fo = open(master_model, "r+")
    str_model = fo.read()
    fo.close()
    if extendGreen:
        toReplace = "//CURRENT-PHASE"
        value = "int c_phase =" + str(curPhase) + ";"
        str_model = str.replace(str_model, toReplace, value, 1)

        toReplace = "//REMAINING-PHASES"
        value = "int remainingPhases[3] = {" + listToStringWithoutBrackets(remainingPhases) + "};"
        str_model = str.replace(str_model, toReplace, value, 1)

    toReplace = "//VEHICLE-LIST"
    value = "int waitingVehicles[direc][direc]={ " + listTodoubleArray(vehicleList) + "};"
    str_model = str.replace(str_model, toReplace, value, 1)

    toReplace = "//QUEUE-LENGTH"
    value = "int queueLength[direc] = { " + listToStringWithoutBrackets(queLength) + "};"
    str_model = str.replace(str_model, toReplace, value, 1)

    toReplace = "//CUR-GREEN-TIME"
    value = "int currentGreenTime[direc] = { " + listToStringWithoutBrackets(curGreenTime) + "};"
    str_model = str.replace(str_model, toReplace, value, 1)

    toReplace = "//MAXIMUM-GREEN-TIME"
    value = "int maxGreenTime[direc] = { " + listToStringWithoutBrackets(maxGreenTime) + "};"
    str_model = str.replace(str_model, toReplace, value, 1)

    modelName = pathToModels + "tl" + str(experimentId) + ".xml"
    text_file = open(modelName, "w")
    text_file.write(str_model)
    text_file.close()
    return modelName


def outputStringToindividualOne(string1,startString):
    originalOutput_split = list(string1)
    # remove timing information and get output
    originalOutput_split = str(originalOutput_split[1]).split(' ')
    start = 0; end = 0;
    step = 0
    stepEnd = 0
    for i in originalOutput_split:
        if i == startString:
            start = step
            break
        else:
            step += 1
    reqOutput = originalOutput_split[start::]
    return  reqOutput

def strategyTime(list):
    first = 0
    second = 0
    phase = 4
    for i in  range(1,len(list)-1):
        first = int(list[i][1])
        second = int(list[i+1][1])
        if first < second:
            phase = list[i+1][3]
            break
    return int(phase)

def phaseConversionYellow(phase):
    # print("Phase value in phase conversion:",phase)
    nextphase = 1
    if phase == 2:
        nextphase = 1
    if phase == 4:
        nextphase = 2
    if phase == 6:
        nextphase = 3
    if phase == 8:
        nextphase = 4
    return nextphase
def phaseConversionGreen(phase,curPhase,remainingPhases):
    if phase == 2:
        nextphase = curPhase
        print("Extend green equal phase:",nextphase)
    else:
        nextphase = random.choice(remainingPhases)
        print("Extend green random phase:",nextphase)

    return nextphase
def extractStrategy(output,extendGreen,curPhase,remainingPhases):
    nextPhase = 1
    if extendGreen:
        afterExtraction = outputStringToindividualOne(output, 'extendGreen.goYellow_3:\n[0]:')
        print("After extraction", afterExtraction)
        phase = strategyTime(afterExtraction)
        print("After Phase:", phase)
        nextPhase = phaseConversionGreen(phase,curPhase,remainingPhases)
    else:
        afterExtraction = outputStringToindividualOne(output, 'yellow.West:\n[0]:')
        print("After extraction", afterExtraction)
        phase = strategyTime(afterExtraction)
        print("After Phase:", phase)
        nextPhase = phaseConversionYellow(phase)
    return int(nextPhase)

def findRemaingPhases(cPhase):
    remainingPhases = []
    for i in phases:
        if cPhase == i:
            # print("Equal....",cPhase,i)
            continue
        else:
            # print("Not equal",cPhase,i)
            remainingPhases.append(i)
    print("Remainig Phases:",remainingPhases)
    return remainingPhases



def callUnCoorIntelController(vehicleList, queLength, curGreen, maxGreen, extendGreen, curPhase):
    remainingPhases = findRemaingPhases(curPhase)
    stratego = 'verifyta '
    # -------------------------------------- single traffic light model --------------------------------------------
    if extendGreen:
        print("Calling Extend Green Model in UnCoordinated Intelligent...")
        newModel = createModel(strategoTrafficLightModelExtendGreen, experimentId[0], vehicleList, queLength, curGreen, maxGreen,
                               extendGreen, curPhase,remainingPhases)
    else:
        print("Calling Yellow Model in UnCoordinated Intelligent...")
        newModel = createModel(strategoTrafficLightModelYellow, experimentId[0], vehicleList, queLength, curGreen, maxGreen,
                               extendGreen, curPhase,remainingPhases)

    argsFour = newModel \
      + ' --learning-method ' + strategoLearningMet \
      + ' --good-runs ' + strategoSuccRuns \
      + ' --total-runs ' + strategoMaxRuns \
      + ' --runs-pr-state ' + strategoGoodRuns \
      + ' --eval-runs ' + strategoEvalRuns \
      + ' --max-iterations ' + strategoMaxIterations \
      + ' --filter 0 '
    #  call extend green model
    if extendGreen:
        cmdOutputFour = runStratego(stratego, argsFour, strategoQueryExtendGreen, extendGreen)  # command line output
    else:
        cmdOutputFour = runStratego(stratego, argsFour, strategoQueryYellow, extendGreen)  # command line output
    # print("Calling intelligent for traffic light strategy")
    # print("output like: \n",cmdOutputFour)
    nextPhase = extractStrategy(cmdOutputFour,extendGreen,curPhase,remainingPhases)
    # nextPhase = phaseConversion(phaseinfoFour)
    print("Phases from Intelligent Controller:",nextPhase)
    return nextPhase


if __name__ == "__main__":
    extendGreen = True
    curPhase = 1
    areaJammed = [[15, 21, 14, 35],[1, 1, 14, 3],    [1, 1, 14, 3],[1, 1, 14, 3]]
    queueLenth = [120, 1, 14, 3]
    remainingPhases = [2,3,4]
    currentGreenTime = [30,20,20,20]
    maxGreenTime = [40,40,40,40]
    print(os.path.abspath(os.getcwd()))
    phase = callUnCoorIntelController(areaJammed,queueLenth,currentGreenTime,maxGreenTime,extendGreen,curPhase)





