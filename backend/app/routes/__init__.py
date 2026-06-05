from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.project_routes import project_bp
from app.routes.mentor_routes import mentor_bp
from app.routes.sprint_routes import sprint_bp
from app.routes.task_routes import task_bp
from app.routes.member_routes import member_bp
from app.routes.rating_routes import rating_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(rating_bp)
