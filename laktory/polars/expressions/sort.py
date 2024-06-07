import polars as pl
from laktory.polars.expressions._common import (
    EXPR_OR_NAME,
    INT_OR_EXPR,
    FLOAT_OR_EXPR,
    STRING_OR_EXPR,
)

__all__ = [
    "row_number",
]


def row_number(
) -> pl.Expr:
    """
    Window function: returns a sequential number starting at 1 within a window partition.

    Returns
    -------
    :
        Output column

    Examples
    --------
    ```py
    import laktory  # noqa: F401
    import polars as pl

    df = pl.DataFrame({"x": ["a", "a", "b", "b", "b", "c"]})
    df = df.with_columns(y1=pl.Expr.laktory.row_number())
    df = df.with_columns(y2=pl.Expr.laktory.row_number().over("x"))
    print(df.glimpse(return_as_string=True))
    '''
    Rows: 6
    Columns: 3
    $ x  <str> 'a', 'a', 'b', 'b', 'b', 'c'
    $ y1 <i64> 1, 2, 3, 4, 5, 6
    $ y2 <i64> 1, 2, 1, 2, 3, 1
    '''
    ```
    """
    return pl.int_range(1, pl.len()+1)
