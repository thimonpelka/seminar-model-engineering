## **1. Architecture Overview**

```
        +----------------+
        |   LLM Agent    |
        +----------------+
        | decides tasks  |
        +----------------+
        |                |
        v                v
+----------------+   +----------------+
| Model Validator|   | Code Generator |
+----------------+   +----------------+
| Validates a    |   | Generates code |
| model and gives|   | from model     |
| feedback       |   +----------------+
+----------------+
```

## **2. Quickstart**

### Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

### Start it and pull a model
ollama serve
ollama pull llama3.2

### Install Python deps
pip install requests

### Run the script
python main.py
