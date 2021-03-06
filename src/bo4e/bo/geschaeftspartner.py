import attr

from marshmallow import fields
from marshmallow_enum import EnumField
from typing import List

from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt, GeschaeftsobjektSchema
from bo4e.com.adresse import Adresse, AdresseSchema
from bo4e.enum.anrede import Anrede
from bo4e.enum.kontaktart import Kontaktart
from bo4e.enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from bo4e.enum.botyp import BoTyp


@attr.s(auto_attribs=True, kw_only=True)
class Geschaeftspartner(Geschaeftsobjekt):
    """
    Object containing information about a Geschaeftspartner
    """

    # required attributes
    bo_typ: BoTyp = attr.ib(default=BoTyp.GESCHAEFTSPARTNER)
    name1: str
    gewerbekennzeichnung: bool
    geschaeftspartnerrolle: List[Geschaeftspartnerrolle] = attr.ib(validator=attr.validators.instance_of(List))

    # optional attributes
    anrede: Anrede = attr.ib(default=None)
    name2: str = attr.ib(default=None)
    name3: str = attr.ib(default=None)
    hrnummer: str = attr.ib(default=None)
    amtsgericht: str = attr.ib(default=None)
    kontaktweg: List[Kontaktart] = attr.ib(default=[])
    umsatzsteuer_id: str = attr.ib(default=None)
    glaeubiger_id: str = attr.ib(default=None)
    e_mail_adresse: str = attr.ib(default=None)
    website: str = attr.ib(default=None)
    partneradresse: Adresse = attr.ib(default=None)


class GeschaeftspartnerSchema(GeschaeftsobjektSchema):
    # class_name is needed to use the correct schema for deserialisation.
    # see function `deserialise` in geschaeftsobjekt.py
    class_name = Geschaeftspartner

    # required attributes
    name1 = fields.Str()
    gewerbekennzeichnung = fields.Bool()
    geschaeftspartnerrolle = fields.List(EnumField(Geschaeftspartnerrolle))

    # optional attributes
    anrede = EnumField(Anrede, missing=None)
    name2 = fields.Str(missing=None)
    name3 = fields.Str(missing=None)
    hrnummer = fields.Str(missing=None)
    amtsgericht = fields.Str(missing=None)
    kontaktweg = fields.List(EnumField(Kontaktart), missing=None)
    umsatzsteuer_id = fields.Str(missing=None)
    glaeubiger_id = fields.Str(missing=None)
    e_mail_adresse = fields.Str(missing=None)
    website = fields.Str(missing=None)
    partneradresse = fields.Nested(AdresseSchema, missing=None)
