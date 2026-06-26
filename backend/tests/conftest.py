import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import User, UserRole, UserTier
from app.models.team import Team, TeamMember, TeamMemberRole


def is_enterprise_installed():
    try:
        import confirmroi_enterprise  # noqa: F401
        return True
    except ImportError:
        return False


enterpriseskip = pytest.mark.skipif(
    not is_enterprise_installed(),
    reason="Enterprise package not installed",
)


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def auth_user(app):
    with app.app_context():
        user = User(
            email="test@example.com",
            password_hash="$2b$12$examplehash",
            name="Test User",
            role=UserRole.user,
            tier=UserTier.free,
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        return user_id


@pytest.fixture
def auth_headers(app, auth_user):
    with app.app_context():
        token = create_access_token(identity=str(auth_user))
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def team_id(app, auth_user):
    with app.app_context():
        team = Team(name="Test Team", manager_user_id=auth_user)
        db.session.add(team)
        db.session.flush()
        db.session.add(TeamMember(
            team_id=team.id, user_id=auth_user, role=TeamMemberRole.manager
        ))
        db.session.commit()
        return team.id
