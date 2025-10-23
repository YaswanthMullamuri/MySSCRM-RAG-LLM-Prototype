# RUN:
# python3 test_rag.py --model llama3
# or
# python3 test_rag.py mistral
# or
# python3 test_rag.py

from query_data import query_rag
from langchain_ollama import OllamaLLM
import sys

# Allow passing model name from CLI
DEFAULT_MODEL = "llama3.2:3b"
if len(sys.argv) > 1 and sys.argv[1] in ("--model", "-m"):
    MODEL_NAME = sys.argv[2]
elif len(sys.argv) > 1:
    MODEL_NAME = sys.argv[1]
else:
    MODEL_NAME = DEFAULT_MODEL

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def query_and_validate(question: str, expected_response: str, model_name: str = "llama3.2:3b"):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = OllamaLLM(model=model_name)
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
    {
        "name": "Self Attestation Form",
        "question": "What does the self attestation form identify?",
        "expected": "This self-attestation form identifies the minimum secure software development requirements a software producer must meet, and attest to meeting, before their software subject to the requirements of M-22-18 may be used by Federal agencies. This form is used by software producers to attest that the software they produce was developed in conformity with specified secure software development practices.",
    },
    {
        "name": "Self Attestation Memorandum",
        "question": "Give me more details about memorandum M-22-18",
        "expected": "The memorandum provides that a Federal agency may use software subject to M-22-18’s requirements2 only if the producer of that software has first attested to compliance with Federal Government-specified secure software development practices drawn from the SSDF.",
    },
    {
        "name": "BSSIM Report",
        "question": "I want to know about SRI.2: 96",
        "expected": "The organization has a well-known central location for information about software security. Typically, this is an internal website maintained by the SSG and security champions that people refer to for current information on security policies, standards, and requirements, as well as for other resources (such as training). An interactive portal is better than a static portal with guideline documents that rarely change. Organizations often supplement these materials with mailing lists, chat channels (see [T2.12]), and face-to-face meetings. Development teams are increasingly putting software security knowledge directly into toolchains and automation that are outside the organization (e.g., GitHub), but that does not remove the need for SSG-led knowledge management.",
    },
    {
        "name": "BSSIM Report - Security Feature Review",
        "question": "I want to know about AA1.1: 99",
        "expected": "Security-aware reviewers identify application security features, review these features against application security requirements and runtime parameters, and determine if each feature can adequately perform its intended function—usually collectively referred to as threat modeling. The goal is to quickly identify missing security features and requirements, or bad deployment configuration (authentication, access control, use of cryptography, etc.), and address them. For example, threat modeling would identify both a system that was subject to escalation of privilege attacks because of broken access control as well as a mobile application that incorrectly puts PII in local storage. Use of the firm’s secure-by-design components often streamlines this process (see [SFD2.1]). Many modern applications are no longer simply “3-tier” but instead involve components architected to interact across a variety of tiers—browser/endpoint, embedded, web, microservices, orchestration engines, deployment pipelines, third-party SaaS, etc. Some of these environments might provide robust security feature sets, whereas others might have key capability gaps that require careful analysis, so organizations should consider the applicability and correct use of security features across all tiers that constitute the architecture and operational environment.",
    },
    {
        "name": "BSSIM Report - Compliance and Policy",
        "question": "Give me median scores in Compliance & Policy in BSSIM Report.",
        "expected": "Another strong practice in terms of median scores is Compliance & Policy, with an overall median score of 54.4%. In fact, six of the eight verticals have a median score of 54.4%. Financial achieves the highest median score of 63.6%, and Insurance achieves the lowest median score of 45.5%.",
    },
    {
        "name": "CNCF Pdf",
        "question": "What does the report say about preventing secret commits to source code repository",
        "expected": "Secrets such as credential files, SSH keys and access tokens or API keys should not be committed to the source code repository unless encrypted prior to placement21. Tooling exists to detect secret key leaks, such as trufflehog22, which can be implemented using either a client-side hook (pre-commit), server-side hook (pre-receive or update), and as a step in the CI process.",
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

def run_all_tests_for_model(model_name: str):
    results = []
    for test in TEST_CASES:
        try:
            result = query_and_validate(
                test["question"],
                test["expected"],
                model_name=model_name
            )
            results.append((test["name"], result))
        except Exception as e:
            print(f"Error in {test['name']}: {e}")
            results.append((test["name"], None))
    return results
