from query_data import query_rag
from langchain_ollama import OllamaLLM

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = OllamaLLM(model="llama3.2:3b")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print("\n----------------------------")
    print(f"Question: {question}")
    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        print("\033[92mResponse: TRUE ✅\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        print("\033[91mResponse: FALSE ❌\033[0m")
        return False
    else:
        print("\033[93mResponse: UNKNOWN ⚠️\033[0m")
        return None


# --- Define all your tests here ---
TEST_CASES = [
    {
        "name": "Attention Function",
        "question": "What is an attention function?",
        "expected": "An attention function is mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.",
    },
    {
        "name": "BSSIM Core Knowledge",
        "question": "Tell me about BSSIM Core Knowledge, from an executive perspective.",
        "expected": "From an executive perspective, you can view BSIMM activities as controls implemented in a software security risk management framework. The implemented activities might function as preventive, detective, corrective, or compensating controls in your SSI. Positioning the activities as controls allows for easier understanding of the BSIMM value by governance, risk, compliance, legal, audit, and other risk management groups.",
    },
    {
        "name": "C-SCRM Activities",
        "question": "Who can perform C-SCRM activities?",
        "expected": "C-SCRM activities can be performed by a variety of individuals or groups within an enterprise, ranging from a single individual to committees, divisions, centralized program offices, or any other enterprise structure",
    },
]


if __name__ == "__main__":
    passed, failed, unknown = 0, 0, 0

    for test in TEST_CASES:
        try:
            result = query_and_validate(test["question"], test["expected"])
            if result is True:
                passed += 1
            elif result is False:
                failed += 1
            else:
                unknown += 1
        except Exception as e:
            print(f"\033[91mError in {test['name']}: {e}\033[0m")
            failed += 1

    print("\n============================")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️ Unknown: {unknown}")
    print("============================")
