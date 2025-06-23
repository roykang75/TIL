from sqlalchemy import inspect

def row_to_dict(row):
  return {key: getattr(row, key) for key in inspect(row).attrs.keys()}