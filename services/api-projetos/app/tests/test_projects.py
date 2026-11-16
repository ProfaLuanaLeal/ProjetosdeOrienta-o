from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        # Avoid entering the app lifespan, which initializes the configured
        # development database. Requests use the isolated in-memory test DB.
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def project_payload() -> dict[str, str]:
    return {
        "title": "Sistema de biblioteca",
        "description": "Aplicação para gestão de empréstimos.",
        "student_name": "Ana Silva",
        "advisor_name": "Prof. Carlos Souza",
        "status": "planned",
    }


def test_create_and_get_project(client: TestClient) -> None:
    create_response = client.post("/projects", json=project_payload())

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["title"] == "Sistema de biblioteca"

    get_response = client.get(f"/projects/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created


def test_list_projects_supports_pagination(client: TestClient) -> None:
    first = client.post("/projects", json=project_payload())
    second_payload = project_payload() | {"title": "Aplicativo educacional"}
    second = client.post("/projects", json=second_payload)

    assert first.status_code == 201
    assert second.status_code == 201

    response = client.get("/projects", params={"skip": 1, "limit": 1})

    assert response.status_code == 200
    assert [project["title"] for project in response.json()] == ["Aplicativo educacional"]


def test_update_project(client: TestClient) -> None:
    created = client.post("/projects", json=project_payload()).json()

    response = client.patch(
        f"/projects/{created['id']}",
        json={"status": "in_progress", "description": "Escopo atualizado."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["description"] == "Escopo atualizado."
    assert response.json()["title"] == "Sistema de biblioteca"


def test_delete_project(client: TestClient) -> None:
    created = client.post("/projects", json=project_payload()).json()

    response = client.delete(f"/projects/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/projects/{created['id']}").status_code == 404


def test_missing_project_returns_404(client: TestClient) -> None:
    response = client.get("/projects/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_create_project_requires_mandatory_fields(client: TestClient) -> None:
    response = client.post("/projects", json={"title": "Projeto incompleto"})

    assert response.status_code == 422
