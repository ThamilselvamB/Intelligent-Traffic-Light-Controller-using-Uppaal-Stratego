#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    generateTLSE2Detectors.py
# @author  Daniel Krajzewicz
# @author  Karol Stosiek
# @author  Lena Kalleske
# @author  Michael Behrisch
# @date    2007-10-25
# @version $Id$

# from __future__ import absolute_import
# from __future__ import print_function
#
# import logging
# import optparse
# import os
# import sys
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import sumolib.xml  # noqa
# from sumolib import checkBinary  # noqa
# import traci  # noqa
#
# def adjust_detector_length(requested_detector_length,
#                            requested_distance_to_tls,
#                            lane_length):
#     """ Adjusts requested detector's length according to
#         the lane length and requested distance to TLS.
#
#         If requested detector length is negative, the resulting detector length
#         will match the distance between requested distance to TLS and lane
#         beginning.
#
#
#         If the requested detector length is positive, it will be adjusted
#         according to the end of lane ending with TLS: the resulting length
#         will be either the requested detector length or, if it's too long
#         to be placed in requested distance from TLS, it will be shortened to
#         match the distance between requested distance to TLS
#         and lane beginning. """
#
#     if requested_detector_length == -1:
#         return lane_length - requested_distance_to_tls
#
#     return min(lane_length - requested_distance_to_tls,
#                requested_detector_length)
#
#
# def adjust_detector_position(final_detector_length,
#                              requested_distance_to_tls,
#                              lane_length):
#     """ Adjusts the detector's position. If the detector's length
#         and the requested distance to TLS together are longer than
#         the lane itself, the position will be 0; it will be
#         the maximum distance from lane end otherwise (taking detector's length
#         and requested distance to TLS into accout). """
#
#     return max(0,
#                lane_length - final_detector_length - requested_distance_to_tls)
#
#
# if __name__ == "__main__":
#     # pylint: disable-msg=C0103
#
#     logging.basicConfig(level="INFO")
#
#     option_parser = optparse.OptionParser()
#     option_parser.add_option("-n", "--net-file",
#                              dest="net_file",
#                              help="Network file to work with. Mandatory.",
#                              type="string")
#     option_parser.add_option("-l", "--detector-length",
#                              dest="requested_detector_length",
#                              help="Length of the detector in meters "
#                              "(-1 for maximal length).",
#                              type="int",
#                              default=250)
#     option_parser.add_option("-d", "--distance-to-TLS",
#                              dest="requested_distance_to_tls",
#                              help="Distance of the detector to the traffic "
#                              "light in meters. Defaults to 0.1m.",
#                              type="float",
#                              default=.1)
#     option_parser.add_option("-f", "--frequency",
#                              dest="frequency",
#                              help="Detector's frequency. Defaults to 60.",
#                              type="int",
#                              default=60)
#     option_parser.add_option("-o", "--output",
#                              dest="output",
#                              help="The name of the file to write the detector "
#                              "definitions into. Defaults to e2.add.xml.",
#                              type="string",
#                              default="e2.add.xml")
#     option_parser.add_option("-r", "--results-file",
#                              dest="results",
#                              help="The name of the file the detectors write "
#                              "their output into. Defaults to e2output.xml.",
#                              type="string",
#                              default="incomingLoopDetectors.xml")
#     option_parser.set_usage("generateTLSE2Detectors.py -n example.net.xml "
#                             "-l 10 -d .1 -f 60")
#
#     (options, args) = option_parser.parse_args()
#     if not options.net_file:
#         print("Missing arguments")
#         option_parser.print_help()
#         exit()
#
#     logging.info("Reading net...")
#     net = sumolib.net.readNet(options.net_file)
#
#     logging.info("Generating detectors...")
#     detectors_xml = sumolib.xml.create_document("additional")
#     lanes_with_detectors = set()
#     lanes_with_detectors_1 = set()
#     for tls in net._tlss:
#         for connection in tls._connections:
#             lane = connection[0]
#             lane_length = lane.getLength()
#             lane_id = lane.getID()
#             print("lane edge co2:",lane.getEdge())
#             print("lane id co2:", lane.getID())
#
#             for lanes in lane.getIncoming():
#
#                 print("lane incoming:", lanes.getID())
#                 lane_id_1 = lanes.getID()
#                 ane_length_1 = lanes.getLength()
#
#                 if lane_id_1 in lanes_with_detectors_1:
#                     logging.warning("Detector for lane %s already generated" %
#                                     (str(lane_id_1)))
#                     continue
#                 lanes_with_detectors_1.add(lane_id_1)
#
#                 final_detector_length = adjust_detector_length(
#                     options.requested_detector_length,
#                     options.requested_distance_to_tls,
#                     ane_length_1)
#                 final_detector_position = adjust_detector_position(
#                     final_detector_length,
#                     options.requested_distance_to_tls,
#                     ane_length_1)
#
#                 detector_xml = detectors_xml.addChild("laneAreaDetector")
#                 detector_xml.setAttribute("file", options.results)
#                 detector_xml.setAttribute("freq", str(options.frequency))
#                 detector_xml.setAttribute("friendlyPos", "x")
#                 detector_xml.setAttribute("id", "e2det_" + str(lane_id_1)+str(lane_id_1))
#                 detector_xml.setAttribute("lane", str(lane_id_1))
#                 detector_xml.setAttribute("length", str(final_detector_length))
#                 detector_xml.setAttribute("pos", str(final_detector_position))
#
#             if lane_id in lanes_with_detectors:
#                 logging.warning("Detector for lane %s already generated" %
#                              (str(lane_id)))
#                 continue
#             lanes_with_detectors.add(lane_id)
#
#
#             logging.debug("Creating detector for lane %s" % (str(lane_id)))
#
#
#
#             final_detector_length = adjust_detector_length(
#                 options.requested_detector_length,
#                 options.requested_distance_to_tls,
#                 lane_length)
#             final_detector_position = adjust_detector_position(
#                 final_detector_length,
#                 options.requested_distance_to_tls,
#                 lane_length)
#             # detector_xml = detectors_xml.addChild("I am here ")
#             detector_xml = detectors_xml.addChild("laneAreaDetector")
#             detector_xml.setAttribute("file", options.results)
#             detector_xml.setAttribute("freq", str(options.frequency))
#             detector_xml.setAttribute("friendlyPos", "x")
#             detector_xml.setAttribute("id", "e2det_" + str(lane_id))
#             detector_xml.setAttribute("lane", str(lane_id))
#             detector_xml.setAttribute("length", str(final_detector_length))
#             detector_xml.setAttribute("pos", str(final_detector_position))
#
#
#     detector_file = open(options.output, 'w')
#     detector_file.write(detectors_xml.toXML())
#     detector_file.close()
#
#     logging.info("%d e2 detectors generated!" % len(lanes_with_detectors))
#
#


