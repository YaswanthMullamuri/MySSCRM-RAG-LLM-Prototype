# Prototyping LLMs for MySSCRM

## Steps to make this work:

- Install Ollama and keep it running in the background.
    - Download -> (https://ollama.com/download)
    - From a terminal: ``` ollama serve ``` or you can keep Ollama GUI running.
- Install the models you want to use (https://ollama.com/library)
- Pull the following models to run current version of code:
    - gemma3:1b, llama3.2:3b, mistral, mxbai-embed-large:latest
    - Command to pull a model: ``` ollama pull {modelname} ```
- Create a virtual environment if required. A virtual environment is used to create an isolated Python environment so each project can have its own dependencies without affecting the system or other projects.
    - Run the following commands in the project folder.
    - ``` python -m venv myenv ```
    - Activate it.
        - Windows: ``` venv\Scripts\activate ```
        - Mac/Linux: ``` source venv/bin/activate ```
    - Install requirements.txt (After you're in a virtual environment, these dependencies will only be relevant to the current project.)
    - Virtual Environment Deactivation command: ``` deactivate ```
```
pip install -r requirements.txt
```
- Run these files in order
```
python3 populate_database.py
python3 query_data.py "Query/Prompt"
```
- ```populate_database.py``` embeddes the pdf documents to ChromaDB.
- ```query_data.py``` generates a response for your query.


- The below command tests actual response vs expected response with LLM-as-a-judge methodology.
```
python3 test_rag.py --model {modelname}
```

To run tests and compare with multiple models:
```
python3 multi_model_rag_runner.py {number}
```
