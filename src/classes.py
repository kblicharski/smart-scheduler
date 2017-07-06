import datetime


class Course():
    def __init__(self, name, number, time_range):
        self.name = name
        self.number = number
        self.time_range = time_range

    def __str__(self):
        return str(self.name) + ' - ' + str(self.number) + ' - ' + str(self.time_range)


class TimeBlock():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        # Remove seconds for readability
        [start, end] = map(lambda s: s[:-3], [str(self.start), str(self.end)])
        return '[' + str(start) + '-' + str(end) + ']'

    @property
    def duration(self):
        return datetime.timedelta(self.end - self.start)


class CourseNumber():
    def __init__(self, department, number):
        self.department = department
        self.number = number

    def __str__(self):
        return self.department + ':' + str(self.number)
