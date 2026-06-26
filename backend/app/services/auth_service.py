from passlib.context import CryptContext
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import db
from app.models.user import User, UserRole, UserTier
from app.models.user_identity import UserIdentity
from app.models.team import Team, TeamMember, TeamMemberRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LocalAuthProvider:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService:
    @staticmethod
    def register(email: str, password: str, name: str = None):
        existing = User.query.filter_by(email=email).first()
        if existing:
            return None, "Email already registered"

        tier_str = current_app.config.get("DEFAULT_USER_TIER", "free")
        tier = UserTier.paid if tier_str == "paid" else UserTier.free

        user = User(
            email=email,
            password_hash=LocalAuthProvider.hash_password(password),
            name=name,
            role=UserRole.user,
            tier=tier,
        )
        db.session.add(user)
        db.session.flush()

        identity = UserIdentity(
            user_id=user.id,
            provider="local",
            provider_user_id=email,
        )
        db.session.add(identity)

        team = Team(
            name=f"{name or email.split('@')[0]}'s Team",
            manager_user_id=user.id,
        )
        db.session.add(team)
        db.session.flush()

        member = TeamMember(
            team_id=team.id,
            user_id=user.id,
            role=TeamMemberRole.manager,
        )
        db.session.add(member)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, None

    @staticmethod
    def login(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if not user or not user.password_hash:
            return None, "Invalid email or password"

        if not LocalAuthProvider.verify_password(password, user.password_hash):
            return None, "Invalid email or password"

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, None

    @staticmethod
    def auto_login():
        user = User.query.first()
        if not user:
            return None, "No user found"

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            uid = int(user_id)
        except (ValueError, TypeError):
            return None
        return db.session.get(User, uid)
