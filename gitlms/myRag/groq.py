from groq import Groq

# Initialize Groq client globally
groq_client = Groq(api_key="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")  # Replace with your actual API key

async def answer_with_groq_using_qdrant_context(query: str, collection_name: str = "lecture_materials", top_k: int = 5) -> str:
    """
    Searches Qdrant with the given query, builds context, and uses Groq LLM to generate an answer.
    
    Args:
        query (str): The user's question.
        collection_name (str): Name of the Qdrant collection to search.
        top_k (int): Number of top search results to retrieve.

    Returns:
        str: LLM-generated answer.
    """
    try:
        # Step 1: Qdrant search
        results = search_qdrant(collection_name=collection_name, query=query, top_k=top_k)
        context = "\n\n".join(result["payload"].get("text", "") for result in results)

        # Step 2: Compose prompt
        prompt = f"""You are an AI assistant. Use the following lecture content to answer the question.

Context:
{context}

Question:
{query}

Answer:"""

        # Step 3: Groq completion
        groq_response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return groq_response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating answer: {str(e)}"
