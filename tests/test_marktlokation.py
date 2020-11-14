from typing import Tuple

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
            marktlokations_id="51238696781",
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
                marktlokations_id="51238696781",
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

    @pytest.mark.parametrize(
        "malo_id_valid",
        [
            ("51238696781", True),
            ("41373559241", True),
            ("56789012345", True),
            ("52935155442", True),
            ("12345678910", False),
            ("asdasd", False),
            ("   ", False),
            ("  asdasdasd ", False),
            ("keine malo id", False),
            (None, False),
            ("", False),
        ],
    )
    def test_id_validation(self, malo_id_valid: Tuple[str, bool]):
        def _instantiate_malo(malo_id: str):
            _ = Marktlokation(
                marktlokations_id=malo_id,
                sparte=Sparte.GAS,
                lokationsadresse=Adresse(
                    postleitzahl="82031", ort="Grünwald", hausnummer="27A", strasse="Nördliche Münchner Straße"
                ),
                energierichtung=Energierichtung.EINSP,
                bilanzierungsmethode=Bilanzierungsmethode.PAUSCHAL,
                unterbrechbar=True,
                netzebene=Netzebene.NSP,
            )

        if not malo_id_valid[1]:
            with pytest.raises(ValueError):
                _instantiate_malo(malo_id_valid[0])
        else:
            _instantiate_malo(malo_id_valid[0])
