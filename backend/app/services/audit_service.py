_audit_backend = None


def set_audit_backend(backend):
    global _audit_backend
    _audit_backend = backend


class AuditService:
    @staticmethod
    def log_change(user_id, entity_type, entity_id, action, changes=None, change_reason=None):
        if _audit_backend:
            return _audit_backend.log_change(user_id, entity_type, entity_id, action, changes, change_reason)

    @staticmethod
    def get_entity_history(entity_type, entity_id):
        if _audit_backend:
            return _audit_backend.get_entity_history(entity_type, entity_id)
        return []

    @staticmethod
    def diff_fields(old_dict, new_dict):
        changes = {}
        for key in set(list(old_dict.keys()) + list(new_dict.keys())):
            old_val = old_dict.get(key)
            new_val = new_dict.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}
        return changes if changes else None
