from app.extensions import db
from app.models.team import Team


_access_provider = None


def set_access_provider(provider):
    global _access_provider
    _access_provider = provider


def get_visible_team_ids(user):
    if _access_provider:
        return _access_provider.get_visible_team_ids(user)
    return [t.id for t in Team.query.filter_by(manager_user_id=user.id).all()]


def check_project_access(project, user):
    if _access_provider:
        return _access_provider.check_project_access(project, user)
    team = db.session.get(Team, project.team_id)
    return team is not None and team.manager_user_id == user.id


def check_team_access(team, user):
    if _access_provider:
        return _access_provider.check_team_access(team, user)
    return team.manager_user_id == user.id
