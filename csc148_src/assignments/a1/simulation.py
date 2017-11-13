"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Callable, Union

import pygame

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    active_rides:
        A list of rides currently active during the current timeframe
        while the simulation is being run.
    queue:
        A PriorityQueue to handle dispatching station events.

    === Preconditions ===
    - station_file exists and contains valid data for at least one station.
    - ride_file exists and contains valid data.
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    active_rides: List[Ride]
    visualizer: Visualizer
    queue: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.visualizer = Visualizer()
        self.queue = PriorityQueue()

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """

        return {
            'max_start': self._get_max(lambda station: station.rides_started),
            'max_end': self._get_max(lambda station: station.rides_ended),
            'max_time_low_availability':
                self._get_max(lambda station: station.tick_low_availability),
            'max_time_low_unoccupied':
                self._get_max(lambda station: station.tick_low_unoccupied)
        }

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        === Preconditions ===
         - start < end
         - all_rides is not empty.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time
        drawables = list(self.all_stations.values())  # Gather static drawables
        current_time = start

        # We want events for every ride that starts before or when we end.

        for ride in self.all_rides:
            self.queue.add(RideStartEvent(self, ride, start, end))

        while True:
            # If we want the simulation to be exclusive of the last minute,
            # change this to current_time < end.
            while current_time <= end:
                # Update the tick statistics if current_time < end,
                # for the beginning of the minute.
                # (low availability and low unoccupancy)
                if current_time < end:
                    self._update_station_tick_statistics()

                self._update_active_rides_fast(current_time)

                # Render the the active rides,
                # in addition to the static drawables
                self._render_process_events(current_time,
                                            drawables + self.active_rides)

                current_time += step
            # We will keep rendering past the simulation,
            # and process events to allow quitting.
            if not self._render_process_events(current_time - step,
                                               drawables + self.active_rides,
                                               True):
                return

    def _render_process_events(self, current_time: datetime,
                               drawables: List['Drawable'],
                               process_events: bool = False) -> bool:
        """Render all drawables and process any window events if required.
           Returns whether or not to continue rendering."""
        self.visualizer.render_drawables(drawables + self.active_rides,
                                         current_time)
        pygame.event.peek([])  # pygame workaround.
        if process_events:
            return not self.visualizer.handle_window_events()
        return True

    def _update_station_tick_statistics(self) -> None:
        """Updates tick statistics (low availability and low unoccupancy)
        for one tick.
        """
        for station in self.all_stations.values():
            station.update_tick_statistics()

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.
        """
        for ride in self.all_rides:
            if ride.start_time <= time < ride.end_time:
                # We want all rides that start at or in between the current time
                # and end at or before the current time.
                self._process_ride_start(ride, time)
            elif ride in self.active_rides:
                # An active ride is past it's timeframe, so we process its
                # removal.
                self._process_ride_end(ride, time)

    def _process_ride_start(self, ride: Ride, current_time: datetime) -> None:
        """Marks a ride as active and records the start statistic if it
        is not active, and the ride can be started.
        === Preconditions ===
        - ride not in self.active_rides
        """
        if ride not in self.active_rides and \
                ride.start.is_ride_start_possible():
            # Process only rides that are possible
            # (there is a bike in the station) and not already active
            if ride.start_time == current_time:
                ride.start.record_ride_started()
            ride.start.register_dispatch()
            self.active_rides.append(ride)

    def _process_ride_end(self, ride: Ride, current_time: datetime) -> None:
        """Removes a ride from the active rides an records it as ended.
        === Preconditions ===
        - ride in self.active_rides
        """
        self.active_rides.remove(ride)
        # Record the ride if it was possible to end
        # (there are unoccupied spots left in the ending station)
        # Event if the ride time is such as we do not count statistics,
        # treat it as parked.
        if ride.end.register_park() and ride.end_time == current_time:
            ride.end.record_ride_ended()

    def _get_max(self, attribute: Callable[[Station], Union[float, int]]) -> \
            Tuple[str, Union[float, int]]:
        """
        Given a numeric attribute to compare with, returns the
        name of the station where the station has the greatest value
        of that attribute. If two or more stations have the same value of the
        attribute, returns the station with the alphabetically earlier name.

        === Preconditions ===
        - attribute is a function of a Station that returns
            either a float or int.
        - all_stations contains at least one item.
        """
        max_station = sorted(self.all_stations.values(),
                             key=lambda station: (-attribute(station),
                                                  station.name))[0]
        # We sort with the negative value of attribute, because we want
        # to sort both in decreasing order for the attribute, and increasing
        # order for the station name, simultaneously. Sorting by the negative
        # attribute value allows us to treat it as increasing unilaterally.

        # DO NOT NORMALIZE CASING for name. Tests expect 'A' < 'a'
        # and so forth for comparison purposes (code-point order
        # sort rather than pure lexicographical).

        return max_station.name, attribute(max_station)

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """

        future_events = []

        if self.queue.is_empty():
            return

        while not self.queue.is_empty():
            event = self.queue.remove()
            if event.time > time:
                future_events.append(event)
                continue
            # This event happens at the given time.
            for result_event in event.process():
                self.queue.add(result_event)
        for event in future_events:
            self.queue.add(event)


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """

    # Read in raw data using the json library.
    # We need to handle the French characters, as such, force encoding to UTF-8.
    with open(stations_file, encoding="utf-8") as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().

        station_id = s['n']
        name = s['s']
        latitude = float(s['la'])
        longitude = float(s['lo'])
        bikes_stored = int(s['da'])
        unoccupied_spaces = int(s['ba'])

        stations[station_id] = Station(
            name=name,
            pos=(longitude, latitude),
            cap=bikes_stored + unoccupied_spaces,
            num_bikes=bikes_stored
        )
    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        for line in csv.reader(file):
            # line is a list of strings, following the format described
            # in the assignment handout.
            #
            # Convert between a string and a datetime object
            # using the function datetime.strptime and the DATETIME_FORMAT
            # constant we defined above. Example:
            # >>> datetime.strptime('2017-06-01 8:00', DATETIME_FORMAT)
            # datetime.datetime(2017, 6, 1, 8, 0)

            ride_start = datetime.strptime(line[0], DATETIME_FORMAT)
            ride_end = datetime.strptime(line[2], DATETIME_FORMAT)
            start_id = line[1]
            end_id = line[3]

            try:
                rides.append(Ride(
                    start=stations[start_id],
                    end=stations[end_id],
                    times=(ride_start, ride_end)
                ))
            except KeyError:
                continue

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride.

    === Public Attributes ===
    ride: The bike ride this event processes the start of.
    start_time: The time this simulation started.
    end_time: The time this simulation ended.

    === Preconditions ===
    - start_time < end_time
    """

    def __init__(self, simulation: Simulation, ride: Ride,
                 start_time: datetime, end_time: datetime):
        super().__init__(simulation, ride.start_time)
        self.ride = ride
        self.start_time = start_time
        self.end_time = end_time

    def process(self) -> List['Event']:
        """Processes a ride starting if valid, by adding the ride to
        the simulation's active rides and recording the event.
        """

        # This ride can not possibly be started.
        if not self.ride.start.register_dispatch():
            return []

        # This ride ends before it starts (!!?)
        if self.ride.start_time >= self.ride.end_time:
            return []

        # This ride is valid.

        self.simulation.active_rides.append(self.ride)
        if self.start_time <= self.ride.start_time <= self.end_time:
            self.ride.start.record_ride_started()
        return [RideEndEvent(self.simulation, self.ride,
                             self.start_time, self.end_time)]


class RideEndEvent(Event):
    """An event corresponding to the end of a ride.

    === Public Attributes ===
    ride: The bike ride this event processes the end of.
    start_time: The time this simulation started.
    end_time: The time this simulation ended.

    === Preconditions ===
    - start_time < end_time
    """

    def __init__(self, simulation: Simulation, ride: Ride,
                 start_time: datetime, end_time: datetime):
        super().__init__(simulation, ride.end_time)
        self.ride = ride
        self.start_time = start_time
        self.end_time = end_time

    def process(self) -> List['Event']:
        """Processes a ride ending event by removing the ride from the
        simulation's active rides and recording the event if valid.
        """

        # Remove the ride from the visualization regardless of status.
        self.simulation.active_rides.remove(self.ride)
        # This ride can be ended.
        if self.ride.end.register_park() \
                and self.start_time <= self.ride.end_time <= self.end_time:
            self.ride.end.record_ride_ended()

        return []


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0), datetime(2017, 6, 1, 9, 0, 0))
    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['create_stations', 'create_rides'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'csv', 'datetime', 'json',
            'bikeshare', 'container', 'visualizer'
        ]
    })
    print(sample_simulation())
