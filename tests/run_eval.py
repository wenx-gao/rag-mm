# tests/run_eval.py
from ragas.metrics import faithfulness, answer_relevance, context_precision
from ragas import evaluate
from datasets import Dataset

# 1. Your "Golden Dataset"
data_samples = {
    'question': ['What is the revenue in Q3?'],
    'answer': ['The revenue was $15M.'],
    'contexts' : [['The company reported Q3 revenue of $15M in the annual report.']],
    'ground_truth': ['The revenue was $15M.']
}

dataset = Dataset.from_dict(data_samples)

# 2. Run Eval (Requires local LLM to act as "Judge")
score = evaluate(dataset, metrics=[faithfulness, answer_relevance, context_precision])
print(score)
