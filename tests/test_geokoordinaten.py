import pytest
import jsons
from decimal import Decimal

from bo4e.com.geokoordinaten import Geokoordinaten


class TestGeokoordinaten:
    def test_serialization(self):
        geo = Geokoordinaten(
            breitengrad=Decimal(52.52149200439453),
            laengengrad=Decimal(13.404866218566895),
        )

        json_string = geo.dumps(
            strip_nulls=True,
            key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE,
            jdkwargs={"ensure_ascii": False},
        )

        assert "breitengrad" in json_string
        assert str(geo.breitengrad) in json_string

        deserialized_geo: Geokoordinaten = Geokoordinaten.loads(
            json_string, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
        )

        assert geo.breitengrad == deserialized_geo.breitengrad

    def test_wrong_datatype(self):
        with pytest.raises(TypeError) as excinfo:

            geo = Geokoordinaten(breitengrad="54,23", laengengrad=-23.2)

        assert "breitengrad" in str(excinfo.value)