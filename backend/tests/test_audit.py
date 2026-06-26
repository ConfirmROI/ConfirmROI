import pytest

from app.extensions import db
from tests.conftest import enterpriseskip

try:
    from app.models.audit_log import AuditLog
except ImportError:
    AuditLog = None


@enterpriseskip
class TestAuditLogAssumptions:
    def test_create_assumption_logs_audit(self, client, auth_headers, app):
        resp = client.post("/api/formulas/assumptions", headers=auth_headers, json={
            "key": "test_key",
            "label": "Test Label",
            "data_type": "number",
            "default_value": 100,
            "change_reason": "Initial creation for testing",
        })
        assert resp.status_code == 201
        assumption_id = resp.get_json()["id"]

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="assumption", entity_id=assumption_id
            ).all()
            assert len(entries) == 1
            assert entries[0].action == "create"
            assert entries[0].change_reason == "Initial creation for testing"

    def test_update_assumption_logs_audit_with_diff(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas/assumptions", headers=auth_headers, json={
            "key": "hours_saved",
            "label": "Hours Saved",
            "data_type": "number",
            "default_value": 50,
        })
        assumption_id = create_resp.get_json()["id"]

        resp = client.put(f"/api/formulas/assumptions/{assumption_id}", headers=auth_headers, json={
            "label": "Hours Saved Per Week",
            "default_value": 80,
            "change_reason": "Updated based on new survey data",
        })
        assert resp.status_code == 200

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="assumption", entity_id=assumption_id
            ).order_by(AuditLog.created_at).all()
            assert len(entries) == 2
            update_entry = entries[1]
            assert update_entry.action == "update"
            assert update_entry.change_reason == "Updated based on new survey data"
            assert update_entry.changes is not None
            assert "label" in update_entry.changes
            assert update_entry.changes["label"]["old"] == "Hours Saved"
            assert update_entry.changes["label"]["new"] == "Hours Saved Per Week"
            assert "default_value" in update_entry.changes

    def test_update_assumption_no_change_reason(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas/assumptions", headers=auth_headers, json={
            "key": "no_reason",
            "label": "No Reason",
            "data_type": "number",
            "default_value": 10,
        })
        assumption_id = create_resp.get_json()["id"]

        client.put(f"/api/formulas/assumptions/{assumption_id}", headers=auth_headers, json={
            "default_value": 20,
        })

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="assumption", entity_id=assumption_id, action="update"
            ).all()
            assert len(entries) == 1
            assert entries[0].change_reason is None

    def test_delete_assumption_logs_audit(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas/assumptions", headers=auth_headers, json={
            "key": "to_delete",
            "label": "To Delete",
            "data_type": "number",
            "default_value": 5,
        })
        assumption_id = create_resp.get_json()["id"]

        resp = client.delete(f"/api/formulas/assumptions/{assumption_id}", headers=auth_headers, json={
            "change_reason": "No longer needed",
        })
        assert resp.status_code == 204

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="assumption", entity_id=assumption_id, action="delete"
            ).all()
            assert len(entries) == 1
            assert entries[0].change_reason == "No longer needed"


@enterpriseskip
class TestAuditLogFormulas:
    def test_create_formula_logs_audit(self, client, auth_headers, app):
        resp = client.post("/api/formulas", headers=auth_headers, json={
            "name": "Custom ROI",
            "formula": "revenue - cost",
            "assumptions": [
                {"key": "revenue", "label": "Revenue", "data_type": "currency", "default_value": 50000},
                {"key": "cost", "label": "Cost", "data_type": "currency", "default_value": 10000},
            ],
            "change_reason": "Creating formula for Q3 planning",
        })
        assert resp.status_code == 201
        arch_id = resp.get_json()["id"]

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="formula", entity_id=arch_id
            ).all()
            assert len(entries) == 1
            assert entries[0].action == "create"
            assert entries[0].change_reason == "Creating formula for Q3 planning"

    def test_update_formula_logs_audit_with_diff(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas", headers=auth_headers, json={
            "name": "Original Name",
            "formula": "a + b",
        })
        arch_id = create_resp.get_json()["id"]

        resp = client.put(f"/api/formulas/{arch_id}", headers=auth_headers, json={
            "name": "Updated Name",
            "formula": "a + b + c",
            "change_reason": "Adding variable c for more accuracy",
        })
        assert resp.status_code == 200

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="formula", entity_id=arch_id, action="update"
            ).all()
            assert len(entries) == 1
            assert entries[0].changes is not None
            assert "name" in entries[0].changes
            assert entries[0].changes["name"]["old"] == "Original Name"
            assert entries[0].changes["name"]["new"] == "Updated Name"
            assert entries[0].change_reason == "Adding variable c for more accuracy"

    def test_delete_formula_logs_audit(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas", headers=auth_headers, json={
            "name": "To Delete",
            "formula": "x",
        })
        arch_id = create_resp.get_json()["id"]

        resp = client.delete(f"/api/formulas/{arch_id}", headers=auth_headers, json={
            "change_reason": "Deprecated formula",
        })
        assert resp.status_code == 204

        with app.app_context():
            entries = AuditLog.query.filter_by(
                entity_type="formula", entity_id=arch_id, action="delete"
            ).all()
            assert len(entries) == 1
            assert entries[0].change_reason == "Deprecated formula"

@enterpriseskip

class TestAuditAPI:
    def test_get_audit_history(self, client, auth_headers, app):
        create_resp = client.post("/api/formulas/assumptions", headers=auth_headers, json={
            "key": "audit_test",
            "label": "Audit Test",
            "data_type": "number",
            "default_value": 1,
        })
        assumption_id = create_resp.get_json()["id"]

        client.put(f"/api/formulas/assumptions/{assumption_id}", headers=auth_headers, json={
            "default_value": 99,
            "change_reason": "Adjusting default",
        })

        resp = client.get(
            f"/api/audit?entity_type=assumption&entity_id={assumption_id}",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 2
        actions = [d["action"] for d in data]
        assert "create" in actions
        assert "update" in actions
        update_entry = [d for d in data if d["action"] == "update"][0]
        assert update_entry["change_reason"] == "Adjusting default"
        assert update_entry["user_name"] == "Test User"

    def test_get_audit_history_missing_params(self, client, auth_headers):
        resp = client.get("/api/audit", headers=auth_headers)
        assert resp.status_code == 400

    def test_get_audit_history_no_auth(self, client):
        resp = client.get("/api/audit?entity_type=assumption&entity_id=1")
        assert resp.status_code == 401

    def test_get_audit_history_empty(self, client, auth_headers):
        resp = client.get(
            "/api/audit?entity_type=assumption&entity_id=99999",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.get_json() == []
