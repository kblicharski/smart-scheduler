"""
This file contains class definitions for the various values we are considering.
"""
import datetime


# TODO: Consider including more fields that might be of interest
# section, instructor, course type (lecture, discussion, lab), semester
# hours, prerequisites, corequisites, location (building, room), days offered

# TODO: Refactor this to make Courses have MULTIPLE times.
class Course():
    """
    Represents a Course.

    department  (string): the department offering the course
    number      (int): the course number
    name        (string): the name of the course
    time_block  (TimeBlock): the time the course runs at
    """
    def __init__(self, department, name, number, time_block):
        self.department = department
        self.number = number
        self.name = name
        self.time_block = time_block

    def __str__(self):
        return '{}:{} - {} - {}'.format(self.department, self.number, self.name,
                                        self.time_block)

    def get_time_block(self):
        """
        Returns the time block associated with a course
        """
        return self.time_block


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
        :return:
        """
        return datetime.timedelta(self.end - self.start)
