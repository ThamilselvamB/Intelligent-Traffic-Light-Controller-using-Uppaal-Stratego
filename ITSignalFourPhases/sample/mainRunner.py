#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    detectorData.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

# @ modified for research purpose Thamilselvam B
# @date 2019-08-01

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
from AreaController import callAreaController_1,callAreaController_2,callAreaController_3,callAreaController_4
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
# import test
NoOfTrafficLights = 5
# allDetectors = ['North100','East100','South100','West100','North300','East300','South300','West300','NorthLoop'
#     ,'EastLoop','SouthLoop','WestLoop','NorthLoopArea','EastLoopArea','SouthLoopArea','WestLoopArea']
queuePhases = [0,2,4,6]
actuatedCurrentPhase = 0
directionDict = {
    "North":['North100','North300'],
    "East":['East100','East300'],
    "South":['South100','South300'],
    "West": ['West100','West300']
}
directions = ['North','East','South','West']
loopAreaDirection = ['NorthLoopArea','EastLoopArea','SouthLoopArea','WestLoopArea']
waitingTimeOfVehcile = {}
noOfStops = {}
trafficData = {
    # traffic light junction detector details
    5:
        {
        "TrafficLightId":"440015629",
        "North100":['e2det_37571582#0_1'],
        "East100":['e2det_-331667958#8_1'],
        "South100":['e2det_-37571582#1_1'],
        "West100":['e2det_331667958#7_1','T1_W_100_1','T1_W_100_2'],
        "North300":['T1_N_300_1'],
        "East300":['T1_E_300_1'],
        "South300":['T1_S_300_1','T1_S_300_2'],
        "West300":['T1_W_300_1','T1_W_300_2'],
        "NorthLoop":['e1det_37571582#0_1'],
        "EastLoop":['e1det_-331667958#8_1'],
        "SouthLoop":['e1det_-37571582#1_1'],
        "WestLoop":['e1det_331667958#7_1'],
        "NorthLoopArea":['e2detLoop_37571582#0_1'],
        "EastLoopArea":['e2detLoop_-331667958#8_1'],
        "SouthLoopArea":['e2detLoop_-37571582#1_1'],
        "WestLoopArea":['e2detLoop_331667958#7_1'],
    },

    4:
        {
        "TrafficLightId":"cluster_1788607244_1789788641_1789788643_1789788649_440296435",
        "North100":['e2det_167468378#1_2','e2det_167468378#1_1','T2_N_100_4','T2_N_100_2','T2_N_100_1','T2_N_100_3','T2_N_100_6','T2_N_100_5'],
        "East100":['e2det_-167589223#0_1','T2_E_100_1','T2_E_100_2'],
        "South100":['e2det_167584434#6_2','e2det_167584434#6_1','T2_S_100_1','T2_S_100_3'],
        "West100":['e2det_167584430#6_1'],
        "North300":['T2_N_300_1','T2_N_300_2','T2_N_300_3','T2_N_300_4'],
        "East300":['T2_E_300_1','T2_E_300_2'],
        "South300":['T2_S_300_1','T2_S_300_2','T2_S_300_3'],
        "West300":[],
        "NorthLoop":['e1det_167468378#1_2','e1det_167468378#1_1'],
        "EastLoop":['e1det_-167589223#0_1'],
        "SouthLoop":['e1det_167584434#6_2','e1det_167584434#6_1'],
        "WestLoop":['e1det_167584430#6_1'],
        "NorthLoopArea":['e2detLoop_167468378#1_2','e2detLoop_167468378#1_1'],
        "EastLoopArea":['e2detLoop_-167589223#0_1'],
        "SouthLoopArea":['e2detLoop_167584434#6_1','e2detLoop_167584434#6_2'],
        "WestLoopArea":['e2detLoop_167584430#6_1'],
    },
    1:
        {
        "TrafficLightId":"440296469",
        "North100":['e2det_331667964#3_1','T3_N_100_1','T5_S_100_2'],
        "East100":['e2det_37573561#2_1','T3_E_100_1'],
        "South100":['e2det_-331667964#4_1','T3_S_100_1'],
        "West100":['e2det_-37573561#3_1','T3_W_100_1','T3_W_100_2'],
        "North300":['T3_N_300_1'],
        "East300":['T3_E_300_1','T3_E_300_2'],
        "South300":['T3_S_300_1','T3_S_300_2'],
        "West300":['T3_W_300_1'],
        "NorthLoop":['e1det_331667964#3_1'],
        "EastLoop":['e1det_37573561#2_1'],
        "SouthLoop":['e1det_-331667964#4_1'],
        "WestLoop":['e1det_-37573561#3_1'],
        "NorthLoopArea":['e2detLoop_331667964#3_1'],
        "EastLoopArea":['e2detLoop_37573561#2_1'],
        "SouthLoopArea":['e2detLoop_-331667964#4_1'],
        "WestLoopArea":['e2detLoop_-37573561#3_1'],
    },
    2:
        {
        "TrafficLightId":"cluster_4150067911_440015670",
        "North100":['e2det_-167186112#4_1','T4_N_100_1'],
        "East100":['e2det_37555809#7_1','T4_E_100_1'],
        "South100":['e2det_167186112#2_1'],
        "West100":['e2det_167584430#0_1'],
        "North300":['T4_N_300_1'],
        "East300":[],
        "South300":['T4_S_300_1','T4_S_300_2','T4_S_300_3'],
        "West300":['T4_W_300_1'],
        "NorthLoop":['e1det_-167186112#4_1'],
        "EastLoop":['e1det_37555809#7_1'],
        "SouthLoop":['e1det_167186112#2_1'],
        "WestLoop":['e1det_167584430#0_1'],
        "NorthLoopArea":['e2detLoop_-167186112#4_1'],
        "EastLoopArea":['e2detLoop_37555809#7_1'],
        "SouthLoopArea":['e2detLoop_167186112#2_1'],
        "WestLoopArea":['e2detLoop_167584430#0_1'],
    },
    3:
        {
        "TrafficLightId":"440015779",
        "North100":['e2det_331667964#1_1','T5_N_100_1'],
        "East100":['e2det_-37555823#2_1','T5_E_100_1'],
        "South100":['e2det_-331667964#2_1','T5_S_100_2','T5_S_100_1'],
        "West100":['e2det_37555823#1_1'],
        "North300":['T5_N_300_1'],
        "East300":['T5_E_300_1'],
        "South300":['T5_S_300_1','T5_S_300_2'],
        "West300":['T5_W_300_1','T5_W_300_2'],
        "NorthLoop":['e1det_331667964#1_1'],
        "EastLoop":['e1det_-37555823#2_1'],
        "SouthLoop":['e1det_-331667964#2_1'],
        "WestLoop":['e1det_37555823#1_1'],
        "NorthLoopArea":['e2detLoop_331667964#1_1'],
        "EastLoopArea":['e2detLoop_-37555823#2_1'],
        "SouthLoopArea":['e2detLoop_-331667964#2_1'],
        "WestLoopArea":['e2detLoop_37555823#1_1'],
    },
    6:
        {
        "TrafficLightId":"cluster_3379602111_440015591",
        "North100":['e2det_-320244139#11_1','T6_N_100_1'],
        "East100":['e2det_167468132#3_1'],
        "South100":['e2det_320244139#9_1','T6_S_100_1','T6_S_100_2'],
        "West100":['e2det_330925771#2_1'],
        "North300":['T6_N_300_1','T6_N_300_2','T6_N_300_3'],
        "East300":['T6_E_300_1'],
        "South300":['T6_S_300_1','T6_S_300_2','T6_S_300_3'],
        "West300":['T6_W_300_1','T6_W_300_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_-320244139#11_1'],
        "EastLoopArea":['e2detLoop_167468132#3_1'],
        "SouthLoopArea":['e2detLoop_320244139#9_1'],
        "WestLoopArea":['e2detLoop_330925771#2_1'],
    },
    7:
        {
        "TrafficLightId":"cluster_1788560793_1788560794_1788560801_1788560803",
        "North100":['e2det_167461554#2_2','e2det_167461554#2_1'],
        "East100":['e2det_172932752#17_2','e2det_172932752#17_1'],
        "South100":['e2det_167468375#1_1','e2det_167468375#1_2','T7_S_100_1','T7_S_100_2','T7_S_100_3'],
        "West100":['e2det_167462415#3_1','e2det_167462415#3_2'],
        "North300":['T7_N_300_1','T7_N_300_2','T7_N_300_3','T7_N_300_4'],
        "East300":['T7_E_300_1','T7_E_300_2','T7_E_300_4','T7_E_300_3','T7_E_300_5','T7_E_300_6'],
        "South300":['T7_S_300_1','T7_S_300_2'],
        "West300":['e2det300_167462415#3_2','e2det300_167462415#3_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167461554#2_2','e2detLoop_167461554#2_1'],
        "EastLoopArea":['e2detLoop_172932752#17_2','e2detLoop_172932752#17_1'],
        "SouthLoopArea":['e2detLoop_167468375#1_2','e2detLoop_167468375#1_1'],
        "WestLoopArea":['e2detLoop_167462415#3_1','e2detLoop_167462415#3_2'],
    },
    8:
        {
        "TrafficLightId":"cluster_3242190339_3433844334",
        "North100":['e2det_167462414_2','e2det_167462414_1','T8_N_100_1','T8_N_100_2'],
        "East100":['e2det_-336337248_1'],
        "South100":['e2det_317891653#2_1','e2det_317891653#2_2','T8_S_100_3','T8_S_100_4'],
        "West100":['e2det_-335563875#0_1'],
        "North300":['T8_N_300_1','T8_N_300_2'],
        "East300":['e2det300_-336337248_1'],
        "South300":[],
        "West300":['e2det300_-335563875#0_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167462414_2','e2detLoop_167462414_1'],
        "EastLoopArea":['e2detLoop_-336337248_1'],
        "SouthLoopArea":['e2detLoop_317891653#2_2','e2detLoop_317891653#2_1'],
        "WestLoopArea":['e2detLoop_-335563875#0_1'],
    },
    9:
        {
        "TrafficLightId":"cluster_1788554984_1788554987_1788554991_1788554995_1788554996_1788554997_1788555000_1788555001_1788555008_6876795489",
        "North100":['e2det_37358087#7_2','e2det_37358087#7_1'],
        "East100":['e2det_167458863#5_2','e2det_167458863#5_1'],
        "South100":['e2det_167461557#1_1','e2det_167461557#1_2'],
        "West100":['e2det_167461552#2_2','e2det_167461552#2_1'],
        "North300":['e2det300_37358087#7_2','e2det300_37358087#7_1','T9_N_300_1','T9_N_300_2'],
        "East300":['T9_E_300_1','T9_E_300_2'],
        "South300":['T9_S_300_1','T9_S_300_2'],
        "West300":['e2det300_167461552#2_2','e2det300_167461552#2_1','T9_W_300_1','T9_W_300_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_37358087#7_2','e2detLoop_37358087#7_1'],
        "EastLoopArea":['e2detLoop_167458863#5_2','e2detLoop_167458863#5_1'],
        "SouthLoopArea":['e2detLoop_167461557#1_2','e2detLoop_167461557#1_1'],
        "WestLoopArea":['e2detLoop_167461552#2_2','e2detLoop_167461552#2_1'],
    },
    10:
        {
        "TrafficLightId":"cluster_1788546056_1788546069",
        "North100":['e2det_36907454#0_1'],
        "East100":['e2det_167458863#2_2','e2det_167458863#2_1','T10_N_100_2','T10_N_100_1','T10_N_100_4','T10_N_100_3'],
        "South100":['e2det_-757229692_1'],
        "West100":['e2det_167456692#0_1','e2det_167456692#0_2'],
        "North300":['e2det300_36907454#0_1'],
        "East300":[],
        "South300":['e2det300_-757229692_1'],
        "West300":['e2det300_167456692#0_1','e2det300_167456692#0_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_36907454#0_1'],
        "EastLoopArea":['e2detLoop_167458863#2_2','e2detLoop_167458863#2_1'],
        "SouthLoopArea":['e2detLoop_-757229692_1'],
        "WestLoopArea":['e2detLoop_167456692#0_2','e2detLoop_167456692#0_1'],
    },
    11:
        {
        "TrafficLightId":"cluster_1788546015_1788554993_1788555007_428785798_6970932738",
        "North100":['e2det_167459400#2_2','e2det_167459400#2_1'],
        "East100":['e2det_172932752#14_2','e2det_172932752#14_1','T11_E_100_2','T11_E_100_1'],
        "South100":['e2det_166753092#5_1','e2det_166753092#5_2'],
        "West100":['e2det_173008341#1_1','e2det_173008341#1_2'],
        "North300":['e2det300_167459400#2_1','e2det300_167459400#2_2','T11_N_300_1','T11_N_300_2','T11_N_300_3','T11_N_300_4'],
        "East300":['T11_E_300_1','T11_E_300_2'],
        "South300":['e2det300_166753092#5_2','e2det300_166753092#5_1'],
        "West300":['T11_W_300_1','T11_W_300_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167459400#2_2','e2detLoop_167459400#2_1'],
        "EastLoopArea":['e2detLoop_172932752#14_2','e2detLoop_172932752#14_1'],
        "SouthLoopArea":['e2detLoop_166753092#5_2','e2detLoop_166753092#5_1'],
        "WestLoopArea":['e2detLoop_173008341#1_2','e2detLoop_173008341#1_1'],
    },
    12:
        {
        "TrafficLightId":"cluster_3236242165_3236242170",
        "North100":['e2det_36907635#6_1'],
        "East100":['e2det_317371668#2_1'],
        "South100":['e2det_-36907635#8_1','T12_S_100_1'],
        "West100":['e2det_331656505_1'],
        "North300":['e2det300_36907635#6_1'],
        "East300":[],
        "South300":['T12_S_300_1','T12_S_300_2','T12_S_300_3','T12_S_300_4'],
        "West300":['e2det300_331656505_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_36907635#6_1'],
        "EastLoopArea":['e2detLoop_317371668#2_1'],
        "SouthLoopArea":['e2detLoop_-36907635#8_1'],
        "WestLoopArea":['e2detLoop_331656505_1'],
    },
    13:
        {
        "TrafficLightId":"cluster_1788519120_1788519122_1788519128_1788519149_1788519159_1788519178",
        "North100":['e2det_-36897741#0_1'],
        "East100":['e2det_317766697#1_2','e2det_317766697#1_1'],
        "South100":['e2det_167456691_1'],
        "West100":['e2det_167456697_1','e2det_167456697_2'],
        "North300":['T13_N_300_1','e2det300_167456697_2','e2det300_167456697_1'],
        "East300":['e2det300_317766697#1_2','e2det300_317766697#1_1','T13_E_300_2','T13_E_300_1'],
        "South300":[],
        "West300":['T13_W_300_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_-36897741#0_1'],
        "EastLoopArea":['e2detLoop_317766697#1_2','e2detLoop_317766697#1_1'],
        "SouthLoopArea":['e2detLoop_167456691_1'],
        "WestLoopArea":['e2detLoop_167456697_2','e2detLoop_167456697_1'],
    },
    14:
        {
        "TrafficLightId":"cluster_1788524083_cluster_1788524073_1788524076_1788524078_1788524081_1788524082_5424475813",
        "North100":['e2det_167456698#1_2','e2det_167456698#1_1'],
        "East100":['e2det_167457328_2','e2det_167457328_1','T14_E_100_2','T14_E_100_1'],
        "South100":['e2det_167458864_1','e2det_167458864_2'],
        "West100":['e2det_167456692#2_1','e2det_167456692#2_2'],
        "North300":[],
        "East300":['T10_E_300_1','T10_E_300_2'],
        "South300":[],
        "West300":[],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167456698#1_2','e2detLoop_167456698#1_1'],
        "EastLoopArea":['e2detLoop_167457328_2','e2detLoop_167457328_1'],
        "SouthLoopArea":['e2detLoop_167458864_2','e2detLoop_167458864_1'],
        "WestLoopArea":['e2detLoop_167456692#2_2','e2detLoop_167456692#2_1'],
    },
    15:
        {
        "TrafficLightId":"cluster_1788519156_1788519160_1788519172_1788519181_1788519208",
        "North100":['e2det_167456088#1_2','e2det_167456088#1_1'],
        "East100":['e2det_331667211#1_1'],
        "South100":['e2det_36897741#1_1'],
        "West100":['e2det_-167457329_1','e2det_-167457329_2'],
        "North300":['e2det300_167456088#1_1','e2det300_167456088#1_2'],
        "East300":['e2det300_331667211#1_1'],
        "South300":['e2det300_36897741#1_1'],
        "West300":['e2det300_-167457329_1','e2det300_-167457329_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167456088#1_2','e2detLoop_167456088#1_1'],
        "EastLoopArea":['e2detLoop_331667211#1_1'],
        "SouthLoopArea":['e2detLoop_36897741#1_1'],
        "WestLoopArea":['e2detLoop_-167457329_2','e2detLoop_-167457329_1'],
    },
    16:
        {
        "TrafficLightId":"429231701",
        "North100":['e2det_-36907637#2_1'],
        "East100":['e2det_331667211#0_1'],
        "South100":['e2det_36907637#1_1'],
        "West100":['e2det_-361576970_1'],
        "North300":[],
        "East300":['e2det300_331667211#0_1'],
        "South300":[],
        "West300":['e2det300_-361576970_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_-36907637#2_1'],
        "EastLoopArea":['e2detLoop_331667211#0_1'],
        "SouthLoopArea":['e2detLoop_36907637#1_1'],
        "WestLoopArea":['e2detLoop_-361576970_1'],
    },
    17:
        {
        "TrafficLightId":"428785779",
        "North100":['e2det_36907635#5_1'],
        "East100":['e2det_36907357#1_1'],
        "South100":['e2det_-36907635#6_1'],
        "West100":['e2det_-331667211#0_1'],
        "North300":[],
        "East300":[],
        "South300":['e2det300_-36907635#6_1'],
        "West300":[],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_36907635#5_1'],
        "EastLoopArea":['e2detLoop_36907357#1_1'],
        "SouthLoopArea":['e2detLoop_-36907635#6_1'],
        "WestLoopArea":['e2detLoop_-331667211#0_1'],
    },
    18:
        {
        "TrafficLightId":"cluster_1788512752_1788512753_1788512755_1788512757_1788512765_1788512771_1788512775_5295041468",
        "North100":['e2det_167456090#1_2','e2det_167456090#1_1'],
        "East100":['e2det_-167456093_2','e2det_-167456093_1'],
        "South100":['e2det_167456092#1_2','e2det_167456092#1_1'],
        "West100":['e2det_167456695#1_1','e2det_167456695#1_2','e2det_167456695#1_3','e2det_167456695#1_4'],
        "North300":['e2det300_167456090#1_1','e2det300_167456090#1_2'],
        "East300":['e2det300_-167456093_2','e2det300_-167456093_1'],
        "South300":['e2det300_167456092#1_2','e2det300_167456092#1_1'],
        "West300":['e2det300_167456695#1_4','e2det300_167456695#1_1','e2det300_167456695#1_2','e2det300_167456695#1_3'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167456090#1_1','e2detLoop_167456090#1_2'],
        "EastLoopArea":['e2detLoop_-167456093_2','e2detLoop_-167456093_1'],
        "SouthLoopArea":['e2detLoop_167456092#1_2','e2detLoop_167456092#1_1'],
        "WestLoopArea":['e2detLoop_167456695#1_1','e2detLoop_167456695#1_2','e2detLoop_167456695#1_3','e2detLoop_167456695#1_4'],
    },
    19:
        {
        "TrafficLightId":"GS_cluster_1781956430_1781956432_1781956434_1781956435",
        "North100":['e2det_167584432#5_1','e2det_167584432#5_2'],
        "East100":['e2det_244327260#3_1','e2det_244327260#3_0'],
        "South100":['e2det_167584711#0_2','e2det_167584711#0_1'],
        "West100":['e2det_166954897#0_1','e2det_166954897#0_0'],
        "North300":['T19_N_300_1','T19_N_300_2'],
        "East300":['e2det300_244327260#3_0','e2det300_244327260#3_1'],
        "South300":['e2det300_167584711#0_2','e2det300_167584711#0_1'],
        "West300":['e2det300_166954897#0_0','e2det300_166954897#0_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_167584432#5_2','e2detLoop_167584432#5_1'],
        "EastLoopArea":['e2detLoop_244327260#3_1','e2detLoop_244327260#3_0'],
        "SouthLoopArea":['e2detLoop_167584711#0_2','e2detLoop_167584711#0_1'],
        "WestLoopArea":['e2detLoop_166954897#0_1','e2detLoop_166954897#0_0'],
    },
    20:
        {
        "TrafficLightId":"cluster_1789797911_1789797912",
        "North100":['e2det_166753096#5_1','e2det_166753096#5_0'],
        "East100":['e2det_167585225#0_2','e2det_167585225#0_1','T20_E_100_1'],
        "South100":['e2det_29375467#1_1','e2det_29375467#1_0'],
        "West100":['e2det_-167585225#2_2','e2det_-167585225#2_1','T20_W_100_2','T20_W_100_1','T20_W_100_4','T20_W_100_3','T20_W_100_5'],
        "North300":[],
        "East300":['T20_E_300_1'],
        "South300":['e2det300_29375467#1_1','e2det300_29375467#1_0'],
        "West300":['T20_W_300_1'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_166753096#5_1','e2detLoop_166753096#5_0'],
        "EastLoopArea":['e2detLoop_167585225#0_2','e2detLoop_167585225#0_1'],
        "SouthLoopArea":['e2detLoop_29375467#1_1','e2detLoop_29375467#1_0'],
        "WestLoopArea":['e2detLoop_-167585225#2_2','e2detLoop_-167585225#2_1'],
    },
    21:
        {
        "TrafficLightId":"cluster_1781970405_1781970409_1781970412_1781970417_1781970432_1781970433_1781970438_1781970457_1781978770_1781978772_1781978775_1781978779_3316796882",
        "North100":['e2det_166753093#0_1','e2det_166753093#0_2'],
        "East100":['e2det_244329796#19_2','e2det_244329796#19_1'],
        "South100":['e2det_29376270#2_1','e2det_29376270#2_0','e2det_325004668#2_1'],
        "West100":['e2det_166954897#7_0','e2det_166954897#7_1','T21_W_100_1','T21_W_100_2','T21_W_100_3','T21_W_100_4'],
        "North300":['T21_N_300_2','T21_N_300_1','T21_N_300_3','T21_N_300_4','T21_N_300_5','T21_N_300_6'],
        "East300":['e2det300_244329796#19_1','e2det300_244329796#19_2','T21_E_300_2','T21_E_300_1','T21_E_300_3','T21_E_300_4','T21_E_300_5','T21_E_300_6'],
        "South300":['e2det300_29376270#2_1','e2det300_29376270#2_0','e2det300_325004668#2_1'],
        "West300":['T21_W_300_1','T21_W_300_2','T21_W_300_3','T21_W_300_4'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_166753093#0_2','e2detLoop_166753093#0_1'],
        "EastLoopArea":['e2detLoop_244329796#19_2','e2detLoop_244329796#19_1'],
        "SouthLoopArea":['e2detLoop_29376270#2_1','e2detLoop_29376270#2_0','e2detLoop_325004668#2_1'],
        "WestLoopArea":['e2detLoop_166954897#7_1','e2detLoop_166954897#7_0'],
    },
    22:
        {
        "TrafficLightId":"440015546",
        "North100":['e2det_-166753092#4_2','e2det_-166753092#4_1','T22_N_100_2','T22_N_100_1'],
        "East100":['e2det_-167589230#2_1'],
        "South100":['e2det_166753092#3_2','e2det_166753092#3_1'],
        "West100":['e2det_167589230#1_1','T22_W_100_1'],
        "North300":['T22_N_300_1','T22_N_300_2'],
        "East300":['T22_E_300_1'],
        "South300":['T22_S_300_1','T22_S_300_2','T22_S_300_3','T22_S_300_4'],
        "West300":[],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_-166753092#4_2','e2detLoop_-166753092#4_1'],
        "EastLoopArea":['e2detLoop_-167589230#2_1'],
        "SouthLoopArea":['e2detLoop_166753092#3_2','e2detLoop_166753092#3_1'],
        "WestLoopArea":['e2detLoop_167589230#1_1'],
    },
    23:
        {
        "TrafficLightId":"cluster_1782342942_1782342945",
        "North100":['e2det_-166753911#0_1','T23_N_100_1'],
        "East100":['e2det_244329796#14_2','e2det_244329796#14_1'],
        "South100":['e2det_324991740#4_1'],
        "West100":['e2det_244327259#5_2','e2det_244327259#5_1'],
        "North300":['T23_N_300_1'],
        "East300":['e2det300_244329796#14_1','e2det300_244329796#14_2','T23_E_300_1','T23_E_300_2'],
        "South300":['e2det300_324991740#4_1'],
        "West300":['e2det300_244327259#5_2','e2det300_244327259#5_1','T23_W_300_1','T23_W_300_2'],
        "NorthLoop":[''],
        "EastLoop":[''],
        "SouthLoop":[''],
        "WestLoop":[''],
        "NorthLoopArea":['e2detLoop_-166753911#0_1'],
        "EastLoopArea":['e2detLoop_244329796#14_2','e2detLoop_244329796#14_1'],
        "SouthLoopArea":['e2detLoop_324991740#4_1'],
        "WestLoopArea":['e2detLoop_244327259#5_2','e2detLoop_244327259#5_1'],
    }


}


throughputLoopDetector = ['outgoing1', 'outgoing2', 'outgoing3', 'outgoing4', 'outgoing5', 'outgoing6', 'outgoing7', 'outgoing8', 'outgoing9', 'outgoing10', 'outgoing11', 'outgoing12', 'outgoing13', 'outgoing14', 'outgoing15', 'outgoing16', 'outgoing17', 'outgoing18', 'outgoing19', 'outgoing20', 'outgoing21', 'outgoing22', 'outgoing23', 'outgoing24', 'outgoing25', 'outgoing26', 'outgoing27', 'outgoing28', 'outgoing29', 'outgoing30', 'outgoing31', 'outgoing32', 'outgoing33', 'outgoing34', 'outgoing35', 'outgoing36', 'outgoing37', 'outgoing38', 'outgoing39', 'outgoing40', 'outgoing41', 'outgoing42', 'outgoing43', 'outgoing44', 'outgoing45', 'outgoing46', 'outgoing47', 'outgoing48', 'outgoing49', 'outgoing50', 'outgoing51', 'outgoing52', 'outgoing53', 'outgoing54', 'outgoing55', 'outgoing56', 'outgoing57', 'outgoing58', 'outgoing59', 'outgoing60', 'outgoing61', 'outgoing62', 'outgoing63',
                          'outgoing64', 'outgoing65', 'outgoing66', 'outgoing67', 'outgoing68', 'outgoing69', 'outgoing70', 'outgoing71', 'outgoing72', 'outgoing73', 'outgoing74', 'outgoing75', 'outgoing76', 'outgoing77', 'outgoing78', 'outgoing79', 'outgoing80', 'outgoing81', 'outgoing82', 'outgoing83', 'outgoing84', 'outgoing85', 'outgoing86', 'outgoing87', 'outgoing88', 'outgoing89', 'outgoing90', 'outgoing91', 'outgoing92', 'outgoing93', 'outgoing94', 'outgoing95', 'outgoing96', 'outgoing97', 'outgoing98', 'outgoing99', 'outgoing100', 'outgoing101', 'outgoing102', 'outgoing103', 'outgoing104', 'outgoing105', 'outgoing106', 'outgoing107', 'outgoing108', 'outgoing109', 'outgoing110', 'outgoing111', 'outgoing112', 'outgoing113', 'outgoing114', 'outgoing115', 'outgoing116', 'outgoing117', 'outgoing118', 'outgoing119', 'outgoing120', 'outgoing121', 'outgoing122', 'outgoing123', 'outgoing124', 'outgoing125', 'outgoing126', 'outgoing127', 'outgoing128', 'outgoing129', 'outgoing130', 'outgoing131', 'outgoing132', 'outgoing133', 'outgoing134', 'outgoing135', 'outgoing136', 'outgoing137', 'outgoing138', 'outgoing139', 'outgoing140', 'outgoing141', 'outgoing142', 'outgoing143', 'outgoing144', 'outgoing145', 'outgoing146', 'outgoing148', 'outgoing150', 'outgoing151', 'outgoing152', 'outgoing153', 'outgoing154', 'outgoing155', 'outgoing156', 'outgoing157', 'outgoing158', 'outgoing159', 'outgoing160', 'outgoing161', 'outgoing162', 'outgoing163', 'outgoing164', 'outgoing165', 'outgoing166', 'outgoing167', 'outgoing168']
class DetectorsInTraffic:
    # global variables for evaluation
    def __init__(self,TrafficLightId,n100,e100,s100,w100,n300,e300,s300,w300,loop_n,
                 loop_e,loop_s,loop_w,loop_area_n,loop_area_e,loop_area_s,loop_area_w):
        self.totalWaitingTime = { "North": 0,"East": 0, "South": 0, "West":0 }
        self.totalQueueLenth = {"North": 0, "East": 0, "South": 0, "West": 0}
        self.totalCoEmission = {"North": 0, "East": 0, "South": 0, "West": 0}
        self.totalCo2Emission = {"North": 0, "East": 0, "South": 0, "West": 0}
        self.totalThroughput = {"North": 0, "East": 0, "South": 0, "West": 0}
        self.vehicleList = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.vehicleListForUppaal = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.queueLength = [0, 0, 0, 0]
        self.previousWaitingTime = 0
        self.currentGreenTime = [0, 0, 0, 0]
        self.maxGreenTime = [120, 120, 120, 120]
        self.loopCurrentGreenTime = [0, 0, 0, 0]
        self.loopMaxGreenTime = [55, 45, 55, 45]
        self.extendGreen = False
        self.curPhase = 1  # North
        self.nextPhase = 1  # North
        self.detectorNames = {
        "TrafficLightId":TrafficLightId,
        "North100": n100,
        "East100": e100,
        "South100": s100,
        "West100": w100,
        "North300": n300,
        "East300": e300,
        "South300": s300,
        "West300": w300,
        "NorthLoop":loop_n,
        "EastLoop": loop_e,
        "SouthLoop": loop_s,
        "WestLoop": loop_w,
        "NorthLoopArea": loop_area_n,
        "EastLoopArea": loop_area_e,
        "SouthLoopArea": loop_area_s,
        "WestLoopArea": loop_area_w
        }
    def getData(self, func, dets):
        numDet = len(dets)
        res = [0] * numDet
        for deti in range(0, numDet):
            res[deti] = func(dets[deti])
        return res
    def getVehicleTypes(self,directionName,need_waiting_time,need_queue_length,need_emission,need_thorughput):
        detectorsList = self.detectorNames[directionName]
        numDet = len(detectorsList)
        res = [0] * numDet
        queueLenth = 0
        coEmission = 0
        co2Emission = 0
        waitingVehicles = [0,0,0,0]  # Bus,Car, Auto, MotorCycle
        arrivingVehicles = [0, 0, 0, 0]  # Bus,Car, Auto, MotorCycle
        throughput = [0,0,0,0]
        for deti in range(0,  numDet):
            # print("Vehicle Types",traci.lanearea.getLastStepVehicleIDs(detectorsList[deti]))
            res[deti]=list(traci.lanearea.getLastStepVehicleIDs(detectorsList[deti]))
            # print("Queue length:", traci.lanearea.getJamLengthMeters(detectorsList[deti]))
            queueLenth = queueLenth + traci.lanearea.getJamLengthMeters(detectorsList[deti])
            for vht in range(len(res[deti])):
                # res[deti][vht].getWaitingTime

                # print("Hei CO emission",traci.vehicle.getCOEmission(res[deti][vht]))
                # print("Hei CO2 emission", traci.vehicle.getCO2Emission(res[deti][vht]))
                coEmission = coEmission + traci.vehicle.getCOEmission(res[deti][vht])
                co2Emission = co2Emission + traci.vehicle.getCO2Emission(res[deti][vht])
                if "Bus" in res[deti][vht]:
                    if traci.vehicle.getWaitingTime(res[deti][vht]) >= 1.0:
                        waitingVehicles[0] = waitingVehicles[0] + 1
                    else:
                        arrivingVehicles[0] = arrivingVehicles[0] + 1
                if "Car" in res[deti][vht]:
                    if traci.vehicle.getWaitingTime(res[deti][vht]) >= 1.0:
                        waitingVehicles[1] = waitingVehicles[1] + 1
                    else:
                        arrivingVehicles[1] = arrivingVehicles[1] + 1
                if "Auto" in res[deti][vht]:
                    if traci.vehicle.getWaitingTime(res[deti][vht]) >= 1.0:
                        waitingVehicles[2] = waitingVehicles[2] + 1
                    else:
                        arrivingVehicles[2] = arrivingVehicles[2] + 1
                if "MotorCycle" in res[deti][vht]:
                    if traci.vehicle.getWaitingTime(res[deti][vht]) >= 1.0:
                        waitingVehicles[3] = waitingVehicles[3] + 1
                    else:
                        arrivingVehicles[3] = arrivingVehicles[3] + 1


             # calculate waiting time for vehicles
        if need_waiting_time:
            if directionName == 'North100' or directionName == 'North300' :
                self.totalWaitingTime['North'] = self.totalWaitingTime['North'] + sum(waitingVehicles)
                # print("Total waiting time:",directionName,self.totalWaitingTime['North'])
            if directionName == 'East100' or directionName == 'East300' :
                self.totalWaitingTime['East'] = self.totalWaitingTime['East'] + sum(waitingVehicles)
            if directionName == 'South100' or directionName == 'South300' :
                self.totalWaitingTime['South'] = self.totalWaitingTime['South'] + sum(waitingVehicles)
            if directionName == 'West100' or directionName == 'West300' :
                self.totalWaitingTime['West'] = self.totalWaitingTime['West'] + sum(waitingVehicles)
             # calculate emission for vehicles
        if need_emission:
            if directionName == 'North100' or directionName == 'North300' :
                self.totalCoEmission['North'] = self.totalCoEmission['North'] + coEmission
                self.totalCo2Emission['North'] = self.totalCo2Emission['North'] + co2Emission
            if directionName == 'East100' or directionName == 'East300' :
                self.totalCoEmission['East'] = self.totalCoEmission['East'] + coEmission
                self.totalCo2Emission['East'] = self.totalCo2Emission['East'] + co2Emission
            if directionName == 'South100' or directionName == 'South300' :
                self.totalCoEmission['South'] = self.totalCoEmission['South'] + coEmission
                self.totalCo2Emission['South'] = self.totalCo2Emission['South'] + co2Emission
            if directionName == 'West100' or directionName == 'West300' :
                self.totalCoEmission['West'] = self.totalCoEmission['West'] + coEmission
                self.totalCo2Emission['West'] = self.totalCo2Emission['West'] + co2Emission
            # calculate queue length for vehicles
        if need_queue_length:
            if directionName == 'North100' or directionName == 'North300' :
                self.totalQueueLenth['North'] = self.totalQueueLenth['North'] + queueLenth
            if directionName == 'East100' or directionName == 'East300' :
                self.totalQueueLenth['East'] = self.totalQueueLenth['East'] + queueLenth
            if directionName == 'South100' or directionName == 'South300' :
                self.totalQueueLenth['South'] = self.totalQueueLenth['South'] + queueLenth
            if directionName == 'West100' or directionName == 'West300' :
                self.totalQueueLenth['West'] = self.totalQueueLenth['West'] + queueLenth
        # print("Total waiting time:",self.totalWaitingTime)
        # print("totalCoEmission:",self.totalCoEmission)
        # print("totalCo2Emission:", self.totalCo2Emission)
        # print("Total queue length:",self.totalQueueLenth)
        return waitingVehicles,arrivingVehicles,queueLenth


    def getVehicleType(self,directionName,need_waiting_time,need_queue_length,need_emission,need_thorughput):
        return self.getVehicleTypes(directionName,need_waiting_time,need_queue_length,need_emission,need_thorughput)
    def getWaitingTimeTotal(self):
        allDetectors = ['North100', 'East100', 'South100', 'West100', 'North300', 'East300', 'South300', 'West300']
        totalTime = 0
        for directions in allDetectors:
            wv,av,ql = self.getVehicleTypes(directions, True, False, False, False)
            # totalTime = totalTime + wv
        return totalTime

    def getQueueLengthTotal(self):
        allDetectors = ['North100', 'East100', 'South100', 'West100', 'North300', 'East300', 'South300', 'West300']
        queueLen = 0
        for directions in allDetectors:
            wv, av, ql =  self.getVehicleTypes(directions, False, True, False, False)
        return int(queueLen)

    def getArrivingVehicles(self,directionName):
        # return self.getData(traci.lanearea.getLastStepVehicleNumber, self.detectorNames[directionName])
        waitingVeh,ArrivingVeh,ql = self.getVehicleTypes(directionName, True, False, False, False)
        return ArrivingVeh
    def getVehiclesList(self,directionName):
        directionName1,directionName2 = directionName[0],directionName[1]
        # return self.getData(traci.lanearea.getLastStepVehicleNumber, self.detectorNames[directionName])
        waitingVeh,ArrivingVeh,ql = self.getVehicleTypes(directionName1, True, True, True, False)
        waitingVeh2, ArrivingVeh2,ql = self.getVehicleTypes(directionName2, True, True, True, False)
        waitingVehNp = np.array(waitingVeh)
        waitingVehNp = 2 * waitingVehNp
        vehicleList1 = waitingVehNp + ArrivingVeh
        vehicleListNp = np.array(vehicleList1)
        waitingVehNp2 = np.array(waitingVeh2)
        waitingVehNp2 = 2 * waitingVehNp2
        vehicleList2 = waitingVehNp + ArrivingVeh
        vehicleList = 2 * vehicleListNp + vehicleList2
        return vehicleList
    def getVehiclesListForUppaalStratego(self,directionName):
        directionName1,directionName2 = directionName[0],directionName[1]
        # return self.getData(traci.lanearea.getLastStepVehicleNumber, self.detectorNames[directionName])
        waitingVeh,ArrivingVeh,ql = self.getVehicleTypes(directionName1, False, False, False, False)
        waitingVeh2, ArrivingVeh2,ql = self.getVehicleTypes(directionName2, False, False, False, False)
        waitingVehNp = np.array(waitingVeh)
        waitingVehNp = 1 * waitingVehNp
        vehicleList1 = waitingVehNp + ArrivingVeh
        vehicleListNp = np.array(vehicleList1)
        waitingVehNp2 = np.array(waitingVeh2)
        waitingVehNp2 = 1 * waitingVehNp2
        vehicleList2 = waitingVehNp + ArrivingVeh
        vehicleList = 1 * vehicleListNp + vehicleList2
        return vehicleList
    def getQueueLength(self,directionName):
        directionName1, directionName2 = directionName[0], directionName[1]
        waitingVeh, ArrivingVeh, ql = self.getVehicleTypes(directionName1, False, True, False, False)
        return int(ql)

    def getLoopAreaDetector(self):
        detectorValues = [0,0,0,0]
        for i in range(4):
            detectorValues[i] = sum(self.getData(traci.lanearea.getLastStepVehicleNumber, self.detectorNames[loopAreaDirection[i]]))
        return detectorValues

    def getLoopDetector(self,directionName):
        return self.getData(traci.inductionloop.getLastStepVehicleNumber, self.detectorNames[directionName])

d= DetectorsInTraffic(100,trafficData[1]['North100'],trafficData[1]['East100'],trafficData[1]['South100'],trafficData[1]['West100'],
                      trafficData[1]['North300'],trafficData[1]['East300'],trafficData[1]['South300'],trafficData[1]['West300'],
                      ['tra1','traff'],['tra1'],['tra1'],['tra1'],['tra1','traff'],['tra1'],['tra1'],['tra1'])

trafficLight = list()
for i in range(1,24):

    trafficLight.append( DetectorsInTraffic(trafficData[i]['TrafficLightId'],
                       trafficData[i]['North100'], trafficData[i]['East100'], trafficData[i]['South100'],trafficData[i]['West100'],
                       trafficData[i]['North300'], trafficData[i]['East300'],trafficData[i]['South300'],trafficData[i]['West300'],
                       trafficData[i]['NorthLoop'], trafficData[i]['EastLoop'],trafficData[i]['SouthLoop'], trafficData[i]['WestLoop'],
                       trafficData[i]['NorthLoopArea'], trafficData[i]['EastLoopArea'],trafficData[i]['SouthLoopArea'], trafficData[i]['WestLoopArea']
                       ))

# print(d.getWaitingCars("North100"))
def updateGreenTimer(i,cPhase,value,checkZero):
    # print("Green time updation:",i,int(cPhase),value,checkZero)
    if cPhase == 1:
        if checkZero:
            trafficLight[i].currentGreenTime[0] = 0
        else:
            trafficLight[i].currentGreenTime[0] = trafficLight[i].currentGreenTime[0] + value
    if cPhase == 2:
        if checkZero:
            trafficLight[i].currentGreenTime[1] = 0
        else:
            trafficLight[i].currentGreenTime[1] = trafficLight[i].currentGreenTime[1] + value
    if cPhase == 3:
        if checkZero:
            trafficLight[i].currentGreenTime[2] = 0
        else:
            trafficLight[i].currentGreenTime[2] = trafficLight[i].currentGreenTime[2] + value
    if cPhase == 4:
        # print("cphase==4")
        if checkZero:
            # print("check zero and update current green time zero")
            trafficLight[i].currentGreenTime[3] = 0
        else:
            trafficLight[i].currentGreenTime[3] = trafficLight[i].currentGreenTime[3] + value

def exceptDirection(direction_1,detectorValues):
    count = 0
    for direc in range(4):
        if direc != direction_1:
            if detectorValues[direc] == 0:
                count = count + 1

    return count

def getThroughput(func, dets):
    numDet = len(dets)
    res = [0] * numDet
    for deti in range(0,numDet):
        res[deti] = func(dets[deti])
    return res


def actuatedController(index,loopAreaDetectors,delay,prevPhase):
    currentPhase = 0
    for direc in range(4):
     if loopAreaDetectors[direc] >= 1:
        if trafficLight[index].loopCurrentGreenTime[direc] < trafficLight[index].loopMaxGreenTime[direc]:
            currentPhase = queuePhases[direc]
            trafficLight[index].loopCurrentGreenTime[direc] = trafficLight[index].loopCurrentGreenTime[direc]  + delay
            break
        else:
            checking = exceptDirection(direc,loopAreaDetectors)
            # if checking == 3:
            #     trafficLight[index].loopCurrentGreenTime[direc] = 0
            # else:
            #     m = max(loopAreaDetectors)
            #     resetList = [i for i, j in enumerate(loopAreaDetectors) if j == m]
            #     if trafficLight[index].loopCurrentGreenTime[resetList[0]] >= trafficLight[index].loopMaxGreenTime[resetList[0]] and \
            #             trafficLight[index].loopCurrentGreenTime[prevPhase] >= trafficLight[index].loopMaxGreenTime[prevPhase]:
            #         trafficLight[index].loopCurrentGreenTime[resetList[0]] = 0

        if trafficLight[index].loopCurrentGreenTime[0] > trafficLight[index].loopMaxGreenTime[0] and trafficLight[index].loopCurrentGreenTime[1] > trafficLight[index].loopMaxGreenTime[1] and trafficLight[index].loopCurrentGreenTime[2] > trafficLight[index].loopMaxGreenTime[2] and trafficLight[index].loopCurrentGreenTime[3] > trafficLight[index].loopMaxGreenTime[3]:
            trafficLight[index].loopCurrentGreenTime = [0,0,0,0]


    return currentPhase


def converPhase(cPhase):
    sumoPhase = 0
    if cPhase == 1:
        sumoPhase = 0
    if cPhase == 2:
        sumoPhase = 2
    if cPhase == 3:
        sumoPhase = 4
    if cPhase == 4:
        sumoPhase = 6
    return sumoPhase
def calculateTravelTime(vehIdsList):
    for vehId in vehIdsList:
        if traci.vehicle.getSpeed(vehId) < 0.1:
            if not vehId in waitingTimeOfVehcile.keys():
                waitingTimeOfVehcile[vehId] = 0
            else:
                waitingTimeOfVehcile[vehId] = waitingTimeOfVehcile[vehId]  + 1
        if traci.vehicle.isStopped(vehId) == True:
            print("Some are stopped",vehId)
            if not vehId in noOfStops.keys():
                noOfStops[vehId] = 0
            else:
                noOfStops[vehId] = noOfStops[vehId]  + 1
        # print("Vehicle Id", vehId)
def conHetroHomo(vehicleList):
    newList = []
    for i, array in enumerate(vehicleList):
        newList.append(sum(array))
    return newList
def prevPhaseConvert(prevPhase):
    if prevPhase == 0:
        return 0
    if prevPhase == 2:
        return 1
    if prevPhase == 4:
        return  2
    if prevPhase == 6:
        return 3
def run():
    noOfTrafficLights = 22
    print("%s controller is working in %s now............." %(options.controller,options.load))
    intelligentTimer = 0
    areaTimer = 0
    delay = 5
    actuatedTimer = delay
    throughputFinal = 0
    actuatedCurrentPhase = np.zeros(23,dtype=int)
    loopPrevPhase = np.zeros(23, dtype=int)
    # print("actuatedCurrentPhase",actuatedCurrentPhase)
    step = 0
    timeVerJammedCars = []
    for i in range(0, noOfTrafficLights):
        traci.trafficlights.setProgram(trafficLight[i].detectorNames['TrafficLightId'], 'High')
    # while traci.simulation.getMinExpectedNumber() > 0:
    # while step <= 100:
    while step <= int(options.step):
        # print("step:",step)
        step = step + 1
        print("-------------------------------Step--------------------------------: ",step)
        throughput = getThroughput(traci.inductionloop.getLastStepVehicleNumber, throughputLoopDetector)
        throughputFinal = throughputFinal + sum(throughput)
        # print("Outgoing Loop Detectors:",throughput )
        traci.simulationStep()
        vehicleCount = 0
        # # CALCULATE VEHICLE STOPS COUNT AND TRAVEL TIME
        # vehIdsList = traci.vehicle.getIDList()
        # calculateTravelTime(vehIdsList)
        # print("--------------------------- Waiting Time --------------------")
        # print(waitingTimeOfVehcile)
        # print("Number of stops:",noOfStops)
        for i in range(0, noOfTrafficLights):
            # calculate waiting time
            twt1 = 0
            # print("Before previous waiting time:",i+1,trafficLight[i].previousWaitingTime)
            for direc in directions:
                twt1 = twt1 + trafficLight[i].totalWaitingTime[direc]
            vehicleCount = vehicleCount + (twt1 - trafficLight[i].previousWaitingTime)
            trafficLight[i].previousWaitingTime = twt1
            # print("After previous wating time:",i+1,trafficLight[i].previousWaitingTime)
            # print("Current waiting vehicles count:",timeVerJammedCars)
            trafficLight[i].getWaitingTimeTotal()
            trafficLight[i].getQueueLengthTotal()
            # print("Total waiting time:",i+1,trafficLight[i].totalWaitingTime)
            # print("Total queue length:",i+1,trafficLight[i].totalQueueLenth)
            vehicleList = []
            vehicleListForUppaal = []
            queueLen = []
            for direction in directions:
                vehicleList.append(list(trafficLight[i].getVehiclesList(directionDict[direction])))
                queueLen.append(trafficLight[i].getQueueLength(directionDict[direction]))

            for direction in directions:
                vehicleListForUppaal.append(list(trafficLight[i].getVehiclesListForUppaalStratego(directionDict[direction])))
            trafficLight[i].vehicleList = vehicleList
            trafficLight[i].vehicleListForUppaal = vehicleListForUppaal
            trafficLight[i].queueLength = queueLen
            # print("Vehicle List:",i+1,vehicleList)
            # print("Queue Length:",i+1,queueLen)
        timeVerJammedCars.append(vehicleCount)
        # print("Jammed Cars with time:",timeVerJammedCars)


            # --------------------------------------------- FULLY ACTUATED CONTROLLER -----------------------------------------------
        # if True:
        if options.controller == "Actuated":
            if actuatedTimer <= 0:
             for j in range(0, noOfTrafficLights):
                    # print("Loop detector value:", j + 1, trafficLight[j].getLoopDetector('NorthLoop'))
                    print("Loop Area Detector:",j+1,trafficLight[j].getLoopAreaDetector())
                    loopAreaValue = trafficLight[j].getLoopAreaDetector()
                    actuatedCurrentPhase[j] = actuatedController(j,loopAreaValue,delay,loopPrevPhase[j])
                    loopPrevPhase[j] = prevPhaseConvert(actuatedCurrentPhase[j])
                    actuatedTimer = delay
                    print("Updated current phase:",j+1,actuatedCurrentPhase[j])
                    print("Current Green Time:",j+1,trafficLight[j].loopCurrentGreenTime)
                    print("Max Green Time:", j + 1, trafficLight[j].loopMaxGreenTime)

            else:
             for j in range(0, noOfTrafficLights):
                    print("Current Phase:",j+1,actuatedCurrentPhase[j])
                    traci.trafficlights.setPhase(trafficLight[j].detectorNames['TrafficLightId'],actuatedCurrentPhase[j])
                    actuatedTimer = actuatedTimer - 1
        # -------------------------------- INTELLIGENT CONTROLLER ---------------------------------------------------
        if options.controller == "Intelligent":
        # if False: # intelligent
            traci.trafficlights.setPhase(trafficLight[8].detectorNames['TrafficLightId'],0)
            if intelligentTimer == 0 and step > 50:
                # print("step here ",int(options.step) )
                for i in range(0, noOfTrafficLights):
                    print("%s vehicles are waiting in %s intersection:" % (trafficLight[i].vehicleList, i + 1))
                    if trafficLight[i].extendGreen:
                        trafficLight[i].nextPhase = callUnCoorIntelController(
                            trafficLight[i].vehicleList,trafficLight[i].queueLength,trafficLight[i].currentGreenTime,
                            trafficLight[i].maxGreenTime,trafficLight[i].extendGreen,trafficLight[i].curPhase)
                        print("Next Phase:",trafficLight[i].nextPhase)
                        # print("Current Phase:",trafficLight[i].curPhase)
                        if trafficLight[i].curPhase == trafficLight[i].nextPhase:
                            trafficLight[i].extendGreen = True
                            updateGreenTimer(i,trafficLight[i].curPhase,5,False)
                        else:
                            trafficLight[i].extendGreen = False
                            updateGreenTimer(i,trafficLight[i].curPhase,5,True)
                        trafficLight[i].curPhase = trafficLight[i].nextPhase
                        # intelligentTimer = 5
                    else:
                        trafficLight[i].nextPhase = callUnCoorIntelController(
                            trafficLight[i].vehicleList, trafficLight[i].queueLength, trafficLight[i].currentGreenTime,
                            trafficLight[i].maxGreenTime, trafficLight[i].extendGreen, trafficLight[i].curPhase)
                        print("Next Phase:", trafficLight[i].nextPhase)
                        # print("Current Phase:",trafficLight[i].curPhase)
                        trafficLight[i].curPhase = trafficLight[i].nextPhase
                        # intelligentTimer = 5
                        trafficLight[i].extendGreen = True
                        updateGreenTimer(i, trafficLight[i].curPhase, 5, True)
                intelligentTimer = 5

            else:
                for i in range(0, noOfTrafficLights):
                    print("Current Phase %s in Traffic Light %s" %(trafficLight[i].curPhase,i+1))
                    print("Current Phase converted %s in Traffic Light %s" %(converPhase(trafficLight[i].curPhase),i+1))
                    traci.trafficlights.setPhase(trafficLight[i].detectorNames['TrafficLightId'], converPhase(trafficLight[i].curPhase))
                if intelligentTimer < 0:
                    intelligentTimer = 0
                else:
                    intelligentTimer = intelligentTimer - 1
                # print("Intelligent Green Timer for %s: %s"%(i+1,trafficLight[i].currentGreenTime))

        # -------------------------------- UPPAAL STRATEGO CONTROLLER ---------------------------------------------------
        if options.controller == "UppaalStratego":
            # if False: # intelligent
            if intelligentTimer == 0 and step > 50:
                # print("%s vehicles in intelligent are waiting in %s intersection:" % (trafficLight[i].vehicleList, i + 1))
                for i in range(0, noOfTrafficLights):
                    print("%s vehicles are waiting in %s intersection:" % (trafficLight[i].vehicleListForUppaal, i + 1))
                    if i == 20 or i == 21:
                        if i == 20:
                            pass
                    else:
                        if trafficLight[i].extendGreen:
                            print("Vehicle list:", trafficLight[i].vehicleListForUppaal)
                            trafficLight[i].nextPhase = callUppaalStratego(
                                trafficLight[i].vehicleListForUppaal, trafficLight[i].queueLength, trafficLight[i].currentGreenTime,
                                trafficLight[i].maxGreenTime, trafficLight[i].extendGreen, trafficLight[i].curPhase)
                            print("Next Phase:", trafficLight[i].nextPhase)
                            # print("Current Phase:", trafficLight[i].curPhase)
                            if trafficLight[i].curPhase == trafficLight[i].nextPhase:
                                trafficLight[i].extendGreen = True
                                updateGreenTimer(i, trafficLight[i].curPhase, 5, False)
                            else:
                                trafficLight[i].extendGreen = False
                                updateGreenTimer(i, trafficLight[i].curPhase, 5, True)
                            trafficLight[i].curPhase = trafficLight[i].nextPhase
                        else:
                            print("Vehicle list:",trafficLight[i].vehicleListForUppaal )
                            trafficLight[i].nextPhase = callUppaalStratego(
                                trafficLight[i].vehicleListForUppaal, trafficLight[i].queueLength, trafficLight[i].currentGreenTime,
                                trafficLight[i].maxGreenTime, trafficLight[i].extendGreen, trafficLight[i].curPhase)
                            print("Next Phase:", trafficLight[i].nextPhase)
                            # print("Current Phase:", trafficLight[i].curPhase)
                            trafficLight[i].curPhase = trafficLight[i].nextPhase
                            trafficLight[i].extendGreen = True
                            updateGreenTimer(i, trafficLight[i].curPhase, 8, True)
                intelligentTimer = 8

            else:
                for i in range(0, noOfTrafficLights):
                    traci.trafficlights.setPhase(trafficLight[i].detectorNames['TrafficLightId'],
                                                 converPhase(trafficLight[i].curPhase))
                if intelligentTimer < 0:
                    intelligentTimer = 0
                else:
                    intelligentTimer = intelligentTimer - 1
                    # print("Intelligent Green Timer for %s: %s" % (i + 1, trafficLight[i].currentGreenTime))

            # -------------------------------- COORDINATED INTELLIGENT CONTROLLER ---------------------------------------------------
        if options.controller == "CoordinatedIntelligent_1":
            # if False: # intelligent
            # Area Controller starts here
            if areaTimer == 0 and step > 100:
                print("----------------  Area Controller is started   ---------------")
                totalVehicleList_1 = []
                totalVehicleList_2 = []
                totalVehicleList_3 = []
                totalVehicleList_4 = []
                for ik in range(0,5):
                    totalVehicleList_1.append(conHetroHomo(trafficLight[ik].vehicleList))
                print("checking here area cont - 1:",conHetroHomo(trafficLight[0].vehicleList))
                print("total vehicle list:",totalVehicleList_1)
                areaGreenTime_1 = callAreaController_1(totalVehicleList_1)
                trafficLight[0].maxGreenTime = [areaGreenTime_1[0:4]]
                trafficLight[1].maxGreenTime = [areaGreenTime_1[4:8]]
                trafficLight[2].maxGreenTime = [areaGreenTime_1[8:12]]
                trafficLight[3].maxGreenTime = [areaGreenTime_1[12:16]]
                trafficLight[4].maxGreenTime = [areaGreenTime_1[16:20]]

                for ik in range(5, 10):
                    totalVehicleList_2.append(conHetroHomo(trafficLight[ik].vehicleList))
                print("checking here area cont - 2:", conHetroHomo(trafficLight[5].vehicleList))
                print("total vehicle list:", totalVehicleList_2)
                areaGreenTime_2 = callAreaController_2(totalVehicleList_2)
                trafficLight[5].maxGreenTime = [areaGreenTime_2[0:4]]
                trafficLight[6].maxGreenTime = [areaGreenTime_2[4:8]]
                trafficLight[7].maxGreenTime = [areaGreenTime_2[8:12]]
                trafficLight[8].maxGreenTime = [areaGreenTime_2[12:16]]
                trafficLight[9].maxGreenTime = [areaGreenTime_2[16:20]]

                for ik in range(10, 18):
                    totalVehicleList_3.append(conHetroHomo(trafficLight[ik].vehicleList))
                print("checking here area cont - 3:", conHetroHomo(trafficLight[10].vehicleList))
                print("total vehicle list:", totalVehicleList_3)
                areaGreenTime_3 = callAreaController_3(totalVehicleList_3)
                trafficLight[10].maxGreenTime = [areaGreenTime_3[0:4]]
                trafficLight[11].maxGreenTime = [areaGreenTime_3[4:8]]
                trafficLight[12].maxGreenTime = [areaGreenTime_3[8:12]]
                trafficLight[13].maxGreenTime = [areaGreenTime_3[12:16]]
                trafficLight[14].maxGreenTime = [areaGreenTime_3[16:20]]
                trafficLight[15].maxGreenTime = [areaGreenTime_3[20:24]]
                trafficLight[16].maxGreenTime = [areaGreenTime_3[24:28]]
                trafficLight[17].maxGreenTime = [areaGreenTime_3[28:32]]


                for ik in range(18, 23):
                    totalVehicleList_4.append(conHetroHomo(trafficLight[ik].vehicleList))
                print("checking here area cont - 4:", conHetroHomo(trafficLight[18].vehicleList))
                print("total vehicle list:", totalVehicleList_4)
                areaGreenTime_4 = callAreaController_4(totalVehicleList_4)
                trafficLight[18].maxGreenTime = [areaGreenTime_4[0:4]]
                trafficLight[10].maxGreenTime = [areaGreenTime_4[4:8]]
                trafficLight[20].maxGreenTime = [areaGreenTime_4[8:12]]
                trafficLight[21].maxGreenTime = [areaGreenTime_4[12:16]]
                trafficLight[22].maxGreenTime = [areaGreenTime_4[16:20]]

                areaTimer_check = random.randint(1, 9)
                areaTimer = num1 = 20 * areaTimer_check
                print("-------------------Green Time is updated from Area Controller ---------------------------------")
            else:
                if areaTimer < 0:
                    areaTimer = 0
                else:
                    areaTimer = areaTimer - 1

            if intelligentTimer == 0 and step > 10:
                for i in range(0, noOfTrafficLights):
                    print("%s vehicles are waiting in %s intersection:" % (trafficLight[i].vehicleListForUppaal, i + 1))
                    if trafficLight[i].extendGreen:
                        trafficLight[i].nextPhase = callCoorIntelController(
                            trafficLight[i].vehicleList, trafficLight[i].queueLength,
                            trafficLight[i].currentGreenTime,
                            trafficLight[i].maxGreenTime, trafficLight[i].extendGreen, trafficLight[i].curPhase)
                        print("Next Phase:", trafficLight[i].nextPhase)
                        # print("Current Phase:", trafficLight[i].curPhase)
                        if trafficLight[i].curPhase == trafficLight[i].nextPhase:
                            trafficLight[i].extendGreen = True
                            updateGreenTimer(i, trafficLight[i].curPhase, 5, False)
                        else:
                            trafficLight[i].extendGreen = False
                            updateGreenTimer(i, trafficLight[i].curPhase, 5, True)
                        trafficLight[i].curPhase = trafficLight[i].nextPhase

                    else:
                        trafficLight[i].nextPhase = callCoorIntelController(
                            trafficLight[i].vehicleList, trafficLight[i].queueLength,
                            trafficLight[i].currentGreenTime,
                            trafficLight[i].maxGreenTime, trafficLight[i].extendGreen, trafficLight[i].curPhase)
                        print("Next Phase:", trafficLight[i].nextPhase)
                        # print("Current Phase:", trafficLight[i].curPhase)
                        trafficLight[i].curPhase = trafficLight[i].nextPhase
                        trafficLight[i].extendGreen = True
                        updateGreenTimer(i, trafficLight[i].curPhase, 5, True)
                intelligentTimer = 5

            else:
                for i in range(0, noOfTrafficLights):
                    traci.trafficlights.setPhase(trafficLight[i].detectorNames['TrafficLightId'],
                                                 converPhase(trafficLight[i].curPhase))
                    print("Intelligent current Green Timer for %s: %s" % (i + 1, trafficLight[i].currentGreenTime))
                    print("Intelligent Maximum Green Timer for %s: %s" % (i + 1, trafficLight[i].maxGreenTime))
                if intelligentTimer < 0:
                    intelligentTimer = 0
                else:
                    intelligentTimer = intelligentTimer - 1


    globalTotalWT = 0
    globalTotalQL = 0
    globalTotalCo = 0
    globalTotalCo2 = 0
    detWaitingTime = np.arange(23)
    for i in range(0,noOfTrafficLights):
        twt = tql = tco = tco2 = 0
        print("------------------------------------------------------------------------------------------------------")
        for direc in directions:
            twt = twt + trafficLight[i].totalWaitingTime[direc]
            tql = tql + trafficLight[i].totalQueueLenth[direc]
            tco = tco + trafficLight[i].totalCoEmission[direc]
            tco2 = tco2 + trafficLight[i].totalCo2Emission[direc]
        detWaitingTime[i] = twt
        globalTotalWT = globalTotalWT + twt
        globalTotalQL = globalTotalQL + tql
        globalTotalCo = globalTotalCo + tco
        globalTotalCo2 = globalTotalCo2 + tco2
        print("Total Waiting Time:",i+1,twt)
        print("Total Queue Length:",i+1,tql)
        print("Total Co Emission :",i+1,tco)
        print("Total Co2 Emisiion:",i+1,tco2)
    print("---------------------------------------------------------------------------------------------")
    print("Total WT Hrs :",globalTotalWT/3600)
    detWaitingTime = np.around(detWaitingTime / 1, 2)
    print("Total QL km*Sec:",globalTotalQL/1000)
    print("Total CO gms :", globalTotalCo/1000)
    print("Total CO2 gms:", globalTotalCo2/1000)
    print("Total TP no.Veh/sec:",throughputFinal/int(options.step))
    traci.close()
    # detWaitingTime = np.arange(20)
    # detQueueLength = np.arange(20)
    # #
    # for i in range(20):
    #     print("In Traffic light %s: %s Hours" % (i + 1, trafficLight[i].totalWaitingTime))
    #     detWaitingTime[i] = trafficLight[i].totalWaitingTime
    #     detQueueLength[i] = trafficLight[i].totalQueueLength
    # detWaitingTime = np.around(detWaitingTime / 3600, 2)
    # detQueueLength = np.around(detQueueLength / 1000, 2)
    # print("Waiting time from detectors:", sum(detWaitingTime))
    # print("Queue length from detectors:", sum(detQueueLength))
    # print("time verses cars:", timeVerJammedCars)
    # writing required data into file
    # plottingPurpose.writeToFile("trafficWaiting.csv", stepPerLoad)
    print("Total jammed cars:", sum(timeVerJammedCars))
    calculateWaitingTime.writingPlottingData(detWaitingTime, options.controller + "Bar", options.load)
    calculateWaitingTime.writingPlottingData(timeVerJammedCars, options.controller + "Line", options.load)
    plottingPurpose.writeResult(globalTotalCo, globalTotalCo2, globalTotalWT,
                                globalTotalQL , throughputFinal/int(options.step),
                                options.controller + options.step + "-" + options.load, True)

    sys.stdout.flush()


# def get_options(controllerNameEx):
#     optParser = optparse.OptionParser()
#     controllerName = ("Intelligent","Fixed-Time","Actuated")
#     optParser.add_option("--nogui", action="store_true",
#                          default=False, help="run the commandline version of sumo")
#     optParser.add_option("--controller", type="string", dest="controller", default= controllerNameEx)
#     optParser.add_option("--step", type="string", dest="step", default="200")
#     optParser.add_option("--load", type="string", dest="load", default="Case1High")
#     options, args = optParser.parse_args()
#     return options


# this is the main entry point of this script
# if __name__ == "__main__":
#
#     # controllerName = ("Intelligent","Fixed-Time", "Actuated")
#     controllerName = ['Fixed-Time']
#     for i in controllerName:
#         options = get_options(i)
#         if options.nogui:
#             sumoBinary = checkBinary('sumo')
#         else:
#             sumoBinary = checkBinary('sumo-gui')
#         traci.start([sumoBinary, "-c", "dataFiles/fourPhases.sumocfg"],label="static")
#         run()
def get_options(controllerNameEx,cases):
    optParser = optparse.OptionParser()
    controllerName = ("Intelligent","Fixed-Time","Actuated")
    optParser.add_option("--nogui", action="store_true",
                         default=True, help="run the commandline version of sumo")
    optParser.add_option("--controller", type="string", dest="controller", default= controllerNameEx)
    optParser.add_option("--step", type="string", dest="step", default="1200")
    optParser.add_option("--load", type="string", dest="load", default=cases)
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":

    controllerName = ('Fixed-Time', 'Actuated','UppaalStratego','Intelligent','CoordinatedIntelligent_1')
    cases = ["Case1Low","Case1Mid","Case1High","Case2","Case3","Case4"]
    controllerName = ['Intelligent']
    cases = ['Case1High']
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

