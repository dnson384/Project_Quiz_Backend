class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class PracticeTestsNotFoundErrorDomain(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass


class QuestionNotFoundErrorDomain(BusinessError):
    pass


class OptionNotFoundErrorDomain(BusinessError):
    pass
