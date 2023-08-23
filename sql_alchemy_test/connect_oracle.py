from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine, text, inspect

# Create the database engine
engine = create_engine('oracle+cx_oracle://sys:Mafadu120c@192.168.80.2:1521/ORCLCDB?mode=sysdba',echo=True)

#sql_drop_parcours = text('DROP TABLE IF EXISTS parcours')
sql_drop_students = """
BEGIN
       EXECUTE IMMEDIATE 'DROP TABLE students';
    EXCEPTION
       WHEN OTHERS THEN
          IF SQLCODE != -942 THEN
             RAISE;
          END IF;
    END;
"""

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
    result_drop_students = conn.execute(text(sql_drop_students))
    result_drop_parcours = conn.execute(text(sql_drop_parcours))
print(result_drop_parcours)
print(result_drop_students)

meta = MetaData()

parcours = Table(
    'parcours', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=100))
)

students = Table(
    'students', meta,
    Column('id', Integer, primary_key=True),
    Column('firstname', String(length=100)),
    Column('lastname', String(length=100)),
    Column('parcours_id', Integer, ForeignKey("parcours.id")),
)

meta.create_all(engine)

# Execute a simple SQL query
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM parcours"))
    for row in result:
        print(row)

inspector = inspect(engine)

tables_name = inspector.get_table_names()
print("Nom des tables:",tables_name)

columns_name=inspector.get_columns(table_name='parcours')
print("Nom des colonnes de la table parcours:",columns_name)



