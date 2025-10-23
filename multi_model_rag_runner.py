# python3 multi_model_rag_runner.py 10 -> Runs each model 10 times

from test_rag import run_all_tests_for_model
import csv
import sys

MODELS = ["gemma3:1b", "llama3.2:3b", "mistral"]
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
output_file = "rag_model_comparison.csv"

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Model", "Run", "Test Name", "Result"])

    for model in MODELS:
        print(f"\n=== Testing model: {model} ===")
        for i in range(1, n + 1):
            print(f"\n--- Run {i}/{n} for {model} ---")
            results = run_all_tests_for_model(model)

            for test_name, result in results:
                if result is True:
                    res = "True"
                elif result is False:
                    res = "False"
                else:
                    res = "Unknown"
                writer.writerow([model, i, test_name, res])
                print(f"{test_name}: {res}")

print(f"\n✅ All results saved to {output_file}")