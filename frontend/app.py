import streamlit as st
import requests
import re
import os
from datetime import datetime

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(
    page_title="DeepResearch AI",
    page_icon="🧠",
    layout="wide"
)

if "current_report" not in st.session_state:
    st.session_state.current_report = None
if "current_critique" not in st.session_state:
    st.session_state.current_critique = None
if "current_query" not in st.session_state:
    st.session_state.current_query = ""
if "current_source_index" not in st.session_state:
    st.session_state.current_source_index = {}

def clean_text(text):
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;)", "&amp;", text)
    text = text.replace("**", "").replace("*", "")
    text = re.sub(r"\|", " ", text)

    unicode_map = {
        "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
        "\u2015": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"',
        "\u201d": '"', "\u2022": "-", "\u2026": "...", "\u00a0": " ",
        "\u00b7": "-", "\u2212": "-"
    }
    for char, replacement in unicode_map.items():
        text = text.replace(char, replacement)

    text = re.sub(r" {2,}", " ", text)
    return text.strip()

def generate_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]
    body_style.leading = 20

    elements = []
    lines = report_text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = clean_text(line)

        if line.startswith("# "):
            elements.append(Paragraph(line.replace("# ", "", 1), title_style))
            elements.append(Spacer(1, 20))
        elif line.startswith("## "):
            elements.append(Paragraph(line.replace("## ", "", 1), heading_style))
            elements.append(Spacer(1, 14))
        elif line.startswith("* ") or line.startswith("- "):
            elements.append(Paragraph(f"• {line[2:]}", body_style))
            elements.append(Spacer(1, 8))
        elif line.startswith("---"):
            elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph(line, body_style))
            elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)
    return buffer

with st.sidebar:
    st.header("📚 Research History")
    try:
        mem_response = requests.get(f"{BACKEND_URL}/memory")
        if mem_response.status_code == 200:
            history_data = mem_response.json()
            if history_data:
                for idx, item in enumerate(reversed(history_data[-10:])):
                    with st.expander(f"🔍 {item.get('query', 'Unknown Query')}"):
                        snippet = item.get('report', '')[:150] + "..."
                        st.write(snippet)
                        
                        if st.button("Load Report", key=f"load_{idx}"):
                            st.session_state.current_report = item.get('report')
                            st.session_state.current_critique = item.get('critique', {})
                            st.session_state.current_query = item.get('query', '')
                            st.rerun()
            else:
                st.info("No research history yet.")
        else:
            st.warning("No memory found.")
    except Exception as e:
        st.error("Could not connect to Backend Memory API.")


st.title("🧠 DeepResearch AI")
st.markdown("### Stateful Multi-Agent Research System")

query = st.text_area(
    "Enter your research topic:",
    value=st.session_state.current_query,
    height=150,
    placeholder="Example: Future of AI agents in software engineering"
)

if st.button("Generate Research Report"):
    if not query.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Running AI Research Workflow..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/research",
                json={"query": query}
            )
            response.raise_for_status()
            data = response.json()

            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"reports/report_{timestamp}.md", "w", encoding="utf-8") as f:
                f.write(data["report"])

            st.session_state.current_report = data.get("report")
            st.session_state.current_critique = data.get("critique", {})
            st.session_state.current_query = query
            st.session_state.current_source_index = data.get("source_index", {})
            st.success("Research Completed Successfully!")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Backend API Error: {e}")

st.markdown("---")

if st.session_state.current_report:
    st.markdown("# 📄 Research Report")
    st.markdown(st.session_state.current_report)

    pdf_file = generate_pdf(st.session_state.current_report)

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_file,
        file_name="research_report.pdf",
        mime="application/pdf"
    )

    st.markdown("---")

    critique = st.session_state.current_critique
    if critique:
        st.markdown("# 🧠 Critic Evaluation")

        st.metric(
            label="Critic Score",
            value=f"{critique.get('score', 'N/A')}/10"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## ✅ Strengths")
            for item in critique.get("strengths", []):
                st.write(f"- {item}")

        with col2:
            st.markdown("## ❌ Weaknesses")
            for item in critique.get("weaknesses", []):
                st.write(f"- {item}")

        st.markdown("## ⚠️ Missing Topics")
        for item in critique.get("missing_topics", []):
            st.write(f"- {item}")

        citation_quality = critique.get("citation_quality", {})
        if citation_quality:
            st.markdown("## 📎 Citation Quality")
            cq_col1, cq_col2 = st.columns(2)
            with cq_col1:
                has_inline = citation_quality.get("has_inline_citations", False)
                st.metric("Inline Citations", "✅ Yes" if has_inline else "❌ No")
            with cq_col2:
                has_sources = citation_quality.get("has_sources_section", False)
                st.metric("Sources Section", "✅ Yes" if has_sources else "❌ No")
            if citation_quality.get("notes"):
                st.caption(citation_quality["notes"])

        st.markdown("## 📝 Final Verdict")
        st.info(critique.get("final_verdict", "No verdict available."))