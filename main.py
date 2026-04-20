from src.ingestion import process_ingestion, reset_table
from app import app

if __name__ == "__main__":
    need_reset = False  # Set this flag based on your requirement
    if need_reset:
        reset_table()
        process_ingestion()

    print("Starting ReqBot web interface at http://localhost:5000")
    app.run(debug=True, port=5000)
