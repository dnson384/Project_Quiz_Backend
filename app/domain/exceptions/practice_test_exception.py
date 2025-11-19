class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class PracticeTestsNotFoundError(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass
