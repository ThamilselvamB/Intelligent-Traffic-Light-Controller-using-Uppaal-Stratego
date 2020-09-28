from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random
#  "518.38,517.78 501.38,517.78"
# we need to import python modules from the directory
sys.path.append(os.path.join('c:', os.sep, 'usr', 'share', 'sumo', 'tools'))
from sumolib import checkBinary  # import library
import traci
import numpy as np


class Configuration:
    def __init__(self, cases):
        start = 1
        end = 27
        # majorRoad = 1500
        # minorRoad = 750
        # leftTurn = 100
        # crossRoad = 600

        self.cases=cases
        self.tcH = {}
        self.routeH = {}
        self.pH = {}
        if cases == "Case1Low":
            multiplier = 0.3
            route_1_AmpliToVaishnamdevi = 999
            route_2AmpliToVaishnamdevi = 999
            route_3GandhinagarToShrikaei = 1156
            route_4GandhinagarToShrikaei = 1156
            route_5NavaNarodatoZundal = 912
            route_6NavaNarodatoZundal = 912
            route_7CGRoadtoUshmanpura = 1375
            route_8CGRoadtoUshmanpura = 1375
            route_9CGRoadtoUshmanpura = 912
            route_10CGRoadtoUshmanpura = 912
            route_11CGRoadtoUshmanpura = 912
            route_12CGRoadtoUshmanpura = 912
            route_13CGRoadtoUshmanpura = 912
            route_14CGRoadtoUshmanpura = 912
            route_15CGRoadtoUshmanpura = 816
            route_16CGRoadtoUshmanpura = 816
            route_17CGRoadtoUshmanpura = 750
            route_18CGRoadtoUshmanpura = 750
            route_19CGRoadtoUshmanpura = 912
            route_20CGRoadtoUshmanpura = 912
            route_21CGRoadtoUshmanpura = 1923
            route_22CGRoadtoUshmanpura = 1923
            route_23CGRoadtoUshmanpura = 1229
            route_24CGRoadtoUshmanpura = 1229
            route_25CGRoadtoUshmanpura = 816
            route_26CGRoadtoUshmanpura = 816

            crossRoad = 300
        if cases == "Case1Mid":
            multiplier = 0.6
            route_1_AmpliToVaishnamdevi = 999
            route_2AmpliToVaishnamdevi = 999
            route_3GandhinagarToShrikaei = 1156
            route_4GandhinagarToShrikaei = 1156
            route_5NavaNarodatoZundal = 912
            route_6NavaNarodatoZundal = 912
            route_7CGRoadtoUshmanpura = 1375
            route_8CGRoadtoUshmanpura = 1375
            route_9CGRoadtoUshmanpura = 912
            route_10CGRoadtoUshmanpura = 912
            route_11CGRoadtoUshmanpura = 912
            route_12CGRoadtoUshmanpura = 912
            route_13CGRoadtoUshmanpura = 912
            route_14CGRoadtoUshmanpura = 912
            route_15CGRoadtoUshmanpura = 816
            route_16CGRoadtoUshmanpura = 816
            route_17CGRoadtoUshmanpura = 750
            route_18CGRoadtoUshmanpura = 750
            route_19CGRoadtoUshmanpura = 912
            route_20CGRoadtoUshmanpura = 912
            route_21CGRoadtoUshmanpura = 1923
            route_22CGRoadtoUshmanpura = 1923
            route_23CGRoadtoUshmanpura = 1229
            route_24CGRoadtoUshmanpura = 1229
            route_25CGRoadtoUshmanpura = 816
            route_26CGRoadtoUshmanpura = 816
        if cases == "Case1High":
            multiplier = 1.0
            route_1_AmpliToVaishnamdevi = 999
            route_2AmpliToVaishnamdevi = 999
            route_3GandhinagarToShrikaei = 1156
            route_4GandhinagarToShrikaei = 1156
            route_5NavaNarodatoZundal = 912
            route_6NavaNarodatoZundal = 912
            route_7CGRoadtoUshmanpura = 1375
            route_8CGRoadtoUshmanpura = 1375
            route_9CGRoadtoUshmanpura = 912
            route_10CGRoadtoUshmanpura = 912
            route_11CGRoadtoUshmanpura = 912
            route_12CGRoadtoUshmanpura = 912
            route_13CGRoadtoUshmanpura = 912
            route_14CGRoadtoUshmanpura = 912
            route_15CGRoadtoUshmanpura = 816
            route_16CGRoadtoUshmanpura = 816
            route_17CGRoadtoUshmanpura = 750
            route_18CGRoadtoUshmanpura = 750
            route_19CGRoadtoUshmanpura = 912
            route_20CGRoadtoUshmanpura = 912
            route_21CGRoadtoUshmanpura = 1923
            route_22CGRoadtoUshmanpura = 1923
            route_23CGRoadtoUshmanpura = 1229
            route_24CGRoadtoUshmanpura = 1229
            route_25CGRoadtoUshmanpura = 816
            route_26CGRoadtoUshmanpura = 816
        if cases == "Case2":
            multiplier = 1.0
            majorRoad = 1600
            minorRoad = 1000
            leftTurn = 100
            crossRoad = 300
        if cases == "Case3":
            multiplier = 1.0
            majorRoad = 850
            minorRoad = 850
            leftTurn = 100
            crossRoad = 300
        if cases == "Case4":
            multiplier = 1.0
            majorRoad = 450
            minorRoad = 750
            leftTurn = 100
            crossRoad = 300

        self.pH1 = np.ones(1)*multiplier * route_1_AmpliToVaishnamdevi / 3600
        self.pH2 = np.ones(1) * multiplier * route_2AmpliToVaishnamdevi / 3600
        self.pH3 = np.ones(1) * multiplier * route_3GandhinagarToShrikaei / 3600
        self.pH4 = np.ones(1) * multiplier * route_4GandhinagarToShrikaei / 3600
        self.pH5 = np.ones(1) * multiplier * route_5NavaNarodatoZundal / 3600
        self.pH6 = np.ones(1) * multiplier * route_6NavaNarodatoZundal / 3600
        self.pH7 = np.ones(1) * multiplier * route_7CGRoadtoUshmanpura / 3600
        self.pH8 = np.ones(1) * multiplier * route_8CGRoadtoUshmanpura / 3600
        self.pH9 = np.ones(1) * multiplier * route_9CGRoadtoUshmanpura / 3600
        self.pH10 = np.ones(1) * multiplier * route_10CGRoadtoUshmanpura / 3600
        self.pH11 = np.ones(1) * multiplier * route_11CGRoadtoUshmanpura / 3600
        self.pH12 = np.ones(1) * multiplier * route_12CGRoadtoUshmanpura / 3600
        self.pH13 = np.ones(1) * multiplier * route_13CGRoadtoUshmanpura / 3600
        self.pH14 = np.ones(1) * multiplier * route_14CGRoadtoUshmanpura / 3600
        self.pH15 = np.ones(1) * multiplier * route_15CGRoadtoUshmanpura / 3600
        self.pH16 = np.ones(1) * multiplier * route_16CGRoadtoUshmanpura / 3600
        self.pH17 = np.ones(1) * multiplier * route_17CGRoadtoUshmanpura / 3600
        self.pH18 = np.ones(1) * multiplier * route_18CGRoadtoUshmanpura / 3600
        self.pH19 = np.ones(1) * multiplier * route_19CGRoadtoUshmanpura / 3600
        self.pH20 = np.ones(1) * multiplier * route_20CGRoadtoUshmanpura / 3600
        self.pH21 = np.ones(1) * multiplier * route_21CGRoadtoUshmanpura / 3600
        self.pH22 = np.ones(1) * multiplier * route_22CGRoadtoUshmanpura / 3600
        self.pH23 = np.ones(1) * multiplier * route_23CGRoadtoUshmanpura / 3600
        self.pH24 = np.ones(1) * multiplier * route_24CGRoadtoUshmanpura / 3600
        self.pH25 = np.ones(1) * multiplier * route_25CGRoadtoUshmanpura / 3600
        self.pH26 = np.ones(1) * multiplier * route_26CGRoadtoUshmanpura / 3600
        self.pH27 = np.ones(1) * multiplier * route_26CGRoadtoUshmanpura / 3600

        self.pH = np.hstack((self.pH1 , self. pH2,self.pH3,self.pH4,self.pH5 , self. pH6,self.pH7,self.pH8,self.pH9 , self. pH10,self.pH11,self.pH12,self.pH13 , self. pH14,self.pH15,self.pH16,
                             self.pH17, self.pH18, self.pH19, self.pH20,self.pH21 , self. pH22,self.pH23,self.pH24,self.pH25 , self. pH26,self.pH27))
        self.routeH = []
        for i in range(start,end):
            self.routeH.append("route_"+str(i) )
        # self.routeH = ["route_1","route_2","route_3","route_4","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1",
        #                "route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1","route_1"]

        # self.directions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19','20','1A', '2A', '3A', '4A', '5A', '6A', '7A', '8A', '9A', '10A', '11A', '12A','13A','14A','15A','16A','17A','18A','19A','20A']
        # self.nrDirections = len(self.directions)
