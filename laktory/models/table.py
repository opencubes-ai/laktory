import json
from typing import Literal
from typing import Any

from pydantic import computed_field
from pydantic import model_validator

from laktory._logger import get_logger
from laktory.sql import value_to_statement
from laktory.models.base import BaseModel
from laktory.models.column import Column
from laktory.models.sources.tablesource import TableSource
from laktory.models.sources.eventsource import EventSource

logger = get_logger(__name__)


class Table(BaseModel):
    name: str
    columns: list[Column] = []
    primary_key: str = None
    comment: str = None
    catalog_name: str = None
    database_name: str = None

    # Data
    data: list[list[Any]] = None

    # Lakehouse
    event_source: EventSource = None
    table_source: TableSource = None
    zone: Literal["BRONZE", "SILVER", "SILVER_STAR", "GOLD"] = None
    pipeline_name: str = None
    # joins
    # expectations

    # ----------------------------------------------------------------------- #
    # Validators                                                              #
    # ----------------------------------------------------------------------- #

    @model_validator(mode="after")
    def assign_table_to_columns(self) -> Any:
        for c in self.columns:
            c.table_name = self.name
            c.catalog_name = self.catalog_name
            c.database_name = self.database_name

    # ----------------------------------------------------------------------- #
    # Computed fields                                                         #
    # ----------------------------------------------------------------------- #

    @computed_field
    @property
    def parent_full_name(self) -> str:
        _id = ""
        if self.catalog_name:
            _id += self.catalog_name

        if self.database_name:
            if _id == "":
                _id = self.database_name
            else:
                _id += f".{self.database_name}"

        return _id

    @computed_field
    @property
    def full_name(self) -> str:
        _id = self.name
        if self.parent_full_name is not None:
            _id = f"{self.parent_full_name}.{_id}"
        return _id

    @computed_field
    @property
    def schema_name(self) -> str:
        return self.database_name

    # ----------------------------------------------------------------------- #
    # Properties                                                              #
    # ----------------------------------------------------------------------- #

    @property
    def column_names(self):
        return [c.name for c in self.columns]

    @property
    def df(self):
        import pandas as pd
        return pd.DataFrame(data=self.data, columns=self.column_names)

    # ----------------------------------------------------------------------- #
    # Class Methods                                                           #
    # ----------------------------------------------------------------------- #

    @classmethod
    def meta_table(cls):

        # Build columns
        columns = []
        for k, t in cls.model_serialized_types().items():
            jsonize = False
            if k in ["columns", "event_source", "table_source"]:
                t = "string"
                jsonize = True

            elif k in ["data"]:
                continue

            columns += [
                Column(name=k, type=t, jsonize=jsonize)
            ]

        # Set table
        return Table(
            name="tables",
            database_name="laktory",
            columns=columns,
        )

    # ----------------------------------------------------------------------- #
    # Methods                                                                 #
    # ----------------------------------------------------------------------- #

    def exists(self):
        return self.name in [c.name for c in self.workspace_client.tables.list(
            catalog_name=self.catalog_name,
            schema_name=self.schema_name,
        )]

    def create(self,
               if_not_exists: bool = True,
               or_replace: bool = False,
               insert_data: bool = False,
               warehouse_id: str = None,
               ):

        if len(self.columns) == 0:
            raise ValueError()

        if or_replace:
            if_not_exists = False

        statement = f"CREATE "
        if or_replace:
            statement += "OR REPLACE "
        statement += "TABLE "
        if if_not_exists:
            statement += "IF NOT EXISTS "

        statement += f"{self.schema_name}.{self.name}"

        statement += "\n   ("
        for c in self.columns:
            t = c.type
            if c.jsonize:
                t = "string"
            statement += f"{c.name} {t},"
        statement = statement[:-1]
        statement += ")"

        logger.info(statement)
        r = self.workspace_client.execute_statement_and_wait(
            statement,
            warehouse_id=warehouse_id,
            catalog_name=self.catalog_name
        )

        if insert_data:
            self.insert()

        return r

    def delete(self, force: bool = False):
        self.workspace_client.tables.delete(self.full_name, force=force)

    def insert(self, warehouse_id: str = None):

        statement = f"INSERT INTO {self.full_name} VALUES\n"
        for row in self.data:
            statement += "   ("
            values = [json.dumps(v) if c.jsonize else v for c, v in zip(self.columns, row)]
            values = [value_to_statement(v) for v in values]
            statement += ", ".join(values)
            statement += "),\n"

        statement = statement[:-2]

        logger.info(statement)
        r = self.workspace_client.execute_statement_and_wait(
            statement,
            warehouse_id=warehouse_id,
            catalog_name=self.catalog_name
        )

        return r

    def select(self, limit=10, warehouse_id: str = None, load_json=True):

        statement = f"SELECT * from {self.full_name} limit {limit}"

        r = self.workspace_client.execute_statement_and_wait(
            statement,
            warehouse_id=warehouse_id,
            catalog_name=self.catalog_name
        )

        data = r.result.data_array

        if load_json:
            for i in range(len(data)):
                j = -1
                for c, v in zip(self.columns, data[i]):
                    j += 1
                    if c.jsonize:
                        data[i][j] = json.loads(data[i][j])

        return data
