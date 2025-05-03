from flask_marshmallow import Marshmallow
from app.schemas.user_schema import UserSchema
from app.schemas.indicator_schema import IndicatorSchema
from app.schemas.disability_type_schema import DisabilityTypeSchema
from app.schemas.job_schema import JobSchema
from app.schemas.enrollment_schema import EnrollmentSchema
from app.schemas.application_schema import ApplicationSchema
from app.schemas.course_schema import CourseSchema

ma = Marshmallow()

__all__ = [
    'UserSchema',
    'IndicatorSchema',
    'DisabilityTypeSchema',
    'JobSchema',
    'EnrollmentSchema',
    'ApplicationSchema',
    'CourseSchema'
]