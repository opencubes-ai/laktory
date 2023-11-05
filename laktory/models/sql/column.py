from typing import Union
from typing import Any
from pydantic import computed_field
from pydantic import field_validator
from pydantic import model_validator
import pyspark.sql.functions as F
from pyspark.sql.connect.column import Column

from laktory._logger import get_logger
from laktory.contants import SUPPORTED_TYPES
from laktory.models.base import BaseModel
from laktory.spark import functions as LF

logger = get_logger(__name__)


class SparkFuncArg(BaseModel):
    value: Any
    to_column: bool = None
    to_lit: bool = None

    @model_validator(mode="after")
    def is_column_default(self) -> Any:
        if self.to_lit is None:
            if not isinstance(self.value, str):
                self.to_lit = True
            else:
                self.to_column = True

        if self.to_column and self.to_lit:
            raise ValueError("Only one of `to_column` or `to_lit` can be True")

        return self


class Column(BaseModel):
    catalog_name: Union[str, None] = None
    comment: Union[str, None] = None
    name: str
    pii: Union[bool, None] = None
    schema_name: Union[str, None] = None
    spark_func_args: list[Union[str, SparkFuncArg]] = []
    spark_func_kwargs: dict[str, Union[Any, SparkFuncArg]] = {}
    spark_func_name: Union[str, None] = None
    sql_expression: Union[str, None] = None
    table_name: Union[str, None] = None
    type: str = "string"
    unit: Union[str, None] = None

    @field_validator("spark_func_args")
    def parse_args(cls, args: list[Union[str, SparkFuncArg]]) -> list[SparkFuncArg]:
        _args = []
        for a in args:
            if not isinstance(a, SparkFuncArg):
                a = SparkFuncArg(value=a)
            _args += [a]
        return _args

    @field_validator("spark_func_kwargs")
    def parse_kwargs(
        cls, kwargs: dict[str, Union[str, SparkFuncArg]]
    ) -> dict[str, SparkFuncArg]:
        _kwargs = {}
        for k, a in kwargs.items():
            if not isinstance(a, SparkFuncArg):
                a = SparkFuncArg(value=a)
            _kwargs[k] = a
        return _kwargs

    @field_validator("type")
    def default_load_path(cls, v: str) -> str:
        if "<" in v:
            return v
        else:
            if v not in SUPPORTED_TYPES:
                raise ValueError(
                    f"Type {v} is not supported. Select one of {SUPPORTED_TYPES}"
                )
        return v

    # ----------------------------------------------------------------------- #
    # Computed fields                                                         #
    # ----------------------------------------------------------------------- #

    @property
    def parent_full_name(self) -> str:
        _id = ""
        if self.catalog_name:
            _id += self.catalog_name

        if self.schema_name:
            if _id == "":
                _id = self.schema_name
            else:
                _id += f".{self.schema_name}"

        if self.table_name:
            if _id == "":
                _id = self.table_name
            else:
                _id += f".{self.table_name}"

        return _id

    @property
    def full_name(self) -> str:
        _id = self.name
        if self.parent_full_name is not None:
            _id = f"{self.parent_full_name}.{_id}"
        return _id

    @property
    def database_name(self) -> str:
        return self.schema_name

    # ----------------------------------------------------------------------- #
    # Class Methods                                                           #
    # ----------------------------------------------------------------------- #

    def to_spark(self, df) -> Column:
        # From SQL expression
        if self.sql_expression:
            logger.info(f"   {self.name}[{self.type}] as `{self.sql_expression}`)")
            return F.expr(self.sql_expression).alias(self.name).cast(self.type)

        # From Spark Function
        func_name = self.spark_func_name
        if func_name is None:
            func_name = "coalesce"

        # TODO: Add support for custom functions
        # if udf_name in udfuncs.keys():
        #     f = udfuncs[udf_name]
        # else:
        #     f = getattr(F, udf_name)

        # Get function and args
        f = getattr(F, func_name, None)
        if f is None:
            f = getattr(LF, func_name, None)
        if f is None:
            raise ValueError(f"Function {func_name} is not available")
        _args = self.spark_func_args
        _kwargs = self.spark_func_kwargs

        logger.info(f"   {self.name}[{self.type}] as {func_name}({_args}, {_kwargs})")

        # Build args
        args = []
        expected_cols = 0
        found_cols = 0
        for i, _arg in enumerate(_args):
            if df is not None:
                if _arg.to_column:
                    expected_cols += 1
                    if not df.has_column(_arg.value):
                        # When columns are not found, they are simply skipped and a
                        # warning is issued. Some functions, like `coalesce` might list
                        # multiple arguments, but don't expect all of them to be
                        # available
                        logger.warning(f"Column '{_arg.value}' not available")
                        continue
                    else:
                        found_cols += 1

            arg = _arg.value
            if _arg.to_column:
                arg = F.expr(_arg.value)
            elif _arg.to_lit:
                arg = F.lit(_arg.value)

            # TODO: Review if required
            # if _arg.value.startswith("data.") or func_name == "coalesce":
            #     pass
            # input_type = dict(df.dtypes)[input_col_name]
            # if input_type in ["double"]:
            #     # Some bronze NaN data will be converted to 0 if cast to int
            #     input_col = F.when(F.isnan(input_col_name), None).otherwise(F.col(input_col_name))
            # if self.type not in ["_any"] and func_name not in [
            #     "to_safe_timestamp"
            # ]:
            #     input_col = F.col(input_col_name).cast(self.type)

            args += [arg]

        if expected_cols > 0 and found_cols == 0:
            raise ValueError(
                f"None of the inputs columns ({_args}) for {self.name} have been found"
            )

        # Build kwargs
        kwargs = {}
        for k, _arg in _kwargs.items():
            arg = _arg.value
            if _arg.to_column:
                arg = F.expr(_arg.value)
            elif _arg.to_lit:
                arg = F.lit(_arg.value)
            kwargs[k] = arg

        return f(*args, **kwargs).cast(self.type)