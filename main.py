from src.database.schema import create_tables

def main():
    create_tables()
    print("Database initialized.")

if __name__ == "__main__":
    main()