from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings

engine = create_async_engine(settings.DATABASE_URL)


def serialize_column(column):
    return {
        "name": column["name"],
        "type": str(column["type"]),
        "nullable": column["nullable"],
        "default": column.get("default"),
        "autoincrement": column.get("autoincrement"),
    }


async def get_database_structure():

    async with engine.connect() as conn:

        def inspect_database(sync_conn):
            inspector = inspect(sync_conn)

            result = {}

            for database in inspector.get_schema_names():
                tables = {}

                for table in inspector.get_table_names(schema=database):
                    tables[table] = {
                        "columns": [
                            serialize_column(column)
                            for column in inspector.get_columns(
                                table,
                                schema=database,
                            )
                        ],
                        "primary_key": inspector.get_pk_constraint(
                            table,
                            schema=database,
                        ),
                        "foreign_keys": inspector.get_foreign_keys(
                            table,
                            schema=database,
                        ),
                        "indexes": inspector.get_indexes(
                            table,
                            schema=database,
                        ),
                    }

                result[database] = tables

            return result

        return await conn.run_sync(inspect_database)
