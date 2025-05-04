from marshmallow import Schema, fields, post_load, pre_dump

class CourseSchema(Schema):
    IdCurso = fields.Int(attribute="IdCurso", dump_only=True)
    Titulo = fields.Str(attribute="Titulo", required=True)
    Descripcion = fields.Str(attribute="Descripcion", required=True)
    Accesibilidad = fields.Str(attribute="Accesibilidad", required=True)
    URLContenido = fields.Str(attribute="URLContenido", required=True)
    
    @post_load
    def make_course(self, data, **kwargs):
        # Transformaciones específicas para curso
        return data
    
    @pre_dump
    def prepare_course(self, data, **kwargs):
        # Manejo específico para campos encriptados
        return data