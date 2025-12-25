import os
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve_context

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an AI Travel Agent.

Instructions:
- Use retrieved context if available.
- If context is weak, give general but safe travel advice.
- Do not hallucinate facts.
- Answer clearly in bullet points.
"""

def decide_tool(query):
    keywords = ["eco", "budget", "solo", "luxury", "adventure"]

    for k in keywords:
        if k in query.lower():
            return "retrieve", f"Keyword '{k}' detected → using knowledge base"

    return "fallback", "No domain keyword detected → using general reasoning"


def generate_answer(query):
    tool, reason = decide_tool(query)
    print(f"[Agent Decision] {reason}")

    if tool == "retrieve":
        context = retrieve_context(query)
        if len(context.strip()) < 150:
            context = "General travel best practices and safety guidelines."
            sources = "Source:\n• General travel best practices"
        else:
            sources = "Sources:\n• Wikipedia\n• Wikivoyage"
    else:
        context = "General travel best practices and safety guidelines."
        sources = "Source:\n• General travel best practices"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{query}

At the end of the answer, include the following source information exactly as provided:
{sources}
"""
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

# CLI LOOP
if __name__ == "__main__":
    while True:
        q = input("\nAsk a travel question (or 'exit'): ")
        if q.lower() == "exit":
            break
        print("\nAnswer:\n", generate_answer(q))