#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    generateTLSE2Detectors.py
# @author  Daniel Krajzewicz
# @author  Karol Stosiek
# @author  Lena Kalleske
# @author  Michael Behrisch
# @date    2007-10-25
# @version $Id$

# from __future__ import absolute_import
# from __future__ import print_function
#
# import logging
# import optparse
# import os
# import sys
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import sumolib.xml  # noqa
# from sumolib import checkBinary  # noqa
# import traci  # noqa
#
# def adjust_detector_length(requested_detector_length,
#                            requested_distance_to_tls,
#                            lane_length):
#     """ Adjusts requested detector's length according to
#         the lane length and requested distance to TLS.
#
#         If requested detector length is negative, the resulting detector length
#         will match the distance between requested distance to TLS and lane
#         beginning.
#
#
#         If the requested detector length is positive, it will be adjusted
#         according to the end of lane ending with TLS: the resulting length
#         will be either the requested detector length or, if it's too long
#         to be placed in requested distance from TLS, it will be shortened to
#         match the distance between requested distance to TLS
#         and lane beginning. """
#
#     if requested_detector_length == -1:
#         return lane_length - requested_distance_to_tls
#
#     return min(lane_length - requested_distance_to_tls,
#                requested_detector_length)
#
#
# def adjust_detector_position(final_detector_length,
#                              requested_distance_to_tls,
#                              lane_length):
#     """ Adjusts the detector's position. If the detector's length
#         and the requested distance to TLS together are longer than
#         the lane itself, the position will be 0; it will be
#         the maximum distance from lane end otherwise (taking detector's length
#         and requested distance to TLS into accout). """
#
#     return max(0,
#                lane_length - final_detector_length - requested_distance_to_tls)
#
#
# def fixingDetector_LaneLengthGreaterThanDetector(requested_detector_length, requested_distance_from_tls,lane_length):
#     detector_lenth = requested_detector_length
#     detector_position = lane_length - requested_detector_length -requested_distance_from_tls
#     return detector_lenth,detector_position
#
# def fixingDetector_LaneLengthLessThanDetector(requested_detector_length, requested_distance_from_tls,lane_length):
#     detector_lenth = requested_detector_length
#     detector_position = lane_length - requested_detector_length -requested_distance_from_tls
#     return detector_lenth,detector_position
#
#
# def write_detectors_in_xml(detectors_xml,results,frequency,lane_id,final_detector_length,final_detector_position):
#     detector_xml = detectors_xml.addChild("laneAreaDetector")
#     detector_xml.setAttribute("file", results)
#     detector_xml.setAttribute("freq", str(frequency))
#     detector_xml.setAttribute("friendlyPos", "x")
#     detector_xml.setAttribute("id", "e2det300_" + str(lane_id))
#     detector_xml.setAttribute("lane", str(lane_id))
#     detector_xml.setAttribute("length", str(final_detector_length))
#     detector_xml.setAttribute("pos", str(final_detector_position))
#
#
#
# if __name__ == "__main__":
#     # pylint: disable-msg=C0103
#
#     logging.basicConfig(level="INFO")
#
#     option_parser = optparse.OptionParser()
#     option_parser.add_option("-n", "--net-file",
#                              dest="net_file",
#                              help="Network file to work with. Mandatory.",
#                              type="string")
#     option_parser.add_option("-l", "--detector-length",
#                              dest="requested_detector_length",
#                              help="Length of the detector in meters "
#                              "(-1 for maximal length).",
#                              type="int",
#                              default=250)
#     option_parser.add_option("-d", "--distance-to-TLS",
#                              dest="requested_distance_to_tls",
#                              help="Distance of the detector to the traffic "
#                              "light in meters. Defaults to 0.1m.",
#                              type="float",
#                              default=.1)
#     option_parser.add_option("-f", "--frequency",
#                              dest="frequency",
#                              help="Detector's frequency. Defaults to 60.",
#                              type="int",
#                              default=60)
#     option_parser.add_option("-o", "--output",
#                              dest="output",
#                              help="The name of the file to write the detector "
#                              "definitions into. Defaults to e2.add.xml.",
#                              type="string",
#                              default="e2.add.xml")
#     option_parser.add_option("-r", "--results-file",
#                              dest="results",
#                              help="The name of the file the detectors write "
#                              "their output into. Defaults to e2output.xml.",
#                              type="string",
#                              default="incomingLoopDetectors.xml")
#     option_parser.set_usage("generateTLSE2Detectors.py -n example.net.xml "
#                             "-l 10 -d .1 -f 60")
#
#     (options, args) = option_parser.parse_args()
#     if not options.net_file:
#         print("Missing arguments")
#         option_parser.print_help()
#         exit()
#
#     logging.info("Reading net...")
#     net = sumolib.net.readNet(options.net_file)
#
#     logging.info("Generating detectors...")
#     detectors_xml = sumolib.xml.create_document("additional")
#     lanes_with_detectors = set()
#     lanes_with_detectors_1 = set()
#     for tls in net._tlss:
#         for connection in tls._connections:
#             lane = connection[0]
#             lane_length = lane.getLength()
#             lane_id = lane.getID()
#             if lane_id in lanes_with_detectors:
#                 logging.warning("Detector for lane %s already generated" %
#                              (str(lane_id)))
#                 continue
#             lanes_with_detectors.add(lane_id)
#
#             if lane_length >= options.requested_detector_length + options.requested_distance_to_tls:
#                 detector_lenth,detector_position = fixingDetector_LaneLengthGreaterThanDetector(options.requested_detector_length,
#                                                              options.requested_distance_to_tls,lane_length)
#                 write_detectors_in_xml(detectors_xml,options.results,options.frequency,lane_id,detector_lenth,detector_position)
#             else:
#
#                 lane_length = lane.getLength()
#                 lane_id = lane.getID()
#                 if lane_length < options.requested_detector_length + options.requested_distance_to_tls:
#                     detector_lenth, detector_position = fixingDetector_LaneLengthLessThanDetector(
#                     options.requested_detector_length,options.requested_distance_to_tls, lane_length)
#                     write_detectors_in_xml(detectors_xml, options.results, options.frequency, lane_id, detector_lenth,
#                                            detector_position)
#                     for lanes in lane.getIncoming():
#                         print("lane incoming:", lanes.getID())
#                         lane_id_1 = lanes.getID()
#                         lane_length_1 = lanes.getLength()
#
#                         if lane_id_1 in lanes_with_detectors_1:
#                             logging.warning("Detector for lane %s already generated" %
#                                         (str(lane_id_1)))
#                             continue
#                         lanes_with_detectors.add(lane_id)
#
#     detector_file = open(options.output, 'w')
#     detector_file.write(detectors_xml.toXML())
#     detector_file.close()
#
#     logging.info("%d e2 detectors generated!" % len(lanes_with_detectors))
#



#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    generateTLSE2Detectors.py
# @author  Daniel Krajzewicz
# @author  Karol Stosiek
# @author  Lena Kalleske
# @author  Michael Behrisch
# @date    2007-10-25
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import logging
import optparse
import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sumolib.xml  # noqa
from sumolib import checkBinary  # noqa
import traci  # noqa
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import sumolib.xml  # noqa

#  <e1Detector id="T17L0L" lane="547560322#7_1" pos="20" freq="10" file="LoopDetectorOutput.txt" friendlyPos="x"/>
def adjust_detector_length(requested_detector_length,
                           requested_distance_to_tls,
                           lane_length):
    """ Adjusts requested detector's length according to
        the lane length and requested distance to TLS.

        If requested detector length is negative, the resulting detector length
        will match the distance between requested distance to TLS and lane
        beginning.


        If the requested detector length is positive, it will be adjusted
        according to the end of lane ending with TLS: the resulting length
        will be either the requested detector length or, if it's too long
        to be placed in requested distance from TLS, it will be shortened to
        match the distance between requested distance to TLS
        and lane beginning. """

    if requested_detector_length == -1:
        return lane_length - requested_distance_to_tls

    return min(lane_length - requested_distance_to_tls,
               requested_detector_length)


def adjust_detector_position(final_detector_length,
                             requested_distance_to_tls,
                             lane_length):
    """ Adjusts the detector's position. If the detector's length
        and the requested distance to TLS together are longer than
        the lane itself, the position will be 0; it will be
        the maximum distance from lane end otherwise (taking detector's length
        and requested distance to TLS into accout). """

    return max(0,
               lane_length - final_detector_length - requested_distance_to_tls)


