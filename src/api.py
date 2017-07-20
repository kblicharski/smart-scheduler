"""
This file contains functions which wrap the MAUI API endpoints with Python
functions for ease of development. Long-term goals include writing a
fully-fledged API wrapper.
"""
from requests import get
from boltons.iterutils import remap


INTERESTED_KEYS = ['courseTitle', 'sectionId', 'sectionNumber',
                   'subjectCourse', 'timeAndLocations']
INTERESTED_TIME_KEYS = ['startTime', 'endTime', 'days']


def get_courses(id: int, subject: str):
    """
    Does all of the dirty work of grabbing course data from the API endpoint
    and cleaning it up into the format we want. The constants defined at the
    top of this module determine what JSON fields we are interested in.

    :param id:
    the sessionId of the courses (what semester/year they were offered in)
    :param subject:
    the department of the course (note: only works past the year 2007,
    or ID 1, as this is when course listings were adopted in the current format)
    :return:
    the complete list of fetched courses
    """
    def clean_and_filter_courses(courses: list):
        """
        Removes unnecessary information (namely, values that are None or
        empty lists). Also filters according to the keys we want, defined above.

        :param courses:
        the raw, unfiltered list of course data
        :return:
        a list of cleaned courses
        """
        def filter_keys(input: dict, keys: list):
            return {k: v for k, v in input.items() if k in keys}

        def filter_time_fields(input: list):
            for i in range(len(input)):
                filtered_times = list(map(lambda p:
                                          filter_keys(p, INTERESTED_TIME_KEYS),
                                          input[i]['timeAndLocations']))
                input[i]['timeAndLocations'] = filtered_times

        cleaned = remap(courses, lambda p, k, v: v is not None and v != [])
        filtered = list(map(lambda p: filter_keys(p, INTERESTED_KEYS), cleaned))
        filter_time_fields(filtered)
        return filtered

    payload = "json={{sessionId: {}, courseSubject: '{}'}}"\
        .format(str(id), subject)
    url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
    response = get(url=url, params=payload).json()
    raw_courses = response['payload']
    return clean_and_filter_courses(raw_courses)

"""
Session IDs for upcoming semesters
    {
        "id": 69,
        "startDate": "2017-05-15T05:00:00.000+0000",
        "endDate": "2017-08-04T05:00:00.000+0000",
        "shortDescription": "Summer 2017",
        "legacyCode": "20171"
    },
    {
        "id": 68,
        "startDate": "2017-08-21T05:00:00.000+0000",
        "endDate": "2017-12-08T06:00:00.000+0000",
        "shortDescription": "Fall 2017",
        "legacyCode": "20173"
    },
    {
        "id": 70,
        "startDate": "2017-12-27T06:00:00.000+0000",
        "endDate": "2018-01-12T06:00:00.000+0000",
        "shortDescription": "Winter 2017",
        "legacyCode": "20175"
    },
    {
        "id": 71,
        "startDate": "2018-01-16T06:00:00.000+0000",
        "endDate": "2018-05-04T05:00:00.000+0000",
        "shortDescription": "Spring 2018",
        "legacyCode": "20178"
    },
"""
