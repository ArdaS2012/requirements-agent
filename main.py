from src.ingestion import process_ingestion, reset_table
from app import app

if __name__ == "__main__":
    # Set need_reset = True the first time you run the app, or whenever you
    # want to re-ingest documents (e.g. after adding new PDFs to data/raw/).
    # Set it back to False afterwards to skip ingestion and go straight to the UI.
    need_reset = False
    if need_reset:
        reset_table()       # truncate existing vectors
        process_ingestion() # parse PDFs, embed chunks, insert into PostgreSQL

    print("Starting ReqBot web interface at http://localhost:5000")
    app.run(debug=True, port=5000)
