from .ingestion import process_ingestion, reset_table


if __name__ == "__main__":
    reset_table()
    process_ingestion()
