from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine, text, inspect

# Create the database engine
engine = create_engine('oracle+cx_oracle://sys:Mafadu120c@192.168.80.2:1521/ORCLCDB?mode=sysdba',echo=True)

#sql_drop_parcours = text('DROP TABLE IF EXISTS parcours')
sql_drop_parcours = """
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE parcours';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
"""
with engine.connect() as conn:
   result = conn.execute(text(sql_drop_parcours))
print(result)

meta = MetaData()

parcours = Table(
   'parcours', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String(length=100))
)

meta.create_all(engine)

# Execute a simple SQL query
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM parcours"))
    for row in result:
        print(row)

inspector = inspect(engine)

tables_name = inspector.get_table_names()
print(tables_name)

columns_name=inspector.get_columns(table_name='parcours')
print(columns_name)

