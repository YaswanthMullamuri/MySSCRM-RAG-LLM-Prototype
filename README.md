# Prototyping LLMs for MySSCRM

## Steps to make this work:

- First Install Ollama and keep it running with required LLMs used for embedding the data and executing the prompts.
- Create a virtual environment if required.
- Install requirements.txt
```
pip install -r requirements.txt
```
- Run these files in order
```
python3 populate_database.py
python3 query_data.py "Query/Prompt"
```

From now, just run the tests just like any other python file instead of pytest!
```
python3 test_rag.py --model {modelname}
```

To run tests with multiple models:
```
python3 multi_model_rag_runner.py {number}
```
