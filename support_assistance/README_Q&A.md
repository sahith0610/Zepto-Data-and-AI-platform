## FastAPI Example Calls

The following questions were sent to the FastAPI `POST /ask` endpoint using the default `MOCK_LLM=1` configuration.

### Example 1 — Delivery Policy

**Request:**

```json
{
  "query": "What is the delivery fee for orders below INR 149?"
}
```

**Raw JSON Response:**

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard delivery is free on orders over INR 149; orders below this threshold incur a flat INR 25 delivery fee. Priority delivery, which reserves the next available rider slot, is available at checkout for an additional INR 15. Zepto does not currently deliver to addresses outside its listed serviceable pin codes.",
  "sources": [
    "doc1",
    "doc5",
    "doc3"
  ],
  "confidence": 1.0
}
```

### Example 2 — Return Policy

**Request:**

```json
{
  "query": "How long do I have to return an item??"
}
```

**Raw JSON Response:**

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within 7 days of delivery in unopened, resalable condition. Approved refunds are credited to the original payment method within 3–5 business days, or instantly to the Zepto wallet if the customer opts for wallet credit. Personal care items that have been opened are non-returnable except in the case of a manufacturing defect. Return pickup, where required, is arranged free of cost by Zepto.",
  "sources": [
    "doc2",
    "doc6",
    "doc5"
  ],
  "confidence": 1.0
}
```

### Example 3 — Negative / General Question

**Request:**

```json
{
  "query": "What is the capital of India?"
}
```

**Raw JSON Response:**

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

The first two questions are classified as Zepto policy questions and trigger retrieval from ChromaDB. The third question is unrelated to Zepto policies, so retrieval is not performed and the `direct_answer` node is used.