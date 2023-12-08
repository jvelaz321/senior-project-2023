import math

import numpy as np

"""
Functions to make it easy to convert between the different frames-of-reference. In particular these
make it easy to navigate in terms of "metres from the current position" when using commands that take 
absolute positions in decimal degrees.

The methods are approximations only, and may be less accurate over longer distances, and when close 
to the Earth's poles.

Specifically, it provides:
* get_location_metres - Get LocationGlobal (decimal degrees) at distance (m) North & East of a given LocationGlobal.
* get_distance_metres - Get the distance between two LocationGlobal objects in metres
* get_bearing - Get the bearing in degrees to a LocationGlobal
"""


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def get_bearing(aLocation1, aLocation2):
    """
    Returns the bearing between the two LocationGlobal objects passed as parameters.

    This method is an approximation, and may not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    off_x = aLocation2.lon - aLocation1.lon
    off_y = aLocation2.lat - aLocation1.lat
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
    if bearing < 0:
        bearing += 360.00
    return bearing;


def get_new_location(original_location, dNorth, dEast):
    earth_radius = 6378137.0  # Radius of "spherical" earth
    # Coordinate offsets in radians
    dLat = dNorth / earth_radius
    dLon = dEast / (earth_radius * math.cos(math.pi * original_location.lat / 180))

    return (dLat, dLon)


def convert_to_distance_vectors(position_data):
    # Convert the list of coordinates to a numpy array for easier calculations
    ned_coords = []
    for index, position in enumerate(position_data):
        if index >= len(position_data) - 1:
            continue
        # Check that there is one more item
        elif index + 1 >= len(position_data) - 1:
            continue

        start = np.array(position)
        end = np.array(position_data[index + 1])

        # Calculate the differences between consecutive coordinates
        difference = end - start
        difference[-1] = -difference[-1]
        difference = difference * 100
        ned_coords.append(difference.tolist())

    return ned_coords


# Example usage
position_data = [[0., 0., 0.], [0., 0., 0.], [-0.00100903, -0.0015942, 0.00235286],
                 [-0.00201643, -0.00318359, 0.00568672], [-0.00301597, -0.00475856, 0.01000151],
                 [-0.00399857, -0.00630839, 0.01529706], [-0.00495101, -0.00782016, 0.02157302],
                 [-0.00585809, -0.00928058, 0.02882877], [-0.00670144, -0.01067657, 0.03706343],
                 [-0.00746191, -0.01199501, 0.04627581], [-0.00812232, -0.01322619, 0.05640696],
                 [-0.00865868, -0.01435643, 0.06751259], [-0.00905817, -0.01538255, 0.07947646],
                 [-0.00930626, -0.01629648, 0.09228068], [-0.00937905, -0.01708141, 0.1060538],
                 [-0.00927143, -0.01773594, 0.12074527], [-0.00897501, -0.01825697, 0.13634361],
                 [-0.00847782, -0.0186367, 0.15290754], [-0.00779392, -0.01888813, 0.17026554],
                 [-0.00690577, -0.01900381, 0.18858917], [-0.00583581, -0.01900378, 0.20770605],
                 [-0.0045757, -0.01888776, 0.22779122], [-0.00313928, -0.01866971, 0.24884677],
                 [-0.00154352, -0.01836878, 0.27087513], [1.9106812e-04, -1.8008484e-02, 2.9387861e-01],
                 [0.00204316, -0.01761751, 0.31784937], [0.0039887, -0.01722806, 0.34279886],
                 [0.00599915, -0.01687495, 0.368728], [0.00804277, -0.0165946, 0.3956365],
                 [0.01008687, -0.01642604, 0.42349377], [0.01209749, -0.01640729, 0.4522556],
                 [0.01403581, -0.01658813, 0.4819869], [0.01587015, -0.01699456, 0.5125375],
                 [0.01755919, -0.01767227, 0.54393154], [0.01905657, -0.01867306, 0.5762209],
                 [0.02032948, -0.02002397, 0.60931903], [0.02134684, -0.02174689, 0.64313567],
                 [0.02203265, -0.02392647, 0.6778481], [0.02237048, -0.02655932, 0.7132804],
                 [0.02233821, -0.02965184, 0.74931926], [0.0219011, -0.033226, 0.7859151],
                 [0.02107502, -0.03724519, 0.82285005], [0.01978277, -0.0417757, 0.860224],
                 [0.01804652, -0.04677423, 0.89783746], [0.01574918, -0.05234253, 0.93586993]]

distance_vector = convert_to_distance_vectors(position_data)
print(distance_vector)
