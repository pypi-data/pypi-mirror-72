from sqlalchemy import Column, func, text
from sqlalchemy import Integer, DateTime

def common_columns():
    return [
        Column("id"        , Integer , primary_key=True, autoincrement=True),
        Column("created_at", DateTime, index=True, server_default=func.current_timestamp()),
        Column("updated_at", DateTime, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    ]
