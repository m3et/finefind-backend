import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.app import app
from app.auth.jwt import parse_jwt_user_data
from app.auth.models import AuthUser, JWTData
from app.auth.service import create_user
from app.services.sqlalchemy import create_tables  # Import your create_tables function


# TODO: move it to be packase scoped
# Asynchronous fixture to create a database
@pytest_asyncio.fixture(autouse=True, scope="module")
async def create_tables_fixture():
    await create_tables()
    await create_user(
        AuthUser(username="mock_user@mock.com", password="MockPassword123")
    )


# Create a test client using the FastAPI app
client = TestClient(app)


# Mock dependency to override JWT parsing in tests
def override_parse_jwt_user_data():
    return JWTData(user_id=1, is_admin=False)  # Mock JWT data


# Apply dependency override
app.dependency_overrides[parse_jwt_user_data] = override_parse_jwt_user_data


@pytest.fixture(scope="module")
def auth_headers():
    return {"Authorization": "Bearer mocktoken"}


@pytest.fixture(scope="module")
def demo_tasks():
    return [
        {
            "title": "Task 1",
            "description": "First test task",
            "status": "pending",
            "priority": "high",
            "due_date": "2024-12-31T23:59:59Z",
            "assigned_to": 1,
            "tags": ["test", "demo"],
            "estimated_time": "PT1H",
            "actual_time": "PT0.5H",
            "parent_task_id": None,
            "recurrence_rule": None,
        },
        {
            "title": "Task 2",
            "description": "Second test task",
            "status": "in_progress",
            "priority": "medium",
            "due_date": "2024-12-25T23:59:59Z",
            "assigned_to": 2,
            "tags": ["example", "demo"],
            "estimated_time": "PT2H",
            "actual_time": "PT1H",
            "parent_task_id": None,
            "recurrence_rule": None,
        },
        {
            "title": "Task 3",
            "description": "Third test task",
            "status": "done",
            "priority": "low",
            "due_date": "2024-12-20T23:59:59Z",
            "assigned_to": 3,
            "tags": ["sample", "demo"],
            "estimated_time": "PT3H",
            "actual_time": "PT2H",
            "parent_task_id": None,
            "recurrence_rule": None,
        },
    ]


@pytest.fixture(scope="module")
def create_tasks(demo_tasks, auth_headers):
    task_ids = []
    for task in demo_tasks:
        response = client.post("/tasks/", json=task, headers=auth_headers)
        assert response.status_code == 200
        task_ids.append(response.json()["id"])
    return task_ids


@pytest.mark.asyncio
async def test_create_tasks(demo_tasks, auth_headers):
    for task in demo_tasks:
        response = client.post("/tasks/", json=task, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == task["title"]


@pytest.mark.asyncio
async def test_get_all_tasks(create_tasks, auth_headers):
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= len(create_tasks)


@pytest.mark.asyncio
async def test_get_task(create_tasks, auth_headers):
    task_id = create_tasks[0]
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_update_task(create_tasks, demo_tasks, auth_headers):
    task_id = create_tasks[0]
    updated_task = demo_tasks[0].copy()
    updated_task["id"] = task_id
    updated_task["title"] = "Updated Task 1"
    response = client.put(f"/tasks/{task_id}", json=updated_task, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task 1"


@pytest.mark.asyncio
async def test_delete_task(create_tasks, auth_headers):
    task_id = create_tasks[0]
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    # Confirm the task is deleted
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_non_existent_task(auth_headers):
    non_existent_id = 9999
    response = client.get(f"/tasks/{non_existent_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_non_existent_task(demo_tasks, auth_headers):
    non_existent_id = 9999
    updated_task = demo_tasks[0].copy()
    updated_task["id"] = non_existent_id
    updated_task["title"] = "Non-existent Task"
    response = client.put(
        f"/tasks/{non_existent_id}", json=updated_task, headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_non_existent_task(auth_headers):
    non_existent_id = 9999
    response = client.delete(f"/tasks/{non_existent_id}", headers=auth_headers)
    assert response.status_code == 404
