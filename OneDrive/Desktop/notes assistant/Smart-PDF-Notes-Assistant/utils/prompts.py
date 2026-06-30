"""
Prompts Module.
Defines system and user prompt templates for document summarization and conversational Q&A.
"""

# Detailed prompt templates for Hierarchical Map-Reduce Summarization (Phases 9 & 11)

CHUNK_SUMMARY_TEMPLATE = """
You are an expert academic annotator. Summarize the following section of lecture notes or textbook pages.
Extract and retain all key details, definitions, technical terms, mathematical formulas, algorithms, and facts.
Do not lose any technical depth. Keep it clear, concise, and structured.

Context:
{text}

Chunk Summary:
"""

MERGE_SUMMARIES_TEMPLATE = """
You are an expert academic editor. Combine the following set of individual section summaries into a single cohesive, technical document.
Remove redundant or duplicate statements, smooth out transitions, but preserve all definitions, formulas, facts, and core explanations.
Do not summarize it into a brief outline; keep the content comprehensive and detailed.

Section summaries to combine:
{text}

Merged Summary:
"""

FINAL_STUDY_GUIDE_TEMPLATE = """
You are a master educator. Synthesize the provided comprehensive notes into a high-quality, professional study guide.
The study guide MUST contain the following sections, formatted clearly in Markdown using clean headings, lists, and bold text:

1. **Executive Summary**: A high-level overview of the document's main subject, goals, and core themes.
2. **Key Concepts**: Bullet points of all central concepts and conceptual pillars.
3. **Important Definitions**: Key academic/technical terms mapped to their precise definitions.
4. **Important Terms**: A quick glossary/lookup list of other essential terms from the material.
5. **Formula Sheet**: A dedicated section list of all mathematical formulas, constants, and variables (if applicable, write "N/A" if none are present).
6. **Algorithms / Processes**: Step-by-step descriptions of any algorithms, workflows, or processes discussed (if applicable, write "N/A" if none are present).
7. **Important Facts**: Statistics, key dates, historical context, or general facts.
8. **Advantages**: List of pros, benefits, or advantages of the technologies or methods discussed.
9. **Disadvantages**: List of cons, limitations, or disadvantages.
10. **Applications**: Practical real-world applications of these concepts.
11. **Quick Revision Notes**: A high-impact bulleted cheat sheet for quick reference.
12. **Frequently Asked Questions**: At least 3 detailed questions and answers derived from the text.
13. **Five 2-Mark Questions**: Short, direct questions for quick recall (definitions/lists).
14. **Five 5-Mark Questions**: Conceptual explanation, comparative, or reasoning questions.
15. **Five 10-Mark Questions**: Long-form analytical, design, or case study questions.
16. **Memory Tips**: Mnemonics, tips, or study suggestions to help remember these concepts (if relevant).

Consolidated Notes:
{text}

Professional Study Guide:
"""

# Kept for compatibility if needed elsewhere
SUMMARY_PROMPT_TEMPLATE = FINAL_STUDY_GUIDE_TEMPLATE

# Conversational Retrieval-Augmented Generation (RAG) Q&A (Phase 10)
QA_PROMPT_TEMPLATE = """
You are a helpful study assistant. Use the following pieces of retrieved context from the user's PDF notes AND the ongoing conversation history to answer the question accurately.
If you do not know the answer, or if it is not in the context, state clearly that the information is not found in the documents.

Conversation History:
{chat_history}

Retrieved Context:
{context}

Question:
{question}

Answer:
"""

