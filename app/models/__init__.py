from app.extensions import login_manager
from .user import User
from .disability_type import DisabilityType
from .job import Job
from .application import Application
from .course import Course
from .enrollment import Enrollment
from .indicator import Indicator

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

__all__ = [
    "User",
    "DisabilityType",
    "Job",
    "Application",
    "Course",
    "Enrollment",
    "Indicator"
]