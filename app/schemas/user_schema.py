from marshmallow import Schema, fields, post_load, pre_dump

class UserSchema(Schema):
    IdUsuario = fields.Int(attribute="IdUsuario", dump_only=True)
    NombreCompleto = fields.Str(attribute="NombreCompleto", required=True)
    Correo = fields.Str(attribute="Correo", required=True)
    Contrasena = fields.Str(attribute="Contrasena", required=True, load_only=True)
    Rol = fields.Str(attribute="Rol", required=True)
    IdDiscapacidad = fields.Int(attribute="IdDiscapacidad", allow_none=True)
    FechaRegistro = fields.DateTime(attribute="FechaRegistro", dump_only=True)
    
    # Hook para procesar los datos después de deserializar
    @post_load
    def make_user(self, data, **kwargs):
        # Aquí podríamos realizar cualquier transformación necesaria
        return data
    
    # Hook para procesar los datos antes de serializar
    @pre_dump
    def prepare_user(self, data, **kwargs):
        # Aseguramos que los datos encriptados se manejen correctamente
        return data