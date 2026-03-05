# # tests/eval_ragas.py

# import asyncio
# from ragas import evaluate
# from datasets import Dataset
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import OllamaEmbeddings

# # NEW: Notice these are Classes (Capitalized)
# from ragas.metrics import (
#     Faithfulness,
#     AnswerRelevancy,
#     ContextPrecision,
#     ContextRecall,
# )

# # 1. Setup the "Judge" (Your local Llama 3)
# langchain_llm = ChatOllama(model="llama3:8b", base_url="http://ollama:11434")
# langchain_embeddings = OllamaEmbeddings(model="llama3:8b", base_url="http://ollama:11434")

# async def run_feeder_eval(question, answer, contexts, ground_truth):
#     # 2. Prepare the data in Ragas format
#     data_sample = {
#         "question": [question],
#         "answer": [answer],
#         "contexts": [contexts],
#         "ground_truth": [ground_truth]
#     }
    
#     dataset = Dataset.from_dict(data_sample)
    
#     # 3. Initialize the metric objects
#     metrics = [
#         Faithfulness(),
#         AnswerRelevancy(),
#         ContextPrecision(),
#         ContextRecall(),
#     ]

#     print("\n--- Starting Ragas Evaluation (using local Llama 3) ---")
    
#     # 4. Run evaluation
#     result = evaluate(
#         dataset=dataset,
#         metrics=metrics,
#         llm=langchain_llm,
#         embeddings=langchain_embeddings,
#     )
    
#     return result

# if __name__ == "__main__":
#     test_question = "What are the technical capacities of the feeder?"
    
#     test_answer = """According to the context, the feeder (Vibrating/Apron) has the following technical requirements:
#     * Crushed material: Lime stone
#     * Capacity: 1500 ~ 1800 tph
#     * Feed size: 1080 mm
#     * Montage angle: 3~8°
#     * Aperture:100mm
#     * Motor: 68 kW
#     * Capable of loaded starting."""

#     test_contexts = [
#         "Feeder (Vibrating/Apron specify) Crushed material: Lime stone; Capacity: 1500 ~ 1800 tph; Feed size: 1080 mm; Montage angle: 3~8 ; Aperture: 100 mm ; Motor: 68 kW; Capable of loaded starting."
#     ]
    
#     test_ground_truth = "Capacity: 1500-1800 tph, Feed size: 1080mm, Motor: 68kW, Material: Limestone, Angle: 3-8 degrees."

#     result = asyncio.run(run_feeder_eval(test_question, test_answer, test_contexts, test_ground_truth))
    
#     print("\n--- RAGAS SCORES ---")
#     print(result)

# tests/eval_ragas.py
import asyncio
from ragas import evaluate
from datasets import Dataset
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.run_config import RunConfig # Import RunConfig

# 1. Setup the "Judge"
# We keep the 300s timeout for the individual LLM calls
langchain_llm = ChatOllama(
    model="llama3:8b", 
    base_url="http://ollama:11434",
    timeout=300 
)
langchain_embeddings = OllamaEmbeddings(
    model="llama3:8b", 
    base_url="http://ollama:11434"
)

async def run_feeder_eval(question, answer, contexts, ground_truth):
    data_sample = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": [ground_truth]
    }
    dataset = Dataset.from_dict(data_sample)
    
    metrics = [
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall(),
    ]

    # 2. Setup the RunConfig
    # max_workers=1 is the "secret" for CPU users. 
    # It prevents the LLM from trying to do 4 things at once.
    run_config = RunConfig(max_workers=1, timeout=300)

    print("\n--- Starting Ragas Evaluation (Sequential Mode) ---")
    
    # 3. Run evaluation
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=langchain_llm,
        embeddings=langchain_embeddings,
        run_config=run_config # Use run_config instead of is_async
    )
    
    return result

if __name__ == "__main__":
    test_question = "What are the technical capacities of the feeder?"
    test_answer = """According to the context, the feeder (Vibrating/Apron) has the following technical requirements:
    * Crushed material: Lime stone
    * Capacity: 1500 ~ 1800 tph
    * Feed size: 1080 mm
    * Montage angle: 3~8°
    * Aperture: 100mm
    * Motor: 68 kW
    * Capable of loaded starting."""

    test_contexts = [
        "Feeder (Vibrating/Apron specify) Crushed material: Lime stone; Capacity: 1500 ~ 1800 tph; Feed size: 1080 mm; Montage angle: 3~8 ; Aperture: 100 mm ; Motor: 68 kW; Capable of loaded starting."
    ]
    
    test_ground_truth = "Capacity: 1500-1800 tph, Feed size: 1080mm, Motor: 68kW, Material: Limestone, Angle: 3-8 degrees."

    result = asyncio.run(run_feeder_eval(test_question, test_answer, test_contexts, test_ground_truth))
    print("\n--- RAGAS SCORES ---")
    print(result)
