from marshmallow import Schema, fields, post_load, pre_dump

class JobSchema(Schema):
    IdVacante = fields.Int(attribute="IdVacante", dump_only=True)
    IdEmpresa = fields.Int(attribute="IdEmpresa", required=True)
    Titulo = fields.Str(attribute="Titulo", required=True)
    Descripcion = fields.Str(attribute="Descripcion", required=True)
    Requisitos = fields.Str(attribute="Requisitos", required=True)
    FechaPublicacion = fields.DateTime(attribute="FechaPublicacion", dump_only=True)
    
    @post_load
    def make_job(self, data, **kwargs):
        # Aquí podríamos aplicar transformaciones específicas
        return data
    
    @pre_dump
    def prepare_job(self, data, **kwargs):
        # Manejo específico para campos encriptados
        return data