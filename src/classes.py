"""
This file contains class definitions for the various values we are considering.
Eventually we will want to set up automatic JSON deserializing.
"""
import datetime
import string


class CourseSection():
    """
    Represents a particular section of a Course.

    course_title: string        the name of the course
    section_id: int             unique identifier of this section
    section_number: string      human-readable identifier of this section
    subject_course: string      human-readable identifier of this course
    time_and_locations: list    list containing a dictionary with time values
    """

    def __init__(self, course_title, section_id, section_number,
                 subject_course, time_and_locations):
        self.course_title = course_title
        self.section_id = section_id
        self.section_number = section_number
        self.subject_course = subject_course
        self.days = time_and_locations[0]['days']
        self.start_time = time_and_locations[0]['startTime']
        self.end_time = time_and_locations[0]['endTime']
        self.time_block = self.create_time_block(self.start_time,
                                                 self.end_time)

    def __str__(self):
        return self.course_title

    def create_time_block(self, start_time, end_time):
        return TimeBlock(start_time, end_time)


class TimeBlock():
    """
    Custom object to make calculating time conflicts easier by converting
    passed string values into Python time objects.

    Params:
        start_time: time    starting time of the course section
        end_time: time      ending time of the course section
    """

    def __init__(self, start_time: string, end_time: string):
        self.start_time = self.to_time(start_time)
        self.end_time = self.to_time(end_time)

    def __str__(self):
        # Removes seconds for readability
        [start, end] = map(lambda s: s[:-3], [str(self.start_time),
                                              str(self.end_time)])
        return '[' + str(start) + '-' + str(end) + ']'

    def to_time(self, time: string):
        """
        Returns a time object from a passed string representation of a time.
        This is a convenient format for internal time calculations.

        Params:
            time    human-readable time ('8:00A', '5:30P', etc)
        """
        tokens = time.split(':')
        hours = int(tokens[0])
        minutes = int(tokens[1][:2])

        am_or_pm = time[-1]

        if am_or_pm == 'P' and hours < 12:
            hours += 12

        return datetime.time(hour=hours, minute=minutes)
