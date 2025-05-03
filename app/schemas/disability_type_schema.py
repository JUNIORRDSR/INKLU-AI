from marshmallow import Schema, fields

class DisabilityTypeSchema(Schema):
    IdDiscapacidad = fields.Int(attribute="IdDiscapacidad", dump_only=True)
    Nombre = fields.Str(attribute="Nombre", required=True)
    Descripcion = fields.Str(attribute="Descripcion", required=False)