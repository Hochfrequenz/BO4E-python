import pytest
import jsons

from bo4e.bo.marktlokation import Marktlokation
from bo4e.com.adresse import Adresse
from bo4e.enum.bilanzierungsmethode import Bilanzierungsmethode
from bo4e.enum.energierichtung import Energierichtung
from bo4e.enum.sparte import Sparte
from bo4e.enum.netzebene import Netzebene


class TestMaLo:
    def test_serialization(self):
        malo = Marktlokation(
            marktlokations_id="54321012345",
            sparte=Sparte.GAS,
            lokationsadresse=Adresse(
                postleitzahl="04177", ort="Leipzig", hausnummer="1", strasse="Jahnalle"
            ),
            energierichtung=Energierichtung.EINSP,
            bilanzierungsmethode=Bilanzierungsmethode.PAUSCHAL,
            unterbrechbar=True,  # optional attribute
            netzebene=Netzebene.NSP,
        )
        assert malo.versionstruktur == 2, "versionstruktur was not automatically set"
        assert malo.bo_typ == "MARKTLOKATION", "boTyp was not automatically set"

        json_string = malo.dumps(
            strip_nulls=True,
            key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE,
            jdkwargs={"ensure_ascii": False},
        )

        assert (
                "boTyp" in json_string
        ), "No camel case serialization"  # camel case serialization
        assert (
                "marktlokationsId" in json_string
        ), "No camel case serialization"  # camel case serialization

        deserialized_malo: Marktlokation = Marktlokation.loads(
            json_string, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
        )

        assert malo.marktlokations_id == deserialized_malo.marktlokations_id
        assert malo.marktlokations_id is not deserialized_malo.marktlokations_id

    def test_address_validation(self):
        with pytest.raises(ValueError) as excinfo:
            malo = Marktlokation(
                marktlokations_id="54321012345",
                sparte=Sparte.GAS,
                lokationsadresse=Adresse(
                    postleitzahl="04177",
                    ort="Leipzig",
                    hausnummer="1",
                    strasse="Jahnalle",
                ),
                energierichtung=Energierichtung.EINSP,
                bilanzierungsmethode=Bilanzierungsmethode.PAUSCHAL,
                unterbrechbar=True,  # optional attribute
                netzebene=Netzebene.NSP,
                geoadresse="test",
                katasterinformation="test",
            )

        assert "No or more than one address information is given." == str(excinfo.value)

    def test_id_validation(self):
        with pytest.raises(ValueError):
            _ = Marktlokation(
                marktlokations_id="asdasdasdas",
                sparte=Sparte.GAS,
                lokationsadresse=Adresse(
                    postleitzahl="04177", ort="Leipzig", hausnummer="1", strasse="Jahnalle"
                ),
                energierichtung=Energierichtung.EINSP,
                bilanzierungsmethode=Bilanzierungsmethode.PAUSCHAL,
                unterbrechbar=True,  # optional attribute
                netzebene=Netzebene.NSP,
            )
