import streamlit as st
import requests
import re
import os
from datetime import datetime
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


def clean_text(text):
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)

    text = re.sub(
        r"&(?!amp;|lt;|gt;|quot;|apos;)",
        "&amp;",
        text
    )

    text = text.replace("**", "").replace("*", "")

    text = re.sub(r"\|", " ", text)

    unicode_map = {
        "\u2011": "-",   # non-breaking hyphen
        "\u2012": "-",   # figure dash
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2015": "-",   # horizontal bar
        "\u2018": "'",   # left single quotation mark
        "\u2019": "'",   # right single quotation mark
        "\u201c": '"',   # left double quotation mark
        "\u201d": '"',   # right double quotation mark
        "\u2022": "-",   # bullet
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u00b7": "-",   # middle dot
        "\u2212": "-",   # minus sign
    }
    for char, replacement in unicode_map.items():
        text = text.replace(char, replacement)

    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def generate_pdf(report_text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
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
            text = line.replace("# ", "", 1)

            elements.append(
                Paragraph(text, title_style)
            )

            elements.append(
                Spacer(1, 20)
            )

        elif line.startswith("## "):
            text = line.replace("## ", "", 1)

            elements.append(
                Paragraph(text, heading_style)
            )

            elements.append(
                Spacer(1, 14)
            )

        elif line.startswith("* ") or line.startswith("- "):
            text = line[2:]

            bullet = f"• {text}"

            elements.append(
                Paragraph(bullet, body_style)
            )

            elements.append(
                Spacer(1, 8)
            )

        elif line.startswith("---"):

            elements.append(
                Spacer(1, 12)
            )

        else:

            elements.append(
                Paragraph(line, body_style)
            )

            elements.append(
                Spacer(1, 10)
            )

    doc.build(elements)

    buffer.seek(0)
    return buffer

st.title("🧠 DeepResearch AI")

st.markdown(
    "### Stateful Multi-Agent Research System"
)

query = st.text_area(
    "Enter your research topic:",
    height=200,
    placeholder="Example: Future of AI agents in software engineering"
)

if st.button("Generate Research Report"):

    if not query.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Running AI Research Workflow..."):
        response = requests.post(
            "http://127.0.0.1:8000/research",
            json={"query": query}
        )
        data = response.json()

        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        with open(
            f"reports/report_{timestamp}.md",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(data["report"])

    st.success("Research Completed Successfully!")
    st.markdown("---")

    st.markdown("# 📄 Research Report")
    st.markdown(data["report"])

    pdf_file = generate_pdf(data["report"])

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_file,
        file_name="research_report.pdf",
        mime="application/pdf"
    )

    st.markdown("---")

    critique = data["critique"]

    st.markdown("# 🧠 Critic Evaluation")

    st.metric(
        label="Critic Score",
        value=f"{critique['score']}/10"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## ✅ Strengths")
        for item in critique["strengths"]:
            st.write(f"- {item}")

    with col2:
        st.markdown("## ❌ Weaknesses")
        for item in critique["weaknesses"]:
            st.write(f"- {item}")

    st.markdown("## ⚠️ Missing Topics")
    for item in critique["missing_topics"]:
        st.write(f"- {item}")

    st.markdown("## 📝 Final Verdict")
    st.info(critique["final_verdict"])