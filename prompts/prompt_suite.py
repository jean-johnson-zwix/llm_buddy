PROMPT_SUITE = [
    # ─────────────────────────────────────────
    # CATEGORY 1: CODING (8 prompts)
    # ─────────────────────────────────────────
    {
        "id": "code_001",
        "category": "coding",
        "difficulty": "easy",
        "prompt": "Write a Python function that takes a list of integers and returns the two numbers that add up to a target sum.",
        "evaluation_criteria": "Correctness, edge case handling, code clarity"
    },
    {
        "id": "code_002",
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Debug this Python code and explain what was wrong:\n\ndef calculate_average(nums):\n    total = 0\n    for n in nums:\n        total =+ n\n    return total / len(nums)",
        "evaluation_criteria": "Correctly identifies =+ bug, explains fix clearly"
    },
    {
        "id": "code_003",
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python class for a thread-safe counter that can be safely incremented by multiple threads simultaneously.",
        "evaluation_criteria": "Uses threading.Lock correctly, proper class structure"
    },
    {
        "id": "code_004",
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Given a binary tree, write a Python function to find the lowest common ancestor of two given nodes.",
        "evaluation_criteria": "Correct recursive logic, handles edge cases"
    },
    {
        "id": "code_005",
        "category": "coding",
        "difficulty": "easy",
        "prompt": "Write a Python decorator that measures and prints the execution time of any function.",
        "evaluation_criteria": "Correct use of functools.wraps, time measurement accuracy"
    },
    {
        "id": "code_006",
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Explain the difference between a shallow copy and deep copy in Python with code examples showing where each would produce different results.",
        "evaluation_criteria": "Clear explanation, correct examples, demonstrates understanding"
    },
    {
        "id": "code_007",
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Implement a rate limiter in Python that allows a maximum of N requests per minute using a sliding window algorithm.",
        "evaluation_criteria": "Sliding window logic correct, handles edge cases, clean code"
    },
    {
        "id": "code_008",
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python context manager that automatically retries a block of code up to 3 times if an exception is raised, with exponential backoff.",
        "evaluation_criteria": "Correct context manager protocol, exponential backoff logic"
    },

    # ─────────────────────────────────────────
    # CATEGORY 2: REASONING (8 prompts)
    # ─────────────────────────────────────────
    {
        "id": "reason_001",
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "A bat and ball together cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost? Show your reasoning step by step.",
        "evaluation_criteria": "Correct answer ($0.05), clear step-by-step reasoning"
    },
    {
        "id": "reason_002",
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "You have 3 boxes: one contains only apples, one contains only oranges, one contains both. All 3 boxes are mislabeled. You can pick one fruit from one box. How do you correctly label all boxes? Explain your reasoning.",
        "evaluation_criteria": "Correct strategy: pick from mixed box, logical chain of deductions"
    },
    {
        "id": "reason_003",
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "A company has 3 departments. Dept A has 10 people with avg salary $80K. Dept B has 20 people with avg salary $90K. Dept C has 30 people with avg salary $70K. What is the overall average salary? Show your work.",
        "evaluation_criteria": "Weighted average calculation correct: (800K+1800K+2100K)/60"
    },
    {
        "id": "reason_004",
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? What type of logical reasoning is this?",
        "evaluation_criteria": "Correct answer (yes), identifies syllogistic/deductive reasoning"
    },
    {
        "id": "reason_005",
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "You are designing a distributed system where nodes can fail. Explain the CAP theorem and give a concrete example of a real system that chooses CP and one that chooses AP, and why.",
        "evaluation_criteria": "Correct CAP explanation, valid real-world examples with justification"
    },
    {
        "id": "reason_006",
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "A model achieves 99% accuracy on a dataset where 99% of samples are class A. Is this a good model? Why or why not? What metric would you use instead?",
        "evaluation_criteria": "Identifies class imbalance problem, suggests precision/recall/F1"
    },
    {
        "id": "reason_007",
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "You have a sorted array of 1 million integers. Compare the time and space complexity of linear search vs binary search vs building a hash map for repeated lookups. Which would you choose and why?",
        "evaluation_criteria": "Correct complexity analysis, justified recommendation based on use case"
    },
    {
        "id": "reason_008",
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "Your ML model performs well on training data but poorly on test data. Walk through the 5 most likely causes and how you would diagnose each.",
        "evaluation_criteria": "Identifies overfitting, data leakage, distribution shift, etc. with diagnosis steps"
    },

    # ─────────────────────────────────────────
    # CATEGORY 3: SUMMARIZATION (7 prompts)
    # ─────────────────────────────────────────
    {
        "id": "summ_001",
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize the following in 3 bullet points:\n\nTransformer models use a self-attention mechanism that allows them to weigh the importance of different words in a sequence when encoding each word. Unlike RNNs, transformers process all tokens in parallel rather than sequentially, making them significantly faster to train on modern GPU hardware. The attention mechanism computes queries, keys, and values from the input, using the dot product of queries and keys to determine how much attention each token should pay to every other token.",
        "evaluation_criteria": "Captures: self-attention, parallel processing, Q/K/V mechanism"
    },
    {
        "id": "summ_002",
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Explain the following technical concept to a non-technical product manager in 2-3 sentences:\n\nRAG (Retrieval Augmented Generation) combines a vector database with an LLM. At query time, relevant documents are retrieved via semantic similarity search and injected into the LLM prompt as context, allowing the model to answer questions grounded in specific knowledge bases rather than relying solely on its training data.",
        "evaluation_criteria": "Simple language, correct core idea, no jargon, actionable understanding"
    },
    {
        "id": "summ_003",
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "You are a technical lead. Summarize the following incident for an executive in 4 sentences max:\n\nAt 2:14 AM, our payment service began returning 500 errors due to a Redis cache eviction policy misconfiguration that caused cache stampede under high load. The on-call engineer identified the root cause at 3:02 AM. Redis maxmemory-policy was updated from allkeys-lru to volatile-lru and the service recovered at 3:47 AM. Total downtime: 93 minutes. 12,000 payment requests failed.",
        "evaluation_criteria": "Impact first, root cause, resolution, timeline — no unnecessary technical detail"
    },
    {
        "id": "summ_004",
        "category": "summarization",
        "difficulty": "hard",
        "prompt": "Compare and contrast supervised learning, unsupervised learning, and reinforcement learning in a concise paragraph suitable for a technical blog post introduction.",
        "evaluation_criteria": "Accurate distinctions, concrete examples, engaging writing, appropriate length"
    },
    {
        "id": "summ_005",
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "In one sentence each, explain: precision, recall, and F1 score.",
        "evaluation_criteria": "All three correct, concise, no unnecessary elaboration"
    },
    {
        "id": "summ_006",
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the key tradeoffs between SQL and NoSQL databases for a developer who needs to choose one for a new project with unpredictable schema requirements and high write throughput.",
        "evaluation_criteria": "Covers schema flexibility, ACID vs eventual consistency, write performance, gives clear recommendation"
    },
    {
        "id": "summ_007",
        "category": "summarization",
        "difficulty": "hard",
        "prompt": "A junior engineer asks you to explain why their fine-tuned LLM is performing worse than the base model. Write a concise technical explanation covering the 3 most likely causes.",
        "evaluation_criteria": "Covers catastrophic forgetting, insufficient/noisy data, learning rate issues"
    },

    # ─────────────────────────────────────────
    # CATEGORY 4: RAG / RETRIEVAL (7 prompts)
    # ─────────────────────────────────────────
    {
        "id": "rag_001",
        "category": "rag",
        "difficulty": "easy",
        "prompt": "Based only on the following context, answer the question. Do not use outside knowledge.\n\nContext: The LLM Benchmarker evaluates three models: Gemini 2.0 Flash, LLaMA 4 Scout, and LLaMA 3.1 8B. It scores each model on four task categories: coding, reasoning, summarization, and RAG. Scoring is done using an LLM-as-judge approach where Gemini evaluates each response on a scale of 1 to 10.\n\nQuestion: How many models does the LLM Benchmarker evaluate and what scoring method does it use?",
        "evaluation_criteria": "Answers from context only: 3 models, LLM-as-judge, Gemini scores 1-10"
    },
    {
        "id": "rag_002",
        "category": "rag",
        "difficulty": "medium",
        "prompt": "Based only on the following context, answer the question.\n\nContext: MLflow is an open-source platform for managing the ML lifecycle. It provides four main components: Tracking (logs parameters, metrics, and artifacts), Projects (packages code for reproducibility), Models (manages model formats), and Registry (manages model versioning and deployment stages).\n\nQuestion: What are the four components of MLflow and what does the Tracking component do?",
        "evaluation_criteria": "Lists all 4 components correctly, accurately describes Tracking"
    },
    {
        "id": "rag_003",
        "category": "rag",
        "difficulty": "hard",
        "prompt": "Based only on the following context, answer the question. If the answer is not in the context, say 'I cannot answer this from the provided context.'\n\nContext: Vector databases store embeddings — dense numerical representations of text. Similarity search is performed using cosine similarity or dot product. ChromaDB is an open-source vector database optimized for LLM applications. Pinecone is a managed vector database service.\n\nQuestion: What is the pricing model for Pinecone?",
        "evaluation_criteria": "Correctly states the answer is not in the context — tests hallucination resistance"
    },
    {
        "id": "rag_004",
        "category": "rag",
        "difficulty": "medium",
        "prompt": "Based only on the following context, answer the question.\n\nContext: Attention Is All You Need (Vaswani et al., 2017) introduced the Transformer architecture. The paper proposed replacing recurrent layers entirely with multi-head self-attention. The model achieved 28.4 BLEU on WMT 2014 English-to-German translation, outperforming the best previous results including ensembles. Training took 3.5 days on 8 P100 GPUs.\n\nQuestion: What task was used to evaluate the Transformer and what score did it achieve?",
        "evaluation_criteria": "WMT 2014 English-to-German, 28.4 BLEU — exact from context, no elaboration"
    },
    {
        "id": "rag_005",
        "category": "rag",
        "difficulty": "hard",
        "prompt": "Based only on the following context, identify any contradictions.\n\nContext: System A processes requests in under 50ms on average. Load testing showed System A handled 10,000 concurrent users with no degradation. However, the post-mortem report states System A experienced 8 second response times when concurrent users exceeded 5,000.\n\nQuestion: Is there a contradiction in this context? If so, identify it precisely.",
        "evaluation_criteria": "Correctly identifies contradiction between 10K users claim and 8s latency at 5K users"
    },
    {
        "id": "rag_006",
        "category": "rag",
        "difficulty": "medium",
        "prompt": "Based only on the following context, answer the question.\n\nContext: The company's data retention policy states: customer PII must be deleted within 90 days of account closure. Logs containing request metadata (non-PII) may be retained for up to 2 years. Aggregated analytics data with no individual identifiers may be retained indefinitely.\n\nQuestion: Can the company retain a log file containing only request timestamps and endpoint names (no user identifiers) for 3 years?",
        "evaluation_criteria": "Yes — correctly identifies this as non-PII metadata, applies 2-year rule correctly, notes 3 years exceeds it"
    },
    {
        "id": "rag_007",
        "category": "rag",
        "difficulty": "easy",
        "prompt": "Based only on the following context, answer the question.\n\nContext: GCP Cloud Run is a fully managed serverless platform that automatically scales containers from zero to N instances based on incoming requests. It charges only for the compute used during request processing. Cold starts occur when a new instance is initialized after a period of inactivity.\n\nQuestion: What is a cold start in the context of Cloud Run?",
        "evaluation_criteria": "Correctly defines cold start from context: new instance initialized after inactivity"
    }
]
# 10 prompts for development
DEV_SUITE = [
    # Coding
    next(p for p in PROMPT_SUITE if p["id"] == "code_001"),
    next(p for p in PROMPT_SUITE if p["id"] == "code_007"),
    # Reasoning
    next(p for p in PROMPT_SUITE if p["id"] == "reason_001"),
    next(p for p in PROMPT_SUITE if p["id"] == "reason_005"),
    # Summarization
    next(p for p in PROMPT_SUITE if p["id"] == "summ_001"),
    next(p for p in PROMPT_SUITE if p["id"] == "summ_007"),
    # RAG
    next(p for p in PROMPT_SUITE if p["id"] == "rag_001"),
    next(p for p in PROMPT_SUITE if p["id"] == "rag_003"),  # hallucination test
    next(p for p in PROMPT_SUITE if p["id"] == "rag_005"),  # contradiction test
    next(p for p in PROMPT_SUITE if p["id"] == "rag_007"),
]