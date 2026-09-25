## RAG Pipeline Architecture

The Zepto customer support application follows a Retrieval-Augmented Generation (RAG) pipeline consisting of four main stages: **ingestion, embedding, retrieval, and generation**.

### 1. Ingestion

The Zepto policy documents are stored as text files (`doc1.txt` to `doc8.txt`) in the `docs` folder. The ingestion code reads these files and stores their text along with metadata such as document ID, title, category, and source.

The documents are stored in the ChromaDB collection named `zepto_policies`. In this implementation, each policy document is stored as a document/chunk rather than being split into multiple smaller chunks.

### 2. Embedding

The `SentenceTransformer` model:

```text
all-MiniLM-L6-v2
```

is used to convert the policy documents into numerical embedding vectors.

The same embedding model is used when a user submits a question. The user's question is converted into an embedding and compared with the stored embeddings in ChromaDB.

ChromaDB stores the embeddings and document data in:

```text
./chroma_db
```

using the collection:

```text
zepto_policies
```

### 3. Retrieval

The LangGraph workflow first uses the `classify_intent` node to determine whether the question is related to a Zepto policy.

Policy-related questions are routed to the:

```text
retrieve_and_answer
```

node.

This node:

1. Embeds the user's question using `all-MiniLM-L6-v2`.
2. Queries the `zepto_policies` ChromaDB collection.
3. Retrieves the top 3 most similar documents.
4. Combines the retrieved documents into the context.
5. Uses the retrieved document IDs as the `sources`.

The retrieved context is then passed to the answer-generation step.

### 4. Generation

In the graded baseline, `MOCK_LLM` uses its default value:

```python
MOCK_LLM = os.getenv("MOCK_LLM", "1")
```

The mock generation path produces a deterministic answer using the retrieved context:

```text
Based on the retrieved context: <top retrieved document excerpt>
```

The `FinalAnswer` Pydantic model validates the final response and contains:

```text
answer
sources
confidence
```

For a general question that is not related to Zepto policies, the `classify_intent` node routes the request to the `direct_answer` node instead of performing retrieval. This node returns:

```text
I can only answer questions about Zepto policies right now.
```

with an empty `sources` list.

### Data Flow

```text
Zepto Policy Documents
        │
        ▼
   Ingestion
 doc1.txt ... doc8.txt
        │
        ▼
 SentenceTransformer
 all-MiniLM-L6-v2
        │
        ▼
     ChromaDB
  zepto_policies
        │
        │
 User Question
        │
        ▼
 classify_intent
        │
   ┌────┴─────┐
   │          │
Policy      General
Question    Question
   │          │
   ▼          ▼
retrieve_   direct_answer
and_answer      │
   │            │
   ▼            │
Top-3 Docs      │
   │            │
   └──────┬─────┘
          ▼
     FinalAnswer
          │
          ▼
       FastAPI
       POST /ask
```

### MOCK_LLM Toggle

The application is designed around the `MOCK_LLM` environment variable. The default graded configuration is:

```text
MOCK_LLM=1
```

In the default mock mode, no external LLM API is required. The retrieval pipeline still performs embedding and ChromaDB retrieval, while the final answer is generated deterministically from the retrieved context.

The optional real-LLM extension can use:

```text
MOCK_LLM=0
```

to replace the mock generation behavior with an actual LLM-based generation step. The retrieval and ChromaDB stages remain the same; the main change is how the final answer is generated and validated.

For the required submission, the application is run with the default `MOCK_LLM=1` configuration.