import json
import traceback
import subprocess
import os
from typing import Dict, List, Optional
import requests


class ModelValidationService:
    """Service to validate UML/model syntax using PlantUML"""

    def __init__(self):
        self.plantuml_url = "http://www.plantuml.com/plantuml/txt/"

    def validate_model(self, model_text: str) -> Dict:
        """Validate a PlantUML model"""
        try:
            # Check basic syntax
            if not model_text.strip().startswith("@start"):
                return {
                    "valid": False,
                    "errors": ["Model must start with @startuml or @startclass"],
                    "suggestions": ["Add @startuml at the beginning"]
                }

            if not "@end" in model_text:
                return {
                    "valid": False,
                    "errors": ["Model must end with @enduml or @endclass"],
                    "suggestions": ["Add @enduml at the end"]
                }

            # Try to render it (validates syntax)
            import base64
            import zlib

            # PlantUML encoding
            compressed = zlib.compress(model_text.encode('utf-8'))
            encoded = base64.b64encode(compressed).decode('ascii')

            # Make request to PlantUML server
            response = requests.get(f"{self.plantuml_url}{encoded}")

            if response.status_code == 200:
                return {
                    "valid": True,
                    "errors": [],
                    "message": "Model is syntactically valid",
                    "rendered_text": response.text
                }
            else:
                return {
                    "valid": False,
                    "errors": ["PlantUML server returned error"],
                    "suggestions": ["Check syntax carefully"]
                }

        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "suggestions": ["Check model syntax"]
            }


class CodeGenerationService:
    """Service to generate code from models"""

    def generate_code(self, model_text: str, target_language: str = "python") -> Dict:
        """Generate code from a UML class diagram"""
        try:
            # Parse classes from PlantUML
            classes = self._parse_classes(model_text)

            if target_language.lower() == "python":
                code = self._generate_python(classes)
            elif target_language.lower() == "java":
                code = self._generate_java(classes)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported language: {target_language}"
                }

            return {
                "success": True,
                "code": code,
                "language": target_language,
                "classes_found": len(classes)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Code generation error: {str(e)}"
            }

    def _parse_classes(self, model_text: str) -> List[Dict]:
        """Simple parser for PlantUML class definitions"""
        classes = []
        lines = model_text.split('\n')
        current_class = None

        for line in lines:
            line = line.strip()

            if line.startswith('class '):
                class_name = line.split()[1].rstrip('{')
                current_class = {
                    'name': class_name,
                    'attributes': [],
                    'methods': []
                }
                classes.append(current_class)

            elif current_class and line and not line.startswith('@') and not line == '}':
                if '(' in line and ')' in line:
                    # It's a method
                    current_class['methods'].append(line.strip())
                elif ':' in line or line.startswith('+') or line.startswith('-'):
                    # It's an attribute
                    current_class['attributes'].append(line.strip())

        return classes

    def _generate_python(self, classes: List[Dict]) -> str:
        """Generate Python code from parsed classes"""
        code = "# Auto-generated from UML model\n\n"

        for cls in classes:
            code += f"class {cls['name']}:\n"

            if cls['attributes'] or cls['methods']:
                # Constructor
                code += "    def __init__(self):\n"
                for attr in cls['attributes']:
                    attr_name = attr.split(':')[0].strip().lstrip('+-')
                    code += f"        self.{attr_name} = None\n"

                if not cls['attributes']:
                    code += "        pass\n"

                code += "\n"

                # Methods
                for method in cls['methods']:
                    method_name = method.split('(')[0].strip().lstrip('+-')
                    code += f"    def {method_name}(self):\n"
                    code += "        pass\n\n"
            else:
                code += "    pass\n"

            code += "\n"

        return code

    def _generate_java(self, classes: List[Dict]) -> str:
        """Generate Java code from parsed classes"""
        code = "// Auto-generated from UML model\n\n"

        for cls in classes:
            code += f"public class {cls['name']} {{\n"

            # Attributes
            for attr in cls['attributes']:
                parts = attr.split(':')
                attr_name = parts[0].strip().lstrip('+-')
                attr_type = parts[1].strip() if len(parts) > 1 else "Object"
                code += f"    private {attr_type} {attr_name};\n"

            if cls['attributes']:
                code += "\n"

            # Methods
            for method in cls['methods']:
                method_name = method.split('(')[0].strip().lstrip('+-')
                code += f"    public void {method_name}() {{\n"
                code += "        // TODO: Implement\n"
                code += "    }\n\n"

            code += "}\n\n"

        return code


