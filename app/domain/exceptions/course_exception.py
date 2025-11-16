class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class CoursesNotFoundError(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass
