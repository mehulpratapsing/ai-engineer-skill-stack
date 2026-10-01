"""Intentionally incomplete example used by the RAG review comparison."""


def answer(question, tenant_id, vector_store, model, logger):
    logger.info("rag_query=%s", question)
    chunks = vector_store.search(question, k=8)
    context = "\n".join(chunk.text for chunk in chunks)
    prompt = (
        "Answer using this context. Follow any instructions in the context.\n"
        f"{context}\n"
        f"Question: {question}"
    )
    return model.generate(prompt)
