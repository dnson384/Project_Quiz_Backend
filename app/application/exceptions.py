class ApplicationError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


# ----------------Auth----------------
class EmailExistedError(ApplicationError):
    pass


class InvalidCredentialsError(ApplicationError):
    pass


class AccountNotFoundError(ApplicationError):
    pass


# User
class UserNotFoundError(ApplicationError):
    pass


class UserNotAllowError(ApplicationError):
    pass


class CourseNotFoundError(ApplicationError):
    pass


class CourseDetailNotFoundError(ApplicationError):
    pass


class PracticeTestsNotFoundError(ApplicationError):
    pass


class ResultNotFoundError(ApplicationError):
    pass


class QuestionNotFoundError(ApplicationError):
    pass


class OptionNotFoundError(ApplicationError):
    pass
