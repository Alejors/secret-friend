from src.interfaces import IDataRepository


class SQLAlchemyBaseRepository(IDataRepository):
    def __init__(self, sqlalchemy_client, query_class=None, entity=None):
        """
        Constructor del repositorio base.

        :param sqlalchemy_client: Cliente de SQLAlchemy para manejar sesiones.
        :param query_class: Modelo de base de datos asociado.
        :param entity: Clase de la entidad de dominio asociada.
        """
        self.session_factory = sqlalchemy_client.session_factory
        self.query_class = query_class
        self.entity = entity

    def get(
        self,
        *,
        filters: dict = None,
        special_filters: list = None,
        first_only: bool = False,
    ):
        with self.session_factory() as session:
            query = session.query(self.query_class)

            if filters:
                query = query.filter_by(**filters)
            
            if special_filters:
                query = query.filter(*special_filters)

            if first_only:
                results = query.first()
                if self.entity:
                    return self.entity.from_model(results) if results else None
                return results
            else:
                results = query.all()
                if self.entity:
                    return [self.entity.from_model(result) for result in results if result]
                return results

    def insert(
        self,
        data: dict,
    ):
        with self.session_factory() as session:
            instance = self.query_class.from_dict(data)
            session.add(instance)
            session.commit()
            if self.entity:
                return self.entity.from_model(instance) if instance else None
            return instance

    def update(
        self,
        id: int,
        fields: dict,
    ):
        with self.session_factory() as session:
            query = session.query(self.query_class).filter_by(id=id)
            query.update(fields)
            instance = query.first()

            session.commit()
            
            if self.entity:
                return self.entity.from_model(instance) if instance else None
            return instance
