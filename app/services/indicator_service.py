from app.models.indicator import Indicator
from app.schemas.indicator_schema import IndicatorSchema
from app.extensions import db

class IndicatorService:
    @staticmethod
    def create_indicator(data):
        """Crea un nuevo indicador"""
        try:
            indicator = Indicator()
            indicator.IdUsuario = data.get('IdUsuario')
            indicator.Tipo = data.get('Tipo')
            indicator.Valor = data.get('Valor')  # Será encriptado automáticamente
            
            db.session.add(indicator)
            db.session.commit()
            
            indicator_schema = IndicatorSchema()
            return indicator_schema.dump(indicator)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_indicator(indicator_id):
        """Obtiene un indicador por su ID"""
        indicator = Indicator.query.get(indicator_id)
        if not indicator:
            return None
            
        indicator_schema = IndicatorSchema()
        return indicator_schema.dump(indicator)

    @staticmethod
    def update_indicator(indicator_id, data):
        """Actualiza un indicador existente"""
        indicator = Indicator.query.get(indicator_id)
        if not indicator:
            return None
            
        try:
            if 'IdUsuario' in data:
                indicator.IdUsuario = data.get('IdUsuario')
            if 'Tipo' in data:
                indicator.Tipo = data.get('Tipo')
            if 'Valor' in data:
                indicator.Valor = data.get('Valor')  # Será encriptado automáticamente
                
            db.session.commit()
            
            indicator_schema = IndicatorSchema()
            return indicator_schema.dump(indicator)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_indicator(indicator_id):
        """Elimina un indicador por su ID"""
        indicator = Indicator.query.get(indicator_id)
        if not indicator:
            return False
            
        try:
            db.session.delete(indicator)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_indicators():
        """Obtiene todos los indicadores"""
        indicators = Indicator.query.all()
        indicator_schema = IndicatorSchema(many=True)
        return indicator_schema.dump(indicators)