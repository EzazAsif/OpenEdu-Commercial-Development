# answer_with_groq.py
from groq import Groq
from .qdrant_helper import search_qdrant

# Initialize Groq client
groq_client = Groq(api_key="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")  # Replace with env var in prod

async def answer_with_groq_using_qdrant_context(query: str, collection_name: str = "lecture_materials", top_k: int = 5) -> str:
    """
    Searches Qdrant with the given query, builds context, and uses Groq LLM to generate an answer.

    Args:
        query (str): The user's question.
        collection_name (str): Name of the Qdrant collection to search.
        top_k (int): Number of top search results to retrieve.

    Returns:
        str: LLM-generated answer with sources.
    """
    try:
        # Step 1: Qdrant search
        results = search_qdrant(collection_name=collection_name, query=query, top_k=top_k)

        if not results:
            return "No relevant documents found to answer the question."

        # Step 2: Extract and format context
        context_chunks = []
        sources = []

        for idx, result in enumerate(results, start=1):
            payload = result.payload or {}

            # Try multiple possible keys if content is not standardized
            text = payload.get("content") or payload.get("text") or payload.get("chunk") or ""
            title = payload.get("title", f"Document {idx}") or f"Document {idx}"
            url = payload.get("url", None)

            if not text:
                continue  # Skip empty chunks

            context_chunks.append(text)
            source_display = f"{title} - <a href='{url}'>{url}</a> \n" if url else title
            sources.append(f"{idx}. {source_display}")

        if not context_chunks:
            return "Documents found, but none contain readable content."

        context = "\n\n".join(context_chunks)
        sources_str = "\n".join(sources)

        # Step 3: Compose prompt
        prompt = f"""You are an AI assistant. Use the following lecture content to answer the question.

Context:
{context}

Question:
{query}

Answer:"""

        # Step 4: Groq completion
        groq_response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = groq_response.choices[0].message.content.strip()

        # Combine answer and sources
        final_response = f"{answer}\n\nSources:\n{sources_str}"
        return final_response

    except Exception as e:
        return f"Error generating answer: {str(e)}"
