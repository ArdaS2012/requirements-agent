# Requirement Project

This project is now organized around a small package instead of a single large script.

## Layout

- `setup_database.py`: thin root entrypoint that runs the ingestion flow
- `requirements_ingestion/`: modular package containing the extracted application code
- `legacy/setup_database_original.py`: preserved copy of the original all-in-one script
- `data/raw/`: source PDFs
- `data/extracted_images/`: extracted page images
- `outputs/`: generated markdown outputs
- `database_raw`, `extracted_images`, `output.md`, `output_w_hf.md`: compatibility links kept so existing references still work

## Run

```bash
python setup_database.py
```
