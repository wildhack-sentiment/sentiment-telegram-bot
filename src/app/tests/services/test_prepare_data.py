import pytest

from app.services import PrepareData

pytestmark = [pytest.mark.django_db]


def test_load_params():
    service = PrepareData()

    params = service.load_params()

    assert params == {}
