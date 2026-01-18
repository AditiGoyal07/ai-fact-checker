import streamlit as st
import pandas as pd
from claim_extractor import extract_text_from_pdf, extract_claims
from search import search_web
from verifier import verify_claim

st.set_page_config(page_title="AI Fact Checker", layout="wide")
st.title("📄 AI Fact-Checking Web App")
st.write("Upload a PDF to extract and verify factual claims.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")

    # Extract text from PDF
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    # Extract claims using LLM
    with st.spinner("Extracting factual claims..."):
        claims = extract_claims(extracted_text)

    st.subheader("📌 Extracted Factual Claims")

    if claims:
        results = []

        for i, claim in enumerate(claims, 1):
            st.markdown(f"**{i}. {claim}**")

            # Search web and verify claim
            with st.spinner(f"Verifying claim {i}..."):
                search_results = search_web(claim)
                status, explanation, evidence = verify_claim(claim, search_results)
                results.append({
                    "Claim": claim,
                    "Status": status,
                    "Explanation": explanation,
                    "Evidence": evidence
                })

            # Display status
            if status == "Verified":
                st.success(f"✅ Verified — {explanation}")
            elif status == "Inaccurate":
                st.warning(f"⚠️ Inaccurate — {explanation}")
            else:
                st.error(f"❌ False — {explanation}")

            # Collapsible evidence
            if evidence:
                with st.expander("View Evidence"):
                    for ev in evidence:
                        st.write(f"- {ev['snippet']}")
                        st.markdown(f"[Source Link]({ev['link']})")

            st.write("---")

        # Summary
        st.subheader("📊 Verification Summary")
        for res in results:
            st.markdown(f"- **{res['Claim']}** → **{res['Status']}**")

        # --------- Export CSV ---------
        st.subheader("💾 Export Results")
        csv_data = []
        for res in results:
            ev_texts = []
            ev_links = []
            for ev in res["Evidence"]:
                ev_texts.append(ev["snippet"])
                ev_links.append(ev["link"])
            csv_data.append({
                "Claim": res["Claim"],
                "Status": res["Status"],
                "Explanation": res["Explanation"],
                "Evidence Snippets": " || ".join(ev_texts),
                "Evidence Links": " || ".join(ev_links)
            })

        df = pd.DataFrame(csv_data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV of Results",
            data=csv,
            file_name="fact_check_results.csv",
            mime="text/csv"
        )

    else:
        st.warning("No factual claims found.")
