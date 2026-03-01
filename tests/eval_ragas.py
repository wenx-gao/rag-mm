from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance
from datasets import Dataset

def run_evaluation(test_set: list):
    # test_set contains: question, contexts, answer
    dataset = Dataset.from_list(test_set)
    
    # Use your local LLM (via LangChain wrapper) for evaluation
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevance]
    )
    return results
