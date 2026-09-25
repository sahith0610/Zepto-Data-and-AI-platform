
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
docs_folder = Path(r"C:\Python\support_asistant\docs")

# Metadata
metadata_info = {
    "doc1": {"title": "Delivery Policy", "category": "delivery"},
    "doc2": {"title": "Returns & Refunds", "category": "returns"},
    "doc3": {"title": "Membership Tiers", "category": "membership"},
    "doc4": {"title": "Order Tracking", "category": "tracking"},
    "doc5": {"title": "Order Cancellation Policy", "category": "cancellation"},
    "doc6": {"title": "Damaged or Missing Items", "category": "damaged_items"},
    "doc7": {"title": "Gift Cards", "category": "gift_cards"},
    "doc8": {"title": "Customer Support Hours", "category": "support"}
}

documents = []
metadatas = []
ids = []
for file_path in sorted(docs_folder.glob("doc*.txt")):
    doc_id = file_path.stem
    text = file_path.read_text(encoding="utf-8")

    documents.append(text)
    ids.append(doc_id)

    metadatas.append({
        "source": file_path.name,
        "document_id": doc_id,
        "title": metadata_info[doc_id]["title"],
        "category": metadata_info[doc_id]["category"]
    })

print("Number of documents:", len(documents))
embeddings = model.encode(documents).tolist()

print("Embedding dimension:", len(embeddings[0]))
client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("zepto_policies")
except:
    pass

collection = client.create_collection("zepto_policies")

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Documents stored successfully!")
print("Number of records:", collection.count())

result = collection.get(include=["metadatas"])

for i in range(len(result["ids"])):
    print(result["ids"][i], "→", result["metadatas"][i])

result = collection.get(
    include=["documents", "metadatas"]
)

print("Number of records:", len(result["ids"]))

for i in range(len(result["ids"])):
    print("\n-----------------------------")
    print("ID:", result["ids"][i])
    print("Metadata:", result["metadatas"][i])
    print("Document:", result["documents"][i][:100], "...")


prompt_template = """
ROLE:
You are a Zepto customer support assistant. Answer customer questions
accurately using only the information provided in the context.

CONTEXT:
{context}

TASK:
Answer the user's question using the provided context.

Do not answer using information that is not present in the provided context.
If the answer cannot be found in the context, say:
"I don't have enough information in the provided context to answer this question."

FEW-SHOT EXAMPLE:

Example 1:
Question: How much is the delivery fee for orders below INR 149?

Context:
Standard delivery is free on orders over INR 149. Orders below this
threshold incur a flat INR 25 delivery fee.

Answer:
Orders below INR 149 have a flat INR 25 delivery fee.

Example 2:
Question: Can I return an opened personal care item?

Context:
Personal care items that have been opened are non-returnable except
in the case of a manufacturing defect.

Answer:
Opened personal care items cannot normally be returned, except when
there is a manufacturing defect.

USER QUESTION:
{question}

FORMAT:
Give a clear and direct answer in 1-3 sentences.
Do not include information that is not supported by the context.

LENGTH:
Keep the answer concise and no longer than 3 sentences.
"""

import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

MOCK_LLM = os.getenv("MOCK_LLM", "1")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("zepto_policies")

class FinalAnswer(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)

class State(TypedDict):
    query: str
    intent: str
    context: str
    sources: list[str]
    answer: str
    confidence: float

def classify_intent(state: State):

    query = state["query"].lower()

    keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    if any(keyword in query for keyword in keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        "intent": intent
    }

def retrieve_and_answer(state: State):

    query = state["query"]
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    retrieved_ids = results["ids"][0]
    context = "\n\n".join(retrieved_docs)
    top_chunk_snippet = retrieved_docs[0]

    answer_text = (
        f"Based on the retrieved context: "
        f"{top_chunk_snippet}"
    )

    final_answer = FinalAnswer(
        answer=answer_text,
        sources=retrieved_ids,
        confidence=1.0
    )

    return {
        "context": context,
        "sources": final_answer.sources,
        "answer": final_answer.answer,
        "confidence": final_answer.confidence
    }


def direct_answer(state: State):

    final_answer = FinalAnswer(
        answer="I can only answer questions about Zepto policies right now.",
        sources=[],
        confidence=1.0
    )

    return {
        "answer": final_answer.answer,
        "sources": final_answer.sources,
        "confidence": final_answer.confidence
    }

def route_intent(state: State):

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"

graph = StateGraph(State)

graph.add_node("classify_intent", classify_intent)
graph.add_node("retrieve_and_answer", retrieve_and_answer)
graph.add_node("direct_answer", direct_answer)

graph.set_entry_point("classify_intent")

graph.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph.add_edge("retrieve_and_answer", END)
graph.add_edge("direct_answer", END)

app = graph.compile()


query = "What is the delivery fee for orders below INR 149?"

result = app.invoke({
    "query": query,
    "intent": "",
    "context": "",
    "sources": [],
    "answer": "",
    "confidence": 0.0
})


final_output = FinalAnswer(
    answer=result["answer"],
    sources=result["sources"],
    confidence=result["confidence"]
)

print(final_output.model_dump_json(indent=2))



from fastapi import FastAPI

class AskRequest(BaseModel):
    query: str

fastapi_app = FastAPI()

@fastapi_app.post("/ask", response_model=FinalAnswer)
def ask(request: AskRequest):

    result = app.invoke({
        "query": request.query,
        "intent": "",
        "context": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    })

    return FinalAnswer(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

