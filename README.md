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

Run `make run-llama` and `run-app` next to each other.
