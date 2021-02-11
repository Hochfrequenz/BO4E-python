"""
Contains Katasteradresse class
and corresponding marshmallow schema for de-/serialization
"""
import attr
from marshmallow import Schema, fields, post_load

from bo4e.cases import JavaScriptMixin
from bo4e.com.com import COM

# pylint: disable=too-few-public-methods
@attr.s(auto_attribs=True, kw_only=True)
class Katasteradresse(COM):
    """
    Dient der Adressierung über die Liegenschafts-Information.
    """

    gemarkung_flur: str
    flurstueck: str


class KatasteradresseSchema(Schema, JavaScriptMixin):
    """
    Schema for de-/serialization of Katasteradresse.
    Inherits from Schema and JavaScriptMixin.
    """

    gemarkung_flur = fields.Str()
    flurstueck = fields.Str()

    # pylint: disable=no-self-use, unused-argument
    @post_load
    def deserialise(self, data, **kwargs) -> Katasteradresse:
        """ Deserialize JSON to Katasteradresse object """
        return Katasteradresse(**data)
