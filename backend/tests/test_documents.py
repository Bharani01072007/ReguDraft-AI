import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def auth_headers(client: TestClient):
    # Register and login a test user to retrieve JWT token
    user_payload = {
        "email": "docwriter@regudraft.com",
        "password": "passwords123",
        "role": "WRITER"
    }
    client.post("/api/v1/auth/register", json=user_payload)
    
    login_data = {
        "username": "docwriter@regudraft.com",
        "password": "passwords123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_document_lifecycle(client: TestClient, auth_headers: dict):
    # 1. Create Project
    proj_response = client.post(
        "/api/v1/projects/",
        json={"name": "Cancer Study 2026", "description": "Phase 3 clinical trial"},
        headers=auth_headers
    )
    assert proj_response.status_code == 201
    project_id = proj_response.json()["id"]

    # 2. Create Document
    doc_response = client.post(
        f"/api/v1/projects/{project_id}/documents",
        json={"name": "Aspirin study report - Aspirin", "type": "CSR"},
        headers=auth_headers
    )
    assert doc_response.status_code == 201
    doc_data = doc_response.json()
    assert doc_data["status"] == "DRAFT"
    doc_id = doc_data["id"]

    # 3. Generate Draft
    gen_response = client.post(
        f"/api/v1/documents/{doc_id}/generate",
        headers=auth_headers
    )
    assert gen_response.status_code == 200
    gen_data = gen_response.json()
    assert gen_data["status"] == "IN_REVIEW"
    assert "version_id" in gen_data

    # 4. Fetch Document Details
    detail_response = client.get(
        f"/api/v1/documents/{doc_id}",
        headers=auth_headers
    )
    assert detail_response.status_code == 200
    detail_data = detail_response.json()
    assert detail_data["status"] == "IN_REVIEW"
    assert detail_data["current_version"] is not None
    assert detail_data["compliance_report"] is not None
    assert detail_data["compliance_report"]["compliance_score"] >= 90.0

    # 5. Submit Human-in-the-Loop Review Approval
    approve_response = client.post(
        f"/api/v1/documents/{doc_id}/submit-review",
        json={
            "action": "APPROVE",
            "comments": ["Good to export."]
        },
        headers=auth_headers
    )
    assert approve_response.status_code == 200, approve_response.json()
    approve_data = approve_response.json()
    assert approve_data["status"] == "EXPORTED"
    assert "pdf" in approve_data["exports"]
    assert "docx" in approve_data["exports"]

def test_refine_endpoint(client: TestClient, auth_headers: dict):
    payload = {
        "content": "This is raw trial clinical safety text.",
        "action": "IMPROVE"
    }
    response = client.post(
        "/api/v1/documents/refine",
        json=payload,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "refined_content" in data

def test_delete_document(client: TestClient, auth_headers: dict):
    # 1. Create Project
    proj_response = client.post(
        "/api/v1/projects/",
        json={"name": "Delete Test Project", "description": "Testing document deletion"},
        headers=auth_headers
    )
    assert proj_response.status_code == 201
    project_id = proj_response.json()["id"]

    # 2. Create Document
    doc_response = client.post(
        f"/api/v1/projects/{project_id}/documents",
        json={"name": "Temporary Doc to Delete", "type": "CSR"},
        headers=auth_headers
    )
    assert doc_response.status_code == 201
    doc_id = doc_response.json()["id"]

    # 3. Delete Document
    delete_response = client.delete(
        f"/api/v1/documents/{doc_id}",
        headers=auth_headers
    )
    assert delete_response.status_code == 204

    # 4. Try to fetch the deleted document
    get_response = client.get(
        f"/api/v1/documents/{doc_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404
