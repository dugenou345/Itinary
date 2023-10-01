import subprocess

def main():
    # Call the other script using subprocess
    subprocess.call(['python', 'source/data_normalisation/data_normalisation.py'])
    subprocess.call(['python', 'source/neo4j/import_POI_mongo_to_neo4j.py'])

if __name__ == '__main__':
    main()