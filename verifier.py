from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json
import streamlit as st

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@st.cache_data(show_spinner=False)
def verify_claim(claim, search_results):
    """
    Verify a claim using search results.
    Returns: status, explanation, evidence list (with snippet + link)
    Robustly handles JSON parsing and unverifiable claims.
    """
    # Combine snippets for context
    context = "\n".join([res["snippet"] for res in search_results])

    # Prompt forcing strict JSON output
    prompt = PromptTemplate(
        input_variables=["claim", "context"],
        template="""
You are a fact-checking assistant.

Claim:
{claim}

Evidence from live web:
{context}

Task:
1. Decide if the claim is:
   - Verified
   - Inaccurate
   - False
2. Provide a short explanation.
3. Pick 2-3 relevant sentences from the evidence (if any).

IMPORTANT: ALWAYS respond in valid JSON, even if no evidence is available.  
Example for unverifiable claims: 
{{"status": "False", "explanation": "Cannot verify claim; future prediction or no evidence", "evidence_indices": []}}

Respond ONLY in JSON format.
"""
    )

    formatted_prompt = prompt.format(claim=claim, context=context)
    response = llm.invoke(formatted_prompt)
    output = response.content.strip()

    # Try parsing JSON
    try:
        result = json.loads(output)
        indices = result.get("evidence_indices", [])
        evidence = [
            {"snippet": search_results[i]["snippet"], "link": search_results[i]["link"]}
            for i in indices if i < len(search_results)
        ]
        status = result.get("status", "False")
        explanation = result.get("explanation", "")
        return status, explanation, evidence

    except json.JSONDecodeError:
        # Fallback: treat whole output as explanation
        fallback_explanation = output if output else "Could not verify claim; no valid JSON returned."
        return "False", fallback_explanation, []
