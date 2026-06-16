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
if "current_research_data" not in st.session_state:
    st.session_state.current_research_data = []
if "revision_count" not in st.session_state:
    st.session_state.revision_count = 0
if "report_approved" not in st.session_state:
    st.session_state.report_approved = False

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
                            st.session_state.report_approved = True
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

    # Reset state for new research
    st.session_state.report_approved = False
    st.session_state.revision_count = 0

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
            st.session_state.current_research_data = data.get("research_data", [])
            st.session_state.revision_count = data.get("revision_count", 0)
            st.session_state.report_approved = False
            st.success("Research Completed Successfully!")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Backend API Error: {e}")

st.markdown("---")

if st.session_state.current_report:

    # --- Revision Info Badge ---
    rev_count = st.session_state.revision_count
    if rev_count > 0:
        st.info(f"🔄 This report has been revised **{rev_count}** time{'s' if rev_count > 1 else ''}.")

    if st.session_state.report_approved:
        st.success("✅ Report has been approved!")

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

        # --- Revision Suggestions ---
        revision_suggestions = critique.get("revision_suggestions", [])
        if revision_suggestions:
            st.markdown("## 💡 Revision Suggestions")
            for item in revision_suggestions:
                st.write(f"- {item}")

        st.markdown("## 📝 Final Verdict")
        st.info(critique.get("final_verdict", "No verdict available."))

    # ============================================
    # Human-in-the-Loop: Approve / Reject
    # ============================================
    if not st.session_state.report_approved:
        st.markdown("---")
        st.markdown("# 🤝 Human-in-the-Loop")
        st.markdown("**Report is ready for your review. Do you approve?**")

        hitl_col1, hitl_col2 = st.columns(2)

        with hitl_col1:
            if st.button("✅ Approve Report", use_container_width=True, type="primary"):
                st.session_state.report_approved = True
                st.success("✅ Report approved and finalized!")
                st.rerun()

        with hitl_col2:
            if st.button("❌ Request Revision", use_container_width=True):
                st.session_state["show_revision_input"] = True

        # --- Revision Feedback Input ---
        if st.session_state.get("show_revision_input", False):
            st.markdown("### 📝 What should be improved?")
            user_feedback = st.text_area(
                "Your feedback for the revision:",
                height=120,
                placeholder="e.g., Add more details about security risks, expand the conclusion...",
                key="revision_feedback_input"
            )

            if st.button("🚀 Submit Revision", type="primary"):
                if not user_feedback.strip():
                    st.warning("Please provide feedback for the revision.")
                else:
                    with st.spinner("🔄 Revising report based on your feedback..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/revise",
                                json={
                                    "query": st.session_state.current_query,
                                    "report": st.session_state.current_report,
                                    "user_feedback": user_feedback,
                                    "research_data": st.session_state.current_research_data,
                                    "source_index": st.session_state.current_source_index,
                                    "revision_count": st.session_state.revision_count
                                }
                            )
                            response.raise_for_status()
                            data = response.json()

                            st.session_state.current_report = data["report"]
                            st.session_state.current_critique = data["critique"]
                            st.session_state.revision_count = data["revision_count"]
                            st.session_state["show_revision_input"] = False

                            # Save revised report
                            os.makedirs("reports", exist_ok=True)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            with open(f"reports/report_revised_{timestamp}.md", "w", encoding="utf-8") as f:
                                f.write(data["report"])

                            st.success(f"✅ Revision #{data['revision_count']} completed!")
                            st.rerun()

                        except requests.exceptions.RequestException as e:
                            st.error(f"Revision API Error: {e}")