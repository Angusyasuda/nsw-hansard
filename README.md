# NSW Hansard Research Tool

A Streamlit interface around the existing NSW Hansard wage-policy scraper.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL (usually http://localhost:8501). Open it in a browser.

## Current behaviour

- Uses the MP list and direct/euphemism keyword lists carried over from the supplied Colab notebook.
- Lets the user select a start and end date.
- Generates a CSV of verified quotes and a speaker-label audit CSV.
- This is a first-pass conversion. Review results and test the app locally before deploying.

## Before sharing or deploying

- Keep API keys/secrets out of source files (the current notebook does not appear to require an API key).
- Confirm the scraper's results and output columns match your research needs.
- For private use by Nayoen, check the current access-control options of the hosting provider before publishing.
