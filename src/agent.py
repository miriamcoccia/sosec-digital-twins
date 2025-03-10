import json
import logging
from llm import CustomLLM
from output_parser import CustomOutputParser, OutputParserException

class Agent:
    def __init__(self, llm: CustomLLM, persona_id: str, lang: str):
        self.llm = llm
        self.output_parser = CustomOutputParser()
        self.persona_id = persona_id
        self.lang = lang
        logging.debug(f"Agent initialized with persona_id={persona_id}, lang={lang}")

    def read_prompt_by_id(self, filename: str, key: str):
        logging.debug(f"Reading persona prompt from {filename} with key {key}")
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            persona_prompt = {entry['id']: entry.get(key) for entry in data}.get(self.persona_id, None)
            if not persona_prompt:
                logging.error(f"Persona ID {self.persona_id} not found in file {filename}")
            return persona_prompt
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logging.error(f"Error reading JSON file {filename}: {e}")
            raise Exception(f"Error reading JSON file {filename}: {e}")

    def handle_input(self, prompt: str):
        try:
            if self.lang == "de":
                political_file = "../data/reformatted_de_political_personas.json"
                demographic_file = "../data/reformatted_de_demographic_personas.json"
            else:
                political_file = "../data/reformatted_us_political_personas.json"
                demographic_file = "../data/reformatted_us_demographic_personas.json"

            if 'demographic' in self.persona_id.lower():
                persona_prompt = self.read_prompt_by_id(demographic_file, 'demographic_prompt')
            else:
                persona_prompt = self.read_prompt_by_id(political_file, 'political_prompt')
        except Exception as e:
            logging.error(f"Error reading persona prompts: {e}")
            return str(e)

        if not persona_prompt:
            logging.error("Persona ID not found in the selected file.")
            return "Persona ID not found in the selected file."

        combined_prompt = persona_prompt.strip()
        try:
            llm_output = self.llm.generate_response(combined_prompt, prompt)
            logging.debug(f"LLM Output: {llm_output}")
        except Exception as e:
            logging.error(f"Error generating response from LLM: {e}")
            return f"Error generating response from LLM: {e}"

        try:
            parsed_output = self.output_parser.parse(llm_output)
            logging.debug(f"Parsed Output: {parsed_output}")
            return parsed_output.get("content", llm_output)
        except OutputParserException as e:
            logging.error(f"Error parsing LLM output: {e}")
            return llm_output
        except Exception as e:
            logging.error(f"Unexpected error parsing LLM output: {e}")
            return llm_output
