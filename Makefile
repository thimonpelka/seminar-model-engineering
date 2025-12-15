# Name of the virtual environment folder
VENV := venv

# Command to activate the virtual environment
ACTIVATE := $(VENV)/bin/activate

run-llama:
	curl -fsSL https://ollama.ai/install.sh | sh
	ollama serve
	ollama pull llama3.2

run-app: $(VENV)/bin/activate
	# Install dependencies inside the venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	# Run the app inside the venv
	$(VENV)/bin/python main.py