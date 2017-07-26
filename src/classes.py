"""
This file contains class definitions for the various values we are considering.
Eventually we will want to set up automatic JSON deserializing.
"""
import datetime


class TimeBlock():
    """
    Custom object to make calculating time conflicts easier by converting
    passed string values into Python time objects.
    """
    def __init__(self, start_time: str, end_time: str) -> None:
        self.start_time = self.to_time(start_time)
        self.end_time = self.to_time(end_time)

    def __str__(self):
        # Removes seconds for readability
        [start, end] = map(lambda s: s[:-3], [str(self.start_time),
                                              str(self.end_time)])
        return '[' + str(start) + '-' + str(end) + ']'

    def to_time(self, time: str) -> datetime:
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


class CourseSection():
    """
    Represents a particular section of a Course.

    course_title        the name of the course
    section_id          identifier of this section
    section_number      human-readable identifier of this section
    subject_course      human-readable identifier of this course
    time_and_locations  list containing a dictionary with time values
    """
    def __init__(self, course_title: str, section_id: int, section_number: str,
                 subject_course: str, time_and_locations: list):
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
        return '{}:{} - {}'.format(self.subject_course,
                                   self.section_number,
                                   self.time_block)

    def create_time_block(self, start_time: str, end_time: str) -> TimeBlock:
        return TimeBlock(start_time, end_time)


class Course():
    """
    A Course is a container for CourseSections.
    """
    def __init__(self, sections: [CourseSection]):
        self.sections = sections
        self.course_title = sections[0].course_title
        self.subject_course = sections[0].subject_course
        self.time_blocks = self.get_time_blocks(sections)

    def __str__(self):
        return '{} - {}'.format(self.subject_course, self.course_title)

    def get_time_blocks(self, sections: [CourseSection]) -> [TimeBlock]:
        time_blocks = []
        [time_blocks.append(section.time_block) for section in sections]
        return time_blocks