if __name__ == "__main__":
    # pylint: disable-msg=C0103

    logging.basicConfig(level="INFO")

    option_parser = optparse.OptionParser()
    option_parser.add_option("-n", "--net-file",
                             dest="net_file",
                             help="Network file to work with. Mandatory.",
                             type="string")
    option_parser.add_option("-l", "--detector-length",
                             dest="requested_detector_length",
                             help="Length of the detector in meters "
                             "(-1 for maximal length).",
                             type="int",
                             default=250)
    option_parser.add_option("-d", "--distance-to-TLS",
                             dest="requested_distance_to_tls",
                             help="Distance of the detector to the traffic "
                             "light in meters. Defaults to 0.1m.",
                             type="float",
                             default=.1)
    option_parser.add_option("-f", "--frequency",
                             dest="frequency",
                             help="Detector's frequency. Defaults to 60.",
                             type="int",
                             default=60)
    option_parser.add_option("-o", "--output",
                             dest="output",
                             help="The name of the file to write the detector "
                             "definitions into. Defaults to e2.add.xml.",
                             type="string",
                             default="e2.add.xml")
    option_parser.add_option("-r", "--results-file",
                             dest="results",
                             help="The name of the file the detectors write "
                             "their output into. Defaults to e2output.xml.",
                             type="string",
                             default="e2output.xml")
    option_parser.set_usage("generateTLSE2Detectors.py -n example.net.xml "
                            "-l 250 -d .1 -f 60")

    (options, args) = option_parser.parse_args()
    if not options.net_file:
        print("Missing arguments")
        option_parser.print_help()
        exit()

    logging.info("Reading net...")
    net = sumolib.net.readNet(options.net_file)

    logging.info("Generating detectors...")
    detectors_xml = sumolib.xml.create_document("additional")
    lanes_with_detectors = set()
    for tls in net._tlss:
        for connection in tls._connections:
            lane = connection[0]
            lane_length = lane.getLength()
            lane_id = lane.getID()

            logging.debug("Creating detector for lane %s" % (str(lane_id)))

            if lane_id in lanes_with_detectors:
                logging.warn("Detector for lane %s already generated" %
                             (str(lane_id)))
                continue

            final_detector_length = adjust_detector_length(
                options.requested_detector_length,
                options.requested_distance_to_tls,
                lane_length)
            final_detector_position = adjust_detector_position(
                final_detector_length,
                options.requested_distance_to_tls,
                lane_length)
            # if lane_length < final_detector_position :
            lanes_with_detectors.add(lane_id)

            if options.requested_distance_to_tls <= lane_length:
                    detector_xml = detectors_xml.addChild("laneAreaDetector")
                    detector_xml.setAttribute("file", options.results)
                    detector_xml.setAttribute("freq", str(options.frequency))
                    detector_xml.setAttribute("friendlyPos", "x")
                    detector_xml.setAttribute("id", "e2det300_" + str(lane_id))
                    detector_xml.setAttribute("lane", str(lane_id))
                    detector_xml.setAttribute("length", str(final_detector_length))
                    detector_xml.setAttribute("pos", str(final_detector_position))

    detector_file = open(options.output, 'w')
    detector_file.write(detectors_xml.toXML())
    detector_file.close()

    logging.info("%d e2 detectors generated!" % len(lanes_with_detectors))