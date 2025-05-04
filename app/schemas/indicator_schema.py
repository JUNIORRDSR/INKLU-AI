from marshmallow import Schema, fields, post_load, pre_dump

class IndicatorSchema(Schema):
    IdIndicador = fields.Int(attribute="IdIndicador", dump_only=True)
    IdUsuario = fields.Int(attribute="IdUsuario", required=True)
    Tipo = fields.Str(attribute="Tipo", required=True)
    Valor = fields.Decimal(attribute="Valor", required=True)
    FechaRegistro = fields.DateTime(attribute="FechaRegistro", dump_only=True)
    
    @post_load
    def make_indicator(self, data, **kwargs):
        # Aquí podríamos aplicar transformaciones específicas
        return data
    
    @pre_dump
    def prepare_indicator(self, data, **kwargs):
        # Aseguramos que los datos encriptados se manejan correctamente
        return data