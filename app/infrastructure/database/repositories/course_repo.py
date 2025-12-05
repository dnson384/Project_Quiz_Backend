from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import List, Optional, TypedDict

from app.domain.entities.course.course_entity import (
    Course,
    CourseOutput,
    CreateNewCourseInput,
    UpdateCourseInput,
)
from app.domain.entities.course.course_detail_entity import (
    CourseDetail,
    CourseDetailOutput,
    CreateNewCourseDetailInput,
    UpdateCourseDetailInput,
)
from app.domain.exceptions.course_exception import (
    CoursesNotFoundErrorDomain,
    CourseDetailsNotFoundErrorDomain,
)

from app.application.abstractions.course_abstraction import ICourseRepository

from app.infrastructure.database.models.course_model import (
    CourseModel,
    CourseDetailModel,
)
from app.infrastructure.database.models.user_model import UserModel


class CourseWithDetails(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class CoursesRepository(ICourseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseOutput]:
        try:
            query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                    func.count(CourseDetailModel.course_detail_id).label(
                        "num_of_terms"
                    ),
                )
                .filter(CourseModel.course_name.ilike(f"%{keyword}%"))
                .join(UserModel, CourseModel.user_id == UserModel.user_id)
                .join(
                    CourseDetailModel,
                    CourseModel.course_id == CourseDetailModel.course_id,
                )
            )

            if cursor_id:
                query = query.filter(CourseModel.course_id < cursor_id)

            query = query.order_by(CourseModel.course_id.desc())

            db_results = (
                query.group_by(
                    CourseModel.course_id,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
                )
                .limit(12)
                .all()
            )

            domain_results: List[CourseOutput] = []
            for row in db_results:
                domain_results.append(
                    CourseOutput(
                        course_id=row.course_id,
                        course_name=row.course_name,
                        author_avatar_url=row.avatar_url,
                        author_username=row.username,
                        author_role=row.role,
                        num_of_terms=row.num_of_terms,
                    )
                )

            return domain_results

        except Exception as e:
            print("Có lỗi xảy ra khi tìm kiếm học phần", e)
            return []

    def get_random_courses(self) -> List[CourseOutput]:
        try:
            query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                    func.count(CourseDetailModel.course_detail_id).label(
                        "num_of_terms"
                    ),
                )
                .join(UserModel, CourseModel.user_id == UserModel.user_id)
                .join(
                    CourseDetailModel,
                    CourseModel.course_id == CourseDetailModel.course_id,
                )
                .group_by(
                    CourseModel.course_id,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
                )
                .limit(3)
                .all()
            )

            domain_result: List[CourseOutput] = []
            for item in query:
                domain_result.append(
                    CourseOutput(
                        course_id=item.course_id,
                        course_name=item.course_name,
                        author_avatar_url=item.avatar_url,
                        author_username=item.username,
                        author_role=item.role,
                        num_of_terms=item.num_of_terms,
                    )
                )

            return domain_result

        except Exception as e:
            print("Có lỗi xảy ra khi lấy học phần ngẫu nhiên", e)
            return []

    def get_course_by_id(self, course_id: UUID) -> CourseOutput:
        try:
            course_query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                )
                .filter(CourseModel.course_id == course_id)
                .join(UserModel, UserModel.user_id == CourseModel.user_id)
                .first()
            )

            detail_query = (
                self.db.query(
                    CourseDetailModel.course_detail_id,
                )
                .filter(CourseDetailModel.course_id == course_id)
                .all()
            )

            return CourseOutput(
                course_id=course_query.course_id,
                course_name=course_query.course_name,
                author_avatar_url=course_query.avatar_url,
                author_username=course_query.username,
                author_role=course_query.role,
                num_of_terms=len(detail_query),
            )
        except Exception as e:
            print("Có lỗi xảy ra khi lấy thông tin học phần", e)
            return None

    def get_course_detail_by_id(self, course_id: Optional[str]) -> CourseWithDetails:
        try:
            course_query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.avatar_url,
                    UserModel.username,
                    UserModel.role,
                )
                .filter(CourseModel.course_id == course_id)
                .join(UserModel, UserModel.user_id == CourseModel.user_id)
                .first()
            )

            detail_query = (
                self.db.query(
                    CourseDetailModel.course_detail_id,
                    CourseDetailModel.term,
                    CourseDetailModel.definition,
                )
                .filter(CourseDetailModel.course_id == course_id)
                .all()
            )

            course_domain_result = CourseOutput(
                course_id=course_query.course_id,
                course_name=course_query.course_name,
                author_avatar_url=course_query.avatar_url,
                author_username=course_query.username,
                author_role=course_query.role,
                num_of_terms=len(detail_query),
            )

            detail_domain_result: List[CourseDetailOutput] = []
            for item in detail_query:
                detail_domain_result.append(
                    CourseDetailOutput(
                        course_detail_id=item.course_detail_id,
                        term=item.term,
                        definition=item.definition,
                    )
                )

            return CourseWithDetails(
                course=course_domain_result, course_detail=detail_domain_result
            )
        except Exception as e:
            print("Có lỗi xảy ra khi lấy thông tin chi tiết học phần", e)
            return None

    # Thêm
    def create_new_course(
        self,
        course_in: CreateNewCourseInput,
        detail_in: List[CreateNewCourseDetailInput],
    ):
        new_course_domain = Course.create_new_course(
            course_name=course_in.course_name, user_id=course_in.user_id
        )
        new_course_detail_domain: List[CourseDetail] = []
        for detail in detail_in:
            new_course_detail_domain.append(
                CourseDetail.create_new_course_detail(
                    course_id=new_course_domain.course_id,
                    term=detail.term,
                    definition=detail.definition,
                )
            )

        response = {}
        try:
            new_course_model = CourseModel(
                course_id=new_course_domain.course_id,
                user_id=new_course_domain.user_id,
                course_name=new_course_domain.course_name,
                created_at=new_course_domain.created_at,
                updated_at=new_course_domain.updated_at,
            )
            self.db.add(new_course_model)
            self.db.commit()
            self.db.refresh(new_course_model)

            current_user = (
                self.db.query(UserModel.avatar_url, UserModel.username, UserModel.role)
                .filter(UserModel.user_id == new_course_model.user_id)
                .first()
            )

            response["course"] = CourseOutput(
                course_id=new_course_model.course_id,
                course_name=new_course_model.course_name,
                author_avatar_url=current_user.avatar_url,
                author_username=current_user.username,
                author_role=current_user.role,
                num_of_terms=0,
            )
        except Exception as e:
            print("Lỗi xảy ra khi thêm course")
            self.db.rollback()
            return None

        try:
            new_detail_model: List[CourseDetailModel] = []
            for detail_domain in new_course_detail_domain:
                new_detail_model.append(
                    CourseDetailModel(
                        course_detail_id=detail_domain.course_detail_id,
                        course_id=detail_domain.course_id,
                        term=detail_domain.term,
                        definition=detail_domain.definition,
                    )
                )

            self.db.add_all(new_detail_model)
            self.db.commit()
            response["course_detail"] = [
                CourseDetailOutput(
                    course_detail_id=detail.course_detail_id,
                    term=detail.term,
                    definition=detail.definition,
                )
                for detail in new_detail_model
            ]
        except Exception as e:
            print("Lỗi xảy ra khi thêm course detail")
            self.db.rollback()
            return None
        return response

    # Sửa
    def create_new_course_detail(
        self, course_id: UUID, detail_in: CreateNewCourseDetailInput
    ):
        new_detail_domain = CourseDetail.create_new_course_detail(
            course_id=course_id, term=detail_in.term, definition=detail_in.definition
        )

        new_detail_model = CourseDetailModel(
            course_detail_id=new_detail_domain.course_detail_id,
            course_id=new_detail_domain.course_id,
            term=new_detail_domain.term,
            definition=new_detail_domain.definition,
        )

        try:
            self.db.add(new_detail_model)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Lỗi khi thêm mới trong quá trình chỉnh sửa", e)
            raise e

    def update_course_detail(self, course_id: UUID, detail_in: UpdateCourseDetailInput):
        try:
            detail = (
                self.db.query(CourseDetailModel)
                .filter(CourseDetailModel.course_id == course_id)
                .filter(
                    CourseDetailModel.course_detail_id == detail_in.course_detail_id
                )
                .first()
            )

            if not detail:
                raise ValueError("Không tồn tại chi tiết của học phần")

            detail.term = detail_in.term
            detail.definition = detail_in.definition

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Lỗi trong quá trình cập nhật chi tiết học phần: {e}")
            raise e

    def update_course(self, course_id: UUID, course_in: UpdateCourseInput):
        try:
            current_course = (
                self.db.query(CourseModel)
                .filter(CourseModel.course_id == course_id)
                .first()
            )

            if not current_course:
                raise CoursesNotFoundErrorDomain("Không tồn tại học phần cần cập nhật")

            current_course.course_name = course_in.course_name

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Lỗi khi cập nhật tên học phần", e)
            raise e

    def delete_course_detail(self, course_id: UUID, course_detail_id: UUID):
        try:
            current_detail = (
                self.db.query(CourseDetailModel)
                .filter(CourseDetailModel.course_id == course_id)
                .filter(CourseDetailModel.course_detail_id == course_detail_id)
                .first()
            )

            if not current_detail:
                raise CourseDetailsNotFoundErrorDomain("Không tồn tại chi tiết học phần")

            self.db.delete(current_detail)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Lỗi khi xoá chi tiết học phần", e)
            raise e

    def delete_course(self, course_id: UUID):
        try:
            current_course = self.db.query(CourseModel).filter(CourseModel.course_id == course_id).first()

            if not current_course:
                raise CoursesNotFoundErrorDomain("Không tồn tại học phần")

            self.db.delete(current_course)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Lỗi khi xoá học phần", e)
            raise e