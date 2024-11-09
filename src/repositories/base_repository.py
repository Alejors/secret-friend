class SQLAlchemyBaseRepository:
    def __init__(self, sqlalchemy_client, query_class=None):
        self.session_factory = sqlalchemy_client.session_factory
        self.query_class = query_class

    def get(
      self,
      *,
      filters: dict = None,
      first_only: bool = False,
    ):
      with self.session_factory() as session:
        query = session.query(self.query_class)

        if filters:
          query = query.filter_by(**filters)

        if first_only:
          results = query.first()
          return results
        else:
          results = query.all()
          return results

    def insert(
        self,
        instance,
    ):
      with self.session_factory() as session:
        session.add(instance)
        session.commit()
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

        return instance
