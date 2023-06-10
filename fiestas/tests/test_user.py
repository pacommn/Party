import pytest

from fiestas.models import Usuarios

@pytest.fixture
def user_creation():
    return Usuarios(
        usuario='user2',
        correo='user@example.com',
        contrasena='holahola',
        admin=1
    )

@pytest.mark.django_db
def test_common_user_creation_usuario(user_creation):
    user_creation.save()
    assert user_creation.usuario == 'user2'

@pytest.mark.django_db
def test_common_user_creation_correo(user_creation):
    user_creation.save()
    assert user_creation.correo == 'user@example.com'


@pytest.mark.django_db
def test_common_user_creation_admin(user_creation):
    user_creation.save()
    assert user_creation.admin == 1

@pytest.mark.django_db
def test_common_user_creation_contrasena(user_creation):
    user_creation.save()
    assert user_creation.contrasena == 'holahola'