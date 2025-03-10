import pandas as pd
import logging
from tqdm import tqdm
from config import load_config


config = load_config()

GER_KEY = config.paths.input["key_ger_demographic"]
US_KEY = config.paths.input["key_us_demographic"]

class DataPreProcessor:
    def __init__(self, data_path, key_path, language='EN'):
        self.data_path = data_path
        self.key_path = key_path
        self.data = None
        self.key = None
        self.cleaned_data = None
        self.language = language
        self.required_columns = []
        logging.basicConfig(level=config.logging.level, format=config.logging.format)

    def read_data(self):
        logging.info("Reading data from CSV and Excel files.")
        self.data = pd.read_csv(self.data_path).set_index("unique_id")
        self.key = pd.read_excel(self.key_path, index_col=0)
    
    def clean_dataframes(self):
        logging.info("Cleaning dataframes.")
        self.key = self.key.iloc[3:]
        self.key.columns = self.key.iloc[0]
        self.key = self.key[1:]

        self.data.drop_duplicates(inplace=True)
        self.data = self.data[self.data["F7cA1"] != 0]
        if "Unnamed: 0" in self.data.columns:
            self.data = self.data.drop(['Unnamed: 0'], axis=1)
        if "wave_first" in self.data.columns:
            self.data = self.data.drop(['wave_first'], axis=1)

    def map_data_to_key(self):
        logging.info("Mapping data to key.")
        question_codes = self.data.columns
        demo_key = self.key[self.key['Custom variable name'].isin(question_codes)]
        questions_dict = demo_key.set_index("Custom variable name")["Text"].dropna().to_dict()
        
        logging.info("Questions Dictionary:")
        logging.info(questions_dict)
        
        nested_response_map = self._create_nested_response_map(questions_dict)
        common_items = {key: value for key, value in nested_response_map.items() if key in questions_dict}
        free_options = set(questions_dict.keys()) - set(common_items.keys())

        for item in free_options:
            common_items[item] = {}

        decoded_dict = {"user": []}
        for key, value in common_items.items():
            decoded_dict[key] = []

        logging.info("Checking if required columns are present in data.")
        for col in self.required_columns:
            if col in self.data.columns:
                logging.info(f"Column {col} is present.")
            else:
                logging.warning(f"Column {col} is missing.")

        for idx, row in self.data.iterrows():
            decoded_dict["user"].append(idx)
            for key, value in common_items.items():
                response_code = str(int(row[key]))
                if len(response_code) >= 3 or key == "F7cA1":
                    decoded_dict[key].append(response_code)
                else:
                    response = common_items[key].get(response_code, "Unknown")
                    decoded_dict[key].append(response)

        self.cleaned_data = {questions_dict.get(key, key): value for key, value in decoded_dict.items()}
        self._rename_special_columns()

    def _create_nested_response_map(self, questions_dict):
        nested_response_map = {}
        current_question_code = None
        nan_streak_count = 0

        for _, row in self.key.iterrows():
            question_code = row['Custom variable name']
            response_code = row['Characteristic']
            response_text = row['Value labels']

            if pd.isna(response_code) and pd.isna(response_text): 
                nan_streak_count += 1
            else:
                nan_streak_count = 0

            if nan_streak_count >= 3:
                nan_streak_count = 0
                current_question_code = None
                continue

            if pd.notna(question_code):
                current_question_code = question_code

            if current_question_code and pd.notna(response_code) and pd.notna(response_text):
                if current_question_code not in nested_response_map:
                    nested_response_map[current_question_code] = {}
                nested_response_map[current_question_code][str(response_code)] = response_text

        return nested_response_map
    
    def _convert_floats_to_ints(self, d):
        if isinstance(d, dict):
            return {k: self._convert_floats_to_ints(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [self._convert_floats_to_ints(i) for i in d]
        elif isinstance(d, str) and d.endswith('.0'):
            try:
                return int(float(d))
            except ValueError:
                return d
        else:
            return d

    def _rename_special_columns(self):
        if self.language == 'EN':
            try:
                self.cleaned_data['What is your ZIP code?'] = self.cleaned_data.pop('Enter a 5-digit number.:')
                self.cleaned_data['In which year were you born?'] = self.cleaned_data.pop('Enter a 4-digit number between 1910 and 2010:')
            except KeyError:
                pass
        elif self.language == 'DE':
            try:
                self.cleaned_data['Was ist Ihre Postleitzahl? '] = self.cleaned_data.pop('PLZ:')
                self.cleaned_data['Wie alt sind Sie? '] = self.cleaned_data.pop('Jahr')
            except KeyError:
                pass
    
    def save_data(self, destination_path):
        logging.info(f"Saving cleaned data to {destination_path}.")
        final_data = pd.DataFrame(self.cleaned_data)
        final_data.set_index("user", inplace=True)
        final_data.to_csv(destination_path)
        logging.info("Data saved successfully.")
    
    def end_to_end(self, destination_path):
        logging.info("Performing all pre-processing steps at once...")
        logging.info("Reading the data...")
        self.read_data()
        logging.info("Cleaning the data...")
        self.clean_dataframes()
        logging.info("Converting the data into an easy to interpret format...")
        self.map_data_to_key()
        self.save_data(destination_path)

class PoliticalDataProcessor(DataPreProcessor):
    def __init__(self, data_path, key_path, language='EN'):  
        super().__init__(data_path, key_path, language)
        self._set_mappings()
        logging.basicConfig(level=config.logging.level, format=config.logging.format)

    def _set_mappings(self):
        if self.language == 'DE':
            self.code_mapping = {
                "F6b_cdu": "F6b_cduA1",
                "F6b_spd": "F6b_spdA1",
                "F6b_fdp": "F6b_fdpA1",
                "F6b_gruenen": "F6b_gruenenA1",
                "F6b_linke": "F6b_linkeA1",
                "F6b_afd": "F6b_afdA1",
                "F6m": "F6mA1_1",
                "F6c": "F6c.1"
            }
            self.manual_response_map = {   
                "1": "0-links",
                "2": "1",
                "3": "2",
                "4": "3",
                "5": "4",
                "6": "5",
                "7": "6",
                "8": "7",
                "9": "8",
                "10": "9",
                "11": "10-rechts"
            }
            self.manual_response_map_eu = {
                "1": "CDU/CSU",
                "2": "Bündnis 90/Die Grünen",
                "3": "SPD",
                "4": "AfD",
                "5": "Die Linke",
                "6": "FDP",
                "7": "Freie Wähler",
                "8": "Die PARTEI",
                "9": "ÖDP (Ökologisch Demokratische Partei)",
                "10": "Piraten",
                "11": "Volt",
                "12": "Familienpartei",
                "13": "Bündnis Deutschland",
                "14": "Tierschutzpartei",
                "15": "Bündnis Sahra Wagenknecht (BSW)",
                "16": "Eine andere Partei",
                "17": "Ich habe nicht vor, an der Wahl teilzunehmen."
            }
            self.required_columns = ["F6m", "F6b_cdu", "F6b_spd", "F6b_fdp", "F6b_gruenen", "F6b_linke", "F6b_afd", "F6c", "F7p"]
        else:
            self.code_mapping = {
                "F6b_RepParty": "F6b_RepPartyA1",
                "F6b_DemParty": "F6b_DemPartyA1"
            }
            self.manual_response_map = {   
                "1": "0-Left",
                "2": "1",
                "3": "2",
                "4": "3",
                "5": "4",
                "6": "5",
                "7": "6",
                "8": "7",
                "9": "8",
                "10": "9",
                "11": "10-Right"
            }
            self.required_columns = ["F6mA1_1", "F7p", "F7o", "F6b_RepParty", "F6b_DemParty"]

    def map_data_to_key(self):
        logging.info("Mapping data to key.")
        questions_dict = self._get_questions_dict()
        nested_response_map = self._create_nested_response_map(questions_dict)
        self.cleaned_data = self._map_responses_to_text(questions_dict, nested_response_map)
        self._rename_special_columns()
        logging.info("Data mapping completed.")

    def _get_questions_dict(self): 
        demo_key = self.key[self.key['Custom variable name'].isin(self.required_columns)]
        questions_dict = demo_key.set_index("Custom variable name")["Text"].dropna().to_dict()
        logging.info("Questions Dictionary:")
        logging.info(questions_dict)
        return questions_dict

    def _map_responses_to_text(self, questions_dict, nested_response_map):
        decoded_dict = {"user": []}
        for question_code, question_text in questions_dict.items():
            decoded_dict[question_text] = []

        for idx, row in tqdm(self.data.iterrows(), total=self.data.shape[0], desc="Mapping responses"):
            decoded_dict["user"].append(idx)
            for question in questions_dict:
                mapped_question = self.code_mapping.get(question, question)
                if mapped_question in row and pd.notna(row[mapped_question]):
                    response_code = str(row[mapped_question]).rstrip('.0').strip()
                    response_text = self._get_response_text(mapped_question, response_code, nested_response_map)
                    decoded_dict[questions_dict[question]].append(response_text)
                else:
                    decoded_dict[questions_dict[question]].append("Unknown")
        return self._convert_floats_to_ints(decoded_dict)

    def _get_response_text(self, question, response_code, nested_response_map):
        if question in self.code_mapping.values():
            if question == "F6c.1":
                return self.manual_response_map_eu.get(response_code, "Unknown")
            else:
                return self.manual_response_map.get(response_code, "Unknown")

        return nested_response_map.get(question, {}).get(response_code, "Unknown")

    def _rename_special_columns(self):
        if self.language == 'EN':
            try:
                self.cleaned_data['What is your ZIP code?'] = self.cleaned_data.pop('Enter a 5-digit number.:')
                self.cleaned_data['In which year were you born?'] = self.cleaned_data.pop('Enter a 4-digit number between 1910 and 2010:')
            except KeyError:
                pass
        elif self.language == 'DE':
            try:
                parties = ["CDU", "SPD", "FDP", "BÜNDNIS 90 / Die Grünen", "Die Linke", "AFD"]
                for party in parties:
                    self.cleaned_data[f'In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei {party} auf dieser Skala einordnen (0-links bis 10-rechts)?'] = self.cleaned_data.pop(party)
                self.cleaned_data['Was ist Ihre Postleitzahl? '] = self.cleaned_data.pop('PLZ:')
                self.cleaned_data['Wie alt sind Sie? '] = self.cleaned_data.pop('Jahr')
            except KeyError:
                pass

# Set up logging
logging.basicConfig(level=config.logging.level, format=config.logging.format)

# Initialize and process the political data
# For German political data
political_data_processor = PoliticalDataProcessor(
    data_path=config.paths.input["filtered_responses_ger"], 
    key_path=config.paths.input["key_ger_demographic"], 
    language=config.settings.default_language
)
political_data_processor.end_to_end(config.paths.output["ger_political_results"])

# For German demographic data
data_processor = DataPreProcessor(
    data_path=config.paths.input["ger_demographic_data"], 
    key_path=config.paths.input["key_ger_demographic"], 
    language=config.settings.default_language
)
data_processor.end_to_end(config.paths.output["ger_demographic_results"])

# For US political data
political_data_processor = PoliticalDataProcessor(
    data_path=config.paths.input["filtered_responses_us"], 
    key_path=config.paths.input["key_us_demographic"], 
    language=config.settings.default_language
)
political_data_processor.end_to_end(config.paths.output["us_political_results"])

# For US demographic data
data_processor = DataPreProcessor(
    data_path=config.paths.input["us_demographic_data"], 
    key_path=config.paths.input["key_us_demographic"], 
    language=config.settings.default_language
)
data_processor.end_to_end(config.paths.output["us_demographic_results"])
