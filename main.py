import googlemaps
from SECRETS import API_KEY
from datetime import datetime, timedelta
from addresses import delivery_list

"""
Delivery list is defined as follows:
    delivery_list = [
        {"name": "<delivery_name>", "location": "<delivery_location>"},
        ...
        {"name": "<delivery_name>", "location": "<delivery_location>"},
    ]
"""

START = datetime.now()  # When the driver is expected to leave
DELIVERY_BUFFER = 5  # Estimated time in minutes to complete a delivery
DELIVERY_WINDOW = 60  # time window to present to customers, in minutes


def get_travel_time(start, destination, depart_time):
    """
    Return the time in seconds taken to travel from start to destination, when starting the trip at depart time
    """
    rv = gmaps.directions(start, destination, mode="driving", departure_time=depart_time)
    return rv[0]['legs'][0]['duration_in_traffic']['value']


if __name__ == "__main__":
    # create a googlemaps object
    gmaps = googlemaps.Client(key=API_KEY)

    depart_time = START
    total_route_time = timedelta(minutes=0)

    for i in range(len(delivery_list)-1):
        travel_time = get_travel_time(delivery_list[i]["location"], delivery_list[i+1]["location"], depart_time)
        arrival_time = depart_time + timedelta(seconds=travel_time)
        depart_time = arrival_time + timedelta(minutes=DELIVERY_BUFFER)
        total_route_time = total_route_time + timedelta(seconds=travel_time)
        #  Give some feedback
        date = arrival_time.strftime("%b %d")
        lower_bound = (arrival_time - timedelta(minutes=DELIVERY_WINDOW/2)).strftime("%H:%M")
        upper_bound = (arrival_time + timedelta(minutes=DELIVERY_WINDOW/2)).strftime("%H:%M")
        print("{} can expect their delivery on {} between {} and {}".format(delivery_list[i+1]["name"], date, lower_bound, upper_bound))

    print("The driver can expect to spend {} on the road".format(total_route_time))
