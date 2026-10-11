from datetime import date
from pathlib import Path
import tempfile
import streamlit as st
import pandas as pd

from hansard_scraper import prepare_mps_file, run_scraper

st.set_page_config(page_title="NSW Hansard Research Tool", page_icon="🏛️", layout="wide")
st.title("NSW Hansard Research Tool")
st.write("Generate a spreadsheet of verified wage-policy quotes from NSW Parliament Hansard.")

st.info(
    "This first version uses the MP list and keyword groups already embedded in the existing "
    "Colab notebook. The controls below change the date range; the target MPs and keywords "
    "can be made editable in a later version."
)

left, right = st.columns(2)
with left:
    start_date = st.date_input("Start date", value=date(2023, 3, 1))
with right:
    end_date = st.date_input("End date", value=date(2026, 9, 24))

if start_date > end_date:
    st.error("The start date must be on or before the end date.")
    st.stop()

if st.button("Generate spreadsheet", type="primary", use_container_width=True):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        mps_path = temp / "mps.csv"
        quotes_path = temp / "wage_quotes.csv"
        audit_path = temp / "speaker_label_audit.csv"

        prepare_mps_file(str(mps_path))
        status = st.status("Scraper running. This may take several minutes.", expanded=True)
        try:
            # Capture the scraper's print output so the user sees activity in the app.
            import contextlib
            import io
            log_stream = io.StringIO()
            with contextlib.redirect_stdout(log_stream):
                run_scraper(
                    start=start_date.isoformat(),
                    end=end_date.isoformat(),
                    mps_file=str(mps_path),
                    out_file=str(quotes_path),
                    audit_file=str(audit_path),
                )
            status.update(label="Scraping finished.", state="complete", expanded=False)

            if quotes_path.exists():
                df = pd.read_csv(quotes_path)
                st.success(f"Finished. Extracted {len(df):,} verified quote rows.")
                st.dataframe(df.head(20), use_container_width=True)
                st.download_button(
                    "Download quotes spreadsheet (CSV)",
                    data=quotes_path.read_bytes(),
                    file_name="wage_quotes.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            else:
                st.warning("The scraper finished but did not create a quotes file.")
            if audit_path.exists():
                st.download_button(
                    "Download speaker-label audit (CSV)",
                    data=audit_path.read_bytes(),
                    file_name="speaker_label_audit.csv",
                    mime="text/csv",
                )
            with st.expander("Run log"):
                st.text(log_stream.getvalue()[-12000:] or "No log output captured.")
        except Exception as exc:
            status.update(label="Scraper failed.", state="error", expanded=True)
            st.exception(exc)
            st.error("Check the error above before trying again.")
