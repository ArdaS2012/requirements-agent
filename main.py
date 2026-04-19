from src.ingestion import process_ingestion, reset_table
from src.agent import start_agent

if __name__ == "__main__":
    need_reset = False  # Set this flag based on your requirement
    if need_reset:
        reset_table()
        process_ingestion()
    start_agent()
