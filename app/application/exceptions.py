class ApplicationException(Exception):
    pass


class UserNotFoundError(ApplicationException):
    pass


class CourseNotFoundError(ApplicationException):
    pass

class CourseDetailNotFoundError(ApplicationException):
    pass