#<route id="route_1" edges="168277061#0 168277061#1 168277061#3 168277061#4 168275829 168275547#1 168275547#2 547236215#0 547236215#2 547236215#4 547236215#5 168278390#0 168278390#1 168278390#2 168278390#3 168278390#4 547560317 168278394 168278393#1 168278393#2 168274448#1 168244316#0 168244316#1 168244316#3 168244316#4 168244316#5 168244316#6 168108873#2"/>
def generate_routefile(cases, outputfile,randomSeed):
    random.seed(randomSeed)  # make tests reproducible
    N = 1800  # number of time steps
    cf = Configuration(cases)
    # print(cf.pH)
    pBus = 5. / 100
    pCar = 20. / 100
    p3Wheel = 35. / 100
    p2Wheel = 40. / 100
    v_Types = ['Bus','Auto','MotorCycle','Car']
    with open("../dataFiles/"+outputfile, "w") as routes:
        totalCars = 0;
        print("""<routes>
    <vType id="Bus" accel="0.6" decel="3.5" sigma="0.5" length="10.1" minGap="1.0" maxSpeed="16.67" guiShape="bus" width="2.45" latAlignment="left" laneChangeModel="SL2015" lcStrategic="0.5" lcCooperative="0.0"/>
    <vType id="Auto" accel="0.7" decel="4.5" sigma="0.5" length="2.6" minGap="0.3" maxSpeed="16" guiShape="passenger/sedan" width="1.25" latAlignment="left" laneChangeModel="SL2015" lcStrategic="0.5" lcCooperative="0.0" />
    <vType id="MotorCycle" accel="0.9" decel="3.5" sigma="0.5" length="1.85" minGap="0.15" maxSpeed="17" guiShape="motorcycle" width="0.7" latAlignment="left" laneChangeModel="SL2015" lcStrategic="0.5" lcCooperative="0.0"/>
    <vType id="Car" accel="0.8" decel="4.5" sigma="0.5" length="3.6" minGap="0.5" maxSpeed="40" guiShape="passenger" width="1.5" latAlignment="left" laneChangeModel="SL2015" lcStrategic="0.5" lcCooperative="0.0"/>

	<route id="route_1" edges="167584711#0 167584434#1 167584434#2 167584434#3 167584434#4 167584434#5 167584434#6 167584434#8 167584434#9 167468131 167468375#0 167468375#1 167461557#0 167461557#1 167452030#0"/>
	<route id="route_2" edges="167452030#0 -358333263#1 -358333263#0 37358087#7 167461554#0 167461554#1 167461554#2 167468377#0 167468377#1 167468130 167468378#0 167468378#1 167584432#0 167584432#1 167584432#2 167584432#3 167584432#4 167584432#5 167584712"/>
	<route id="route_3" edges="-167456093 167456698#0 167456698#1 167458866 167457476#1 167457476#2 167457476#3 167459400#0 167459400#1 167459400#2 -166753092#6 -166753092#4 -166753092#3 -166753092#2 -166753092#1 -166753092#0 166753093#0 166753096#2 166753096#3 166753096#4 166753096#5 -167585225#0 -166800604#6 -166800604#5"/>
	<route id="route_4" edges="29375467#1 29376270#1 29376270#2 166753090#1 166753090#2 166753090#3 166753092#0 166753092#1 166753092#2 166753092#3 166753092#4 166753092#5 167459399#1 167459399#2 167459399#3 167457476#5 167457476#6 167457476#7 167458864 167456695#0 167456695#1 167456094"/>
	<route id="route_5" edges="167186112#0 167186112#1 167186112#2 167186112#4 167186112#5 331667958#2 320244139#3 320244139#5 320244139#6 320244139#7 320244139#8 320244139#9 320244139#11 320244139#12 320244139#13 645851118#3 317891653#2 317891653#3 167461551#5 167461551#0 167461551#1 167461552#0 335564510#0"/>
	<route id="route_6" edges="167461555 167461551#3 167462414 167462415#1 -645851118#3 -320244139#13 -320244139#12 -320244139#11 -320244139#9 -320244139#8 -320244139#7 -320244139#6 -320244139#5 -320244139#4 -331667958#2 -167186112#5 -167186112#4 -167186112#2 -167186112#1 -167186112#0"/>
	<route id="route_7" edges="324991740#4 166753911#0 166753911#1 166753911#2 172932752#5 -36907635#10 -36907635#9 -36907635#8 -36907635#6 -36907635#5 -36907635#4 -36907635#2 -36907635#0"/>
	<route id="route_8" edges="36907635#0 36907635#2 36907635#4 36907635#5 36907635#6 36907635#8 36907635#9 36907635#10 173008341#6 -166753911#2 -166753911#1 -166753911#0 -324991740#4"/>
	<route id="route_9" edges="167462465 167461551#1 167461552#0 167461552#1 167461552#2 167456692#0 167456692#1 167456692#2 -167457328 -167457329 -361576970 -331667211#0 -36907357#1"/>
	<route id="route_10" edges="36907357#1 331667211#0 331667211#1 167456693 167457328 167458863#0 167458863#2 167458863#3 167458863#4 167458863#5 167461555 167461551#3 167462414 335563875#0"/>
	<route id="route_11" edges="330925771#2 -167468132#3 -167468132#1 -167468132#0 167468375#1 167462409 173008341#1 173008341#4 173008341#5 173008341#6"/>
	<route id="route_12" edges="172932752#4 172932752#5 172932752#6 172932752#7 172932752#8 172932752#9 172932752#10 172932752#11 172932752#12 172932752#13 172932752#14 172932752#15 172932752#16 172932752#17 317891653#0 -330926044 -320244139#12 -320244139#11 -330925771#2"/>
	<route id="route_13" edges="331667958#0 331667958#1 331667958#2 331667958#3 331667958#4 331667958#5 331667958#7 37571582#1 167584430#6 167589223#0 167589223#1 167589223#3 257711537 -166753092#0 166753093#0 244327259#1 244327259#2 244327259#3 244327259#4 244327259#5 244327259#6 244329796#14"/>
	<route id="route_14" edges="244329796#13 244329796#14 244329796#15 244329796#16 244329796#17 244329796#18 244329796#19 166753090#1 166753090#2 166753090#3 166753092#0 -257711537 -167589223#3 -167589223#1 -167589223#0 167584434#8 -331667958#8 -331667958#7 -331667958#5 -331667958#4 -331667958#3 -331667958#2 -331667958#1 -331667958#0"/>
	<route id="route_15" edges="167584430#0 167584430#1 167584430#2 167584430#3 167584430#4 167584430#5 167584430#6 167589223#0 167589223#1 -167583193#2 167589230#0 167589230#1 167589230#2 167589230#3 167589230#4"/>
	<route id="route_16" edges="-167589230#4 -167589230#3 -167589230#2 -167589230#1 -167589230#0 167583193#2 -167589223#1 -167589223#0 37555809#2 37555809#3 37555809#4 37555809#5 37555809#6 37555809#7 -167186112#2"/>
	<route id="route_17" edges="37555829#0 167186112#1 167186112#2 167584430#1 167584430#2 167584430#3 167584430#4 167584430#5 167584430#6 167589223#0 167589223#1 167589223#3 257711537 -166753092#0 166753093#0 244327259#1 244327259#2 244327259#3 244327259#4"/>
	<route id="route_18" edges="244329796#16 244329796#17 244329796#18 244329796#19 166753090#1 166753090#2 166753090#3 166753092#0 -257711537 -167589223#3 -167589223#1 -167589223#0 37555809#2 37555809#3 37555809#4 37555809#5 37555809#6 37555809#7 -167186112#2 -167186112#1 -37555829#0"/>
	<route id="route_19" edges="166751738#1 166751738#3 167584433#1 167584433#2 167584433#3 -331667964#4 37573561#3 37573561#4 37573561#5 -37555807#1 -37555829#1 -37555829#0"/>
	<route id="route_20" edges="37555829#0 37555829#1 37555807#1 -37573561#5 -37573561#4 -37573561#3 -37573561#2 -37573561#1 -37573566#0 -167584433#2 -167584433#1 -167584433#0 -166751738#1"/>
	<route id="route_21" edges="166954897#0 166954897#3 166954897#4 166954897#5 166954897#6 166954897#7 244327259#1 244327259#2 244327259#3 244327259#4 244327259#5 244327259#6 244327259#7 -166753912#0"/>
	<route id="route_22" edges="244329796#13 244329796#14 244329796#15 244329796#16 244329796#17 244329796#18 244329796#19 244327260#2 244327260#3 244327260#6"/>
	<route id="route_23" edges="  167456697 36897741#0 "/>
	<route id="route_24" edges="317766697#1 167457326 "/>
	<route id="route_25" edges="317371668#1"/>
	<route id="route_27" edges="317371668#1 "/>
	<route id="route_26" edges="37571582#0 37571582#1 331667964#1 331667964#2 331667964#3 331667964#4 "/>
	
	
	

	<route id="route_28" edges="166954897#3"/>""",
              file=routes)
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            for j in range(len(cf.routeH)):
                # d = cf.directions[j]
                if random.uniform(0, 1) < cf.pH[j]:
                    route = cf.routeH[j]
                    # cf.tcH[d] = cf.tcH[d] + 1
                    k = random.randint(0, 3)
                    # if k == 0:
                    if random.uniform(0, 1) < pBus:
                        print('<vehicle id="%s_%i" type="Bus" route="%s" depart="%i" />' % (v_Types[k], vehNr, route, i),file=routes)
                        vehNr += 1
                    if random.uniform(0, 1) < p3Wheel:
                        print('<vehicle id="%s_%i" type="Auto" route="%s" depart="%i" />' % (v_Types[k], vehNr, route, i),
                              file=routes)
                        vehNr += 1
                    if random.uniform(0, 1) < p2Wheel:
                        print('<vehicle id="%s_%i" type="MotorCycle" route="%s" depart="%i" />' % (v_Types[k], vehNr, route, i),
                              file=routes)
                        vehNr += 1
                    if random.uniform(0, 1) < pCar:
                        print('<vehicle id="%s_%i" type="Car" route="%s" depart="%i" />' % (v_Types[k], vehNr, route, i),
                              file=routes)
                        vehNr += 1
                    # print('<vehicle id="%s_%i" type="Auto" route="%s" depart="%i" />' % (
                    #     route, vehNr, route, i), file=routes)
                    # vehNr += 1
                    lastVeh = i
        print('<!-- totalCars="%i -->' % (vehNr), file=routes)
        print('<!-- CarsPerDirection="%s -->' % (str(cf.tcH)), file=routes)
        print("</routes>", file=routes)
        # print(cf.tcH)
        print("Total cars Generated:",vehNr)


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--cases", type="string", dest="cases", default="Case1Low")
    optParser.add_option("--output", type="string", dest="output", default="fourPhases.rou.xml")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()
    generate_routefile(options.cases, options.output,32)
    # generate_routefileSimple()


