from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import routes to register them with the blueprint
from .auth import auth_bp
from .users import users_bp
from .disabilities import disabilities_bp
from .jobs import jobs_bp
from .applications import applications_bp
from .courses import courses_bp
from .indicators import indicators_bp
from .enrollments import enrollments_bp

# Register all blueprints
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(disabilities_bp, url_prefix='/api')
    app.register_blueprint(jobs_bp, url_prefix='/api')
    app.register_blueprint(applications_bp, url_prefix='/api')
    app.register_blueprint(courses_bp, url_prefix='/api')
    app.register_blueprint(indicators_bp, url_prefix='/api')
    app.register_blueprint(enrollments_bp, url_prefix='/api')