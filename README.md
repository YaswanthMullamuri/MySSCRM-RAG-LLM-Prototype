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

To run tests, run the below command. Depending on python version, this will change!
```
python3 -m pytest -s -q test_rag.py
```