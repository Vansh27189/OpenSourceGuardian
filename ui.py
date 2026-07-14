import streamlit as st
from app.services.repository_service import analyse_repo
from app.llm.llm_client import ask_llm
from app.llm.prompt import build_report_prompt  # PDF REPORT FEATURE: import new prompt
from fpdf import FPDF  # PDF REPORT FEATURE: import pdf library

st.set_page_config(page_title="OpenSourceGuardian", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}



/* Input box */
.stTextInput > div > div > input {
    background-color: #EDE6D6 !important;
    border: 1px solid #C8B89A !important;
    border-radius: 8px !important;
    color: #2C2416 !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7C5C2E !important;
    box-shadow: 0 0 0 2px rgba(124, 92, 46, 0.15) !important;
}



/* Metric cards */
[data-testid="stMetric"] {
    background-color: #EDE6D6;
    border: 1px solid #C8B89A;
    border-radius: 10px;
    padding: 1rem;
}

/* Expander */
details {
    background-color: #EDE6D6 !important;
    border: 1px solid #C8B89A !important;
    border-radius: 8px !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #EDE6D6 !important;
    border: 1px solid #C8B89A !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}

/* Alerts */
.stSuccess { border-left: 3px solid #7C5C2E !important; background-color: rgba(124, 92, 46, 0.08) !important; }
.stWarning { border-left: 3px solid #B8860B !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background-color: #F2EDE3; }
::-webkit-scrollbar-thumb { background: #C8B89A; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7C5C2E; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ OpenSourceGuardian")
st.caption("Scan GitHub repositories and ask security questions")

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "messages" not in st.session_state:
    st.session_state.messages = []

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repo"
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Scan Repository", type="primary"):
        if not repo_url.strip():
            st.warning("Please enter a repository URL.")
        else:
            with st.spinner("Scanning repository..."):
                st.session_state.scan_result = analyse_repo(repo_url.strip())
                st.session_state.messages = []
            st.success("Scan complete.")

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []

# PDF REPORT FEATURE: function to convert LLM text to downloadable PDF
def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, text=line)
    return bytes(pdf.output())

if st.session_state.scan_result:
    result = st.session_state.scan_result

    st.subheader("Scan Summary")

    m1, m2, m3 = st.columns(3)
    m1.metric("Repository", result['repository'].split("/")[-1])
    m2.metric("Language", result['language'])
    m3.metric("Packages Checked", len(result['report']))

    unpinned = [r for r in result['report'] if r['package']['version'] is None]
    if unpinned:
        st.warning(
            f"⚠️ **{len(unpinned)} out of {len(result['report'])} packages have no version pinned.** "
            f"OSV returns all historical advisories for unpinned packages, so vulnerability counts may appear much higher than what actually affects you. "
            f"Pin versions in your requirements file and rescan for accurate results."
        )

    with st.expander("View Raw Scan Report"):
        st.json(result)

    # PDF REPORT FEATURE: button to generate and download PDF report
    if st.button("📄 Export PDF Report"):
        with st.spinner("Generating report..."):
            report_text = ask_llm(result["report"], build_report_prompt(result["report"]))
            pdf_bytes = generate_pdf(report_text)
        st.download_button("⬇️ Download PDF", pdf_bytes, "security_report.pdf", "application/pdf")

    st.subheader("Ask Questions")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something like: Is this repo safe?")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_llm(result["report"], question)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})