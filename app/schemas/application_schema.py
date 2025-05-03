from marshmallow import Schema, fields

class ApplicationSchema(Schema):
    IdPostulacion = fields.Int(attribute="IdPostulacion", dump_only=True)
    IdUsuario = fields.Int(attribute="IdUsuario", required=True)
    IdVacante = fields.Int(attribute="IdVacante", required=True)
    FechaPostulacion = fields.DateTime(attribute="FechaPostulacion", dump_only=True)
    Estado = fields.Str(attribute="Estado", default='Pendiente')