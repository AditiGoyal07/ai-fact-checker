# AI Fact-Checking Web App

## Overview
A Streamlit-based web application that extracts factual claims from PDFs and verifies them using live web evidence and large language models (LLMs). The app demonstrates how AI and web search can be combined to check claims in real-time.

## Features
- Upload PDFs and extract text
- Extract verifiable factual claims using LLM
- Verify claims using live web search via SerpAPI
- Provide status labels: Verified, Inaccurate, False, Partially Accurate
- Show evidence snippets with source links
- Export results to CSV

## Tech Stack
- Python
- Streamlit
- LangChain
- OpenAI GPT models
- SerpAPI

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/AditiGoyal07/ai-fact-checker.git
  cd ai-fact-checker
  ```
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Set environment variables in a .env file:
  ```bash
  OPENAI_API_KEY=your_openai_api_key
  SERPAPI_API_KEY=your_serpapi_api_key
  ```

## Running the App
Run the Streamlit application:
```bash
streamlit run app.py
```
1. Upload a PDF to extract and verify factual claims.
2. View results, claim status, and evidence.
3. Export verification results to CSV.

## Limitations
1. May not always reflect the current date or time; future events could be misclassified.
2. Web sources can be outdated, affecting verification accuracy.
3. AI interpretation may misjudge nuanced or context-dependent claims.

## CSV Export
The app allows exporting all claims with:
1. Claim text
2. Verification status
3. Explanation
4. Evidence snippets
5. Source links
