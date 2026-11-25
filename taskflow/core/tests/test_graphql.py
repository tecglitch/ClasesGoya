import pytest
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Project, Task


@pytest.mark.django_db
def test_graphql_filtra_por_membresia_y_requiere_jwt(cliente, ana, proyecto):
    Task.objects.create(project=proyecto, title="Visible")
    ajeno = Project.objects.create(name="Privado")
    Task.objects.create(project=ajeno, title="Oculta")

    anonima = cliente.post(
        "/graphql/", {"query": "{ allProjects { name } }"}, format="json"
    )
    assert anonima.status_code == 200
    assert anonima.json()["data"]["allProjects"] == []

    token = str(AccessToken.for_user(ana))
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = cliente.post(
        "/graphql/",
        {"query": "{ allProjects { name tasks { title } } }"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["data"]["allProjects"] == [
        {"name": "Proyecto de Ana", "tasks": [{"title": "Visible"}]}
    ]


@pytest.mark.django_db
def test_graphql_mutation_respeta_rol_y_validacion(cliente, ana, beto, proyecto):
    admin_token = str(AccessToken.for_user(ana))
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    creada = cliente.post(
        "/graphql/",
        {
            "query": (
                f'mutation {{ createTask(projectId: "{proyecto.id}", '
                'title: "GraphQL", priority: "alta") { ok task { title } } }'
            )
        },
        format="json",
    )
    assert creada.json()["data"]["createTask"]["ok"] is True

    invalida = cliente.post(
        "/graphql/",
        {
            "query": (
                f'mutation {{ createTask(projectId: "{proyecto.id}", '
                'title: "Inválida", priority: "urgente") { ok } }'
            )
        },
        format="json",
    )
    assert "errors" in invalida.json()

    member_token = str(AccessToken.for_user(beto))
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {member_token}")
    denegada = cliente.post(
        "/graphql/",
        {
            "query": (
                f'mutation {{ createTask(projectId: "{proyecto.id}", '
                'title: "No autorizada") { ok } }'
            )
        },
        format="json",
    )
    assert "errors" in denegada.json()
