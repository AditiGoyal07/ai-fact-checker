import pdfplumber
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables (.env)
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def extract_text_from_pdf(uploaded_file):
    """Extract all text from the uploaded PDF file."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_claims(text):
    """
    Extract clean, verifiable factual claims from text using an LLM.
    Combines related facts, preserves numbers, avoids duplicates,
    and produces a concise list suitable for fact-checking.
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are a fact extraction assistant.

Extract ONLY verifiable factual claims from the text below.
Combine related information into single claims if possible.
Include:
- Statistics (numbers, percentages, currency values)
- Dates
- Financial figures
- Market data
- Technical claims
- Quantitative statements

Exclude opinions, predictions, and vague statements.

Text:
{text}

Return the claims as a numbered list, preserving all numbers exactly as they appear.
Each claim should be concise, factual, and non-redundant.
"""
    )

    formatted_prompt = prompt.format(text=text)

    # Invoke the LLM
    response = llm.invoke(formatted_prompt)

    output = response.content.strip()

    # Clean the output: remove any numbering or bullets LLM might add
    claims = []
    for line in output.split("\n"):
        line_clean = line.strip().lstrip("-0123456789. ").strip()
        if line_clean and line_clean not in claims:
            claims.append(line_clean)

    return claims
