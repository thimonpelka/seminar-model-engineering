run-llama:
	curl -fsSL https://ollama.ai/install.sh | sh
	ollama serve
	ollama pull llama3.2

run_app:
	pip install -r requirements.txt
	python main.py
