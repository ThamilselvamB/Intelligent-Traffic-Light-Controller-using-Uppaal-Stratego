from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os
import sys
import optparse
import csv
import random
import time
import matplotlib
import matplotlib.pyplot as plt
from os.path import expanduser
from uppaalStrategoController import callUppaalStratego
from unCoordinatedIntelligentController import callUnCoorIntelController
from CoordinatedIntelligentController import callCoorIntelController
from AreaController import callAreaController
from CoordinatedIntelligentController import callCoorIntelController

import plottingPurpose
import calculateWaitingTime

# from uppaalStrategoController import callUppaalStratego

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
from sumolib import checkBinary  # noqa
import traci  # noqa
def run():
    noOfTrafficLights = 22
    step = 0
    traci.trafficlights.setProgram('cluster_1788554984_1788554987_1788554991_1788554995_1788554996_1788554997_1788555000_1788555001_1788555008_6876795489', 'Low')
    while step <= int(options.step):
        traci.simulationStep()
        # print("step:",step)
        step = step + 1
    traci.close()
    sys.stdout.flush()

def get_options(controllerNameEx,cases):
    optParser = optparse.OptionParser()
    controllerName = ("Intelligent","Fixed-Time","Actuated")
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    optParser.add_option("--controller", type="string", dest="controller", default= controllerNameEx)
    optParser.add_option("--step", type="string", dest="step", default="5000")
    optParser.add_option("--load", type="string", dest="load", default=cases)
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":

    controllerName = ('Fixed-Time', 'Actuated','UppaalStratego','Intelligent','CoordinatedIntelligent')
    cases = ["Case1Low","Case1Mid","Case1High","Case2","Case3","Case4"]
    controllerName = [controllerName[3]]
    cases = ['Case1Low']
    for c in cases:
        plottingPurpose.writeToFile("results/resultOfExperiments.csv", "----------------------------------------------------" + c +
                         "------------------------------------------------------")
        for i in controllerName:
            options = get_options(i,c)
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
            if options.nogui:
                sumoBinary = checkBinary('sumo')
            else:
                sumoBinary = checkBinary('sumo-gui')
            # gerenate route for the cases
            # generateRouteForTwenty.generate_routefileAhmFiftyOsm(c, "ahm2PhaseOsmFiftyLoop.rou.xml", 278)

    # first, generate the route file for this simulation
    # generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    # traci.start(["sumo", "-c", "sim1.sumocfg"], label="sim1")
    # traci.start(["sumo", "-c", "sim2.sumocfg"], label="sim2")
            traci.start([sumoBinary, "-c", "dataFiles/fourPhases.sumocfg","--tripinfo-output", "results/"+options.controller+"Tripfile.xml"],label="static")
    # traci.start([sumoBinary, "-c", "twentyJunctionsAhm/ahm2PhaseOsmLoop.sumocfg", "--tripinfo-output",
    #              "twentyJunctionsAhm/tripinfoInte.xml", "--emission-output", "twentyJunctionsAhm/emiInte.xml"],label="loop")
            run()

