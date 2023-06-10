import pytest

from fiestas.models import Entradas

@pytest.fixture
def entrada_creation():
    return Entradas(
        tipo='N',
        coste=15,
        dni='12345678f',
        cantidad=2,
        nombre='pepe'
    )

@pytest.mark.django_db
def test_common_entrada_creation_nombre(entrada_creation):
    entrada_creation.save()
    assert entrada_creation.nombre == 'pepe'

@pytest.mark.django_db
def test_common_entrada_creation_tipo(entrada_creation):
    entrada_creation.save()
    assert entrada_creation.tipo == 'N'


@pytest.mark.django_db
def test_common_entrada_creation_coste(entrada_creation):
    entrada_creation.save()
    assert entrada_creation.coste == 15

@pytest.mark.django_db
def test_common_entrada_creation_cantidad_dni(entrada_creation):
    entrada_creation.save()
    assert entrada_creation.cantidad == 2 and entrada_creation.dni == '12345678f'