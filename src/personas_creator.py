import pandas as pd
import json
import logging
from config import load_config

config = load_config()

class PersonasCreator:
    def __init__(self, data_path: str, lang: str, destination: str):
        self.data_path = data_path
        self.lang = lang
        self.personas = []
        self.destination = destination
    
    def load_data(self):
        data = pd.read_csv(self.data_path, index_col=0)
        return data[~data.index.duplicated(keep='first')]
    
    def get_prompt_template(self):
        prompt_templates = {
            "en": "You are a social media user who has provided the following information about yourself:\n",
            "de": "Du bist ein*e Nutzer*in sozialer Medien mit folgenden Eigenschaften:\n"
        }
        question_format = {
            "en": "To the question: '{question}', your response was: '{answer}'\n",
            "de": "Auf die Frage: '{question}', war deine Antwort: '{answer}'\n"
        }
        return prompt_templates.get(self.lang), question_format.get(self.lang)

    def create_prompt(self):
        data = self.load_data()
        prompt_template, question_line = self.get_prompt_template()

        if not prompt_template or not question_line:
            raise ValueError("Unsupported language. Please use 'en' or 'de'.")

        self.personas = [
            {
                "id": index,
                "persona_prompt": prompt_template + ''.join(
                    question_line.format(question=question, answer=row[question])
                    for question in data.columns
                )
            }
            for index, row in data.iterrows()
        ]

    def to_json(self):
        with open(self.destination, "w", encoding="utf-8") as f:
            json.dump(self.personas, f, ensure_ascii=False, indent=4)

    def create_personas(self):
        self.create_prompt()
        self.to_json()

class PoliticalPersonasCreator(PersonasCreator):
    def get_prompt_template(self):
        prompt_templates = {
            "en": "These are the information you have provided about your political stance and opinions, **NOTE** the political scale works as a spectrum which goes from 1 to 10, where 1 corresponds to extreme left views, and 10 to extreme right views.",
            "de": "Hier sind die Aussagen, die du über deine politische Meinung und Einstellung getroffen hast, **WICHTIG** : die politische Skala funktioniert als Spektrum, das von 1 bis 10 reicht, wobei 1 extremen linken Ansichten entspricht und 10 extremen rechten Ansichten."
        }
        question_format = {
            "en": "To the question: '{question}', your response was: '{answer}'\n",
            "de": "Auf die Frage: '{question}', war deine Antwort: '{answer}'\n"
        }
        return prompt_templates.get(self.lang), question_format.get(self.lang)

    def create_prompt(self):
        data = self.load_data()
        prompt_template, question_line = self.get_prompt_template()

        if not prompt_template or not question_line:
            raise ValueError("Unsupported language. Please use 'en' or 'de'.")

        self.personas = [
            {
                "id": index,
                "political_prompt": prompt_template + ''.join(
                    question_line.format(question=question, answer=row[question])
                    for question in data.columns
                )
            }
            for index, row in data.iterrows()
        ]

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Helper function to create personas
def create_personas(creator_class, data_path, lang, destination):
    logging.info(f"Creating personas for {data_path}")
    creator = creator_class(data_path, lang, destination)
    creator.create_personas()
    logging.info(f"Personas created and saved to {destination}")

# Create personas for German demographic data
create_personas(
    PersonasCreator,
    config.paths.input["ger_demographic_results"],
    config.settings.additional_language,
    config.paths.output["ger_personas_demographic"]
)

# Create personas for German political data
create_personas(
    PoliticalPersonasCreator,
    config.paths.input["ger_political_data"],
    config.settings.additional_language,
    config.paths.output["ger_political_personas"]
)

# Create personas for US demographic data
create_personas(
    PersonasCreator,
    config.paths.input["us_demographic_results"],
    config.settings.default_language,
    config.paths.output["us_personas_demographic"]
)

# Create personas for US political data
create_personas(
    PoliticalPersonasCreator,
    config.paths.input["us_political_data"],
    config.settings.default_language,
    config.paths.output["us_political_personas"]
)
