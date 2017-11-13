"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime, timedelta
from typing import Tuple

# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in long/lat coordinates
        **UPDATED**: make sure the first coordinate is the longitude,
        and the second coordinate is the latitude.
    name:
        name of the station
    num_bikes:
        current number of bikes at the station
    rides_started:
        the number of rides started at this station
    rides_ended:
        the number of rides ended at this station
    tick_low_availability:
        the number of seconds throughout the simulation that this
        station spent with a low availability (5 or less bikes available)
    tick_low_unoccupied:
        the number of seconds throughout the simulation that this
        station spent with a low number of unoccupied spots (5 or less free
        spots available)

    === Public Properties ===
    unoccupied_spots: int
        the number of empty spots in the station.
        Note: This value is a computed value and can not be set.

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    - tick_low_availability >= 0
    - tick_low_unoccupied >= 0
    - rides_started >= 0
    - rides_ended >= 0
    """

    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    rides_started: int
    rides_ended: int
    tick_low_availability: int
    tick_low_unoccupied: int

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        super().__init__(STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.rides_ended = 0
        self.rides_started = 0
        self.tick_low_availability = 0
        self.tick_low_unoccupied = 0

    @property
    def unoccupied_spots(self) -> int:
        """The number of unused spots in the station."""
        return self.capacity - self.num_bikes

    def record_ride_started(self) -> None:
        """Records that a ride has started at this station"""
        self.rides_started += 1

    def record_ride_ended(self) -> None:
        """Records that a ride has ended at this station"""
        self.rides_ended += 1

    def is_ride_start_possible(self) -> bool:
        """Returns if a ride can be started at this location.
        (num_bikes is greater than 0).
        """
        return self.num_bikes > 0

    def is_ride_end_possible(self) -> bool:
        """
        Returns if a ride can be ended at this location.
        (unoccupied_spots is greater than 0).
        """
        return self.unoccupied_spots > 0

    def register_dispatch(self) -> bool:
        """
        Dispatches a bike and registers it as left the station, if
        it is possible to dispatch such a bike (i.e there are no bikes parked).
        Returns whether or not a bike was successfully dispatched.
        """
        if self.is_ride_start_possible():
            self.num_bikes -= 1
            return True
        return False

    def register_park(self) -> bool:
        """
        Parks bike and registers it as in the station, if
        it is possible to park such a bike (i.e there are parking spaces left).
        Returns whether or not a bike was successfully parked.
        """
        if self.is_ride_end_possible():
            self.num_bikes += 1
            return True
        return False

    def update_tick_statistics(self) -> None:
        """Updates statistics on low availability or low unoccupancy for one
        tick (usually one minute).
        """
        if self.num_bikes <= 5:
            self.tick_low_availability += 60
        if self.unoccupied_spots <= 5:
            self.tick_low_unoccupied += 60

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        super().__init__(RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        end_position = self.end.get_position(time)
        start_position = self.start.get_position(time)

        # We will place the ride at the initial position if
        # the ride has yet to be started, and the final position if
        # the ride has already ended.
        # Otherwise, the ride will continue to move past it's end time if
        # the simulation does not clear it.

        if time < self.start_time:
            return start_position
        if time > self.end_time:
            return end_position

        total_distance = Ride.__get_distance(start_position, end_position)
        total_time = self.end_time - self.start_time
        elapsed_time = time - self.start_time

        # Calculate the distance traveled since the start time.
        distance_delta = Ride.__get_distance_time_delta(total_time,
                                                        elapsed_time,
                                                        total_distance)

        return (start_position[0] + distance_delta[0],
                start_position[1] + distance_delta[1])

    @staticmethod
    def __get_distance(start_position: Tuple[float, float],
                       end_position:
                       Tuple[float, float]) -> Tuple[float, float]:
        """
        Gets the distance vector between the given starting position, and the
        given ending position.
        """
        return (end_position[0] - start_position[0],
                end_position[1] - start_position[1])

    @staticmethod
    def __get_distance_time_delta(total_time: timedelta,
                                  elapsed_time: timedelta,
                                  distance:
                                  Tuple[float, float]) -> Tuple[float, float]:
        """
        Gets the scalar multiple of the given distance, and the percentage
        of time elapsed between the currently elapsed and the total time to be
        reached.
        
        Used to get a 'partially complete' distance between two times.
        """
        percentage_complete = elapsed_time / total_time
        return (percentage_complete * distance[0],
                percentage_complete * distance[1])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
