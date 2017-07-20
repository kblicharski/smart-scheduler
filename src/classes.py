"""
This file contains class definitions for the various values we are considering.
Eventually we will want to set up automatic JSON deserializing.
"""
import datetime


class Course():
    """
    Represents a Course.

    department  (string): the department offering the course
    number      (int): the course number
    name        (string): the name of the course
    time_block  (TimeBlock): the time the course runs at
    """
    def __init__(self, department, name, number, time_blocks):
        self.department = department
        self.number = number
        self.name = name
        self.time_blocks = time_blocks

    def __str__(self):
        time_block_listings = [str(time_block) for time_block in
                               self.time_blocks]
        return '{}:{} - {} - {}'.format(self.department, self.number,
                                        self.name, time_block_listings)

    def get_time_block(self):
        """
        Returns the time block associated with a course
        """
        return self.time_blocks


class TimeBlock():
    """
    Represents the allotted time for a course.

    start   (time): the starting time of the class
    end     (time): the ending time of the class
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        # Removes seconds for readability
        [start, end] = map(lambda s: s[:-3], [str(self.start), str(self.end)])
        return '[' + str(start) + '-' + str(end) + ']'

    @property
    def duration(self):
        """
        Returns the duration of the class as a time object
        """
        return datetime.timedelta(self.end - self.start)
