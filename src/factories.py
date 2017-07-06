import random
import datetime

from classes import Course, TimeBlock, CourseNumber
from mock_data import mock_courses, mock_times


class TimeBlockFactory():
    hours = mock_times[0]
    minutes = mock_times[1]

    # TODO: Change behavior so that the timeblocks are of reasonable length
    def get_time_block(self):
        start_time = self.create_datetime()
        end_time = self.create_datetime()

        while (end_time < start_time):
            end_time = self.create_datetime()

        return TimeBlock(start_time, end_time)

    def create_datetime(self):
        return datetime.time(hour=random.choice(self.hours),
                             minute=random.choice(self.minutes))


class CourseFactory():
    courses = mock_courses

    def get_course(self):
        selection = random.choice(self.courses)
        return Course(selection['course_name'], selection['course_number'],
                      TimeBlockFactory().get_time_block())

    @property
    def number_of_courses(self):
        return len(self.courses)