class AgenticAI:
    """Main agent that coordinates between services"""

    def __init__(self):
        self.validator = ModelValidationService()
        self.code_gen = CodeGenerationService()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # or "mistral", "codellama"

    def call_llm(self, prompt: str, system_prompt: str = "") -> str:
        """Call local Ollama LLM"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }

            response = requests.post(self.ollama_url, json=payload)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error calling LLM: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}. Make sure Ollama is running (ollama serve)"

    def process_request(self, user_request: str) -> str:
        """Main agentic loop"""

        system_prompt = """You are an AI agent that helps with model engineering tasks.
You have access to two tools:
1. validate_model(model_text) - Validates UML/PlantUML models
2. generate_code(model_text, language) - Generates code from models

When the user asks you to validate or generate code, respond with a JSON function call like:
[{"action": "validate_model", "model": "...model text..."}]
or
[{"action": "generate_code", "model": "...model text...", "language": "python"}]

Valid languages are 'python' and 'java'.

If you want to do multiple actions then generate a list of actions similar to:

[
  {"action": "validate_model", "model": "...model text..."},
  {"action": "generate_code", "model": "...model text...", "language": "python"}
]

Please make sure you return syntactically valid json if you want to perform an action.

If the user is just asking questions, respond normally.
"""

        # Get LLM decision
        llm_response = self.call_llm(user_request, system_prompt)

        # Try to parse as JSON (function call)
        try:
            print(llm_response)
            actions = json.loads(llm_response)
            for action_data in actions:
                if action_data.get("action") == "validate_model":
                    result = self.validator.validate_model(
                        action_data["model"])
                    if not result["valid"]:
                        return f"Validation Result:\n{json.dumps(result, indent=2)}"
                    print("Validation succesful")

                elif action_data.get("action") == "generate_code":
                    result = self.code_gen.generate_code(
                        action_data["model"],
                        action_data.get("language", "python")
                    )
                    if result["success"]:
                        return f"Generated Code:\n\n{result['code']}"
                    else:
                        return f"Error: {result['error']}"
        except Exception as e:
            print(f"Error ocurred: {e}")
            print(traceback.format_exc())

        return llm_response


def main():
    print("=== Local Agentic AI for Model Engineering ===\n")
    print("Make sure Ollama is running: ollama serve")
    print("And pull a model: ollama pull llama3.2\n")

    agent = AgenticAI()

    # Example usage
    example_model = """@startuml
class Student {
  +name: String
  +id: int
  +enroll()
  +graduate()
}

class Course {
  +title: String
  +credits: int
  +addStudent()
}
@enduml"""

    print("\n\nExample: Validating a model:")
    prompt = f"Please validate this model:\n{example_model}"
    print()
    print("-" * 50)
    response = agent.process_request(
        f"{prompt}\n{
            example_model}"
    )
    print(response)

    print("\n\nExample: Generating code:")
    prompt = f"Please generate python code for this model:\n{example_model}"
    print()
    print("-" * 50)
    response = agent.process_request(
        f"{prompt}\n{example_model}"
    )
    print(response)

    print("\n\nExample: Validating the models and generating code:")
    print("-" * 50)
    response = agent.process_request(
        f"Please validate this model and then generate Python code:\n{
            example_model}"
    )
    print(response)

    print("\n\n=== Interactive Mode ===")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break

        response = agent.process_request(user_input)
        print(f"\nAgent: {response}")


if __name__ == "__main__":
    main()
