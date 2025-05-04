from marshmallow import Schema, fields

class EnrollmentSchema(Schema):
    id_curso = fields.Int(attribute="id_curso", required=True)
    id_usuario = fields.Int(attribute="id_usuario", required=True)
    fecha_inscripcion = fields.DateTime(attribute="fecha_inscripcion", dump_only=True)