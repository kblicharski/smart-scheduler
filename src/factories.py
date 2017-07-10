"""
This file contains factories for quickly generating values during testing.
"""
import random
import datetime

from classes import Course, TimeBlock
from mock_data import mock_courses, mock_start_times, mock_class_durations


MAX_TIME_BLOCKS_FOR_COURSES = 5


class TimeBlockFactory():
    """
    Factory to quickly generate a class time block using mock data.
    """
    possible_start_hours = mock_start_times[0]
    possible_start_minutes = mock_start_times[1]
    possible_durations = mock_class_durations

    def get_time_block(self):
        """
        Generates a 'realistic' time block for a class.
        """
        # Get selections from mock data
        start_hours = random.choice(self.possible_start_hours)
        start_minutes = random.choice(self.possible_start_minutes)
        duration = random.choice(self.possible_durations)

        # Convert durations (which are stored as minutes) into
        # their respect hour and minute durations
        duration_in_minutes_and_hours = self.minutes_to_hours(duration)
        duration_hours = duration_in_minutes_and_hours[0]
        duration_minutes = duration_in_minutes_and_hours[1]

        # Calculate end time from the start time + the durations
        end_hours = start_hours + duration_hours
        end_minutes = start_minutes + duration_minutes

        # Check if adding start_minutes and duration_minutes
        # will result in a new hour, and handle appropriately
        if start_minutes + duration_minutes > 60:
            end_minutes -= 60
            end_hours += 1

        start_time = datetime.time(hour=start_hours, minute=start_minutes)
        end_time = datetime.time(hour=end_hours, minute=end_minutes)

        return TimeBlock(start_time, end_time)

    @staticmethod
    def minutes_to_hours(input_minutes):
        """
        Helper function to simplify logic when creating time blocks.
        Returns a tuple of (hours, minutes) from the input of minutes.
        """
        output_hours = 0
        output_minutes = input_minutes

        while output_minutes > 60:
            output_hours += 1
            output_minutes -= 60

        return (output_hours, output_minutes)


# TODO: Consider allowing for manual course creation as well
class CourseFactory():
    """
    Factory to quickly generate courses from mock data.
    """
    def get_course(self):
        """
        Returns a Course using the mock course data and the TimeBlockFactory
        """
        course = random.choice(mock_courses)
        time_blocks = [TimeBlockFactory().get_time_block() for i in range(
                MAX_TIME_BLOCKS_FOR_COURSES)]

        return Course(department=course['course_department'],
                      number=course['course_number'],
                      name=course['course_name'],
                      time_blocks=time_blocks)

    @property
    def number_of_courses(self):
        """
        Returns the number of courses we have in our mock data
        """
        return len(mock_courses)
