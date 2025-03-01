from utility.SQLProvider import SQLProvider
from dotenv import load_dotenv

load_dotenv()

sqlProvider = SQLProvider()

def show_tables():
    try:
        # Exécutez une requête pour obtenir les noms des tables
        tables = sqlProvider.get("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        
        if tables:
            print("Tables dans la base de données :")
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                
                # Obtenir les colonnes de la table
                columns = sqlProvider.get(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
                if columns:
                    print("Colonnes :")
                    for column in columns:
                        print(f" - {column[0]}")  # Chaque colonne est un tuple, donc on accède au premier élément
                else:
                    print("Aucune colonne trouvée dans cette table.")
        else:
            print("Aucune table trouvée dans la base de données.")
    
    except Exception as e:
        print("Une erreur est survenue lors de la récupération des tables :", e)

if __name__ == "__main__":
    show_tables()