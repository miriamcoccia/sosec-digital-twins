import json
from config import load_config
from prompt_utils import reformat_all_prompts

def main():
    config = load_config()
    us_pol_original = config.paths.output["us_political_personas"]
    us_demo_original = config.paths.output["us_personas_demographic"]
    de_pol_original = config.paths.output["ger_political_personas"]
    de_demo_original = config.paths.output["ger_personas_demographic"]

    try:
        with open(us_pol_original, 'r') as file_us, \
            open(de_pol_original, 'r') as file_de:
                pol_prompts_us = json.load(file_us)
                pol_prompts_de = json.load(file_de)
        with open(us_demo_original, 'r') as file_us, \
            open(de_demo_original, 'r') as file_de:
                demo_prompts_us = json.load(file_us)
                demo_prompts_de = json.load(file_de)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    reformatted_pol_prompts_us = reformat_all_prompts(pol_prompts_us, "political")
    reformatted_demo_prompts_us = reformat_all_prompts(demo_prompts_us, "demographic")
    reformatted_pol_prompts_de = reformat_all_prompts(pol_prompts_de, "political")
    reformatted_demo_prompts_de = reformat_all_prompts(demo_prompts_de, "demographic")

    with open(r'../data/reformatted_us_political_personas.json', 'w') as file:
        json.dump(reformatted_pol_prompts_us, file, indent=4)
    with open(r'../data/reformatted_us_demographic_personas.json', 'w') as file:
        json.dump(reformatted_demo_prompts_us, file, indent=4)
    with open(r'../data/reformatted_de_political_personas.json', 'w') as file:
        json.dump(reformatted_pol_prompts_de, file, indent=4)
    with open(r'../data/reformatted_de_demographic_personas.json', 'w') as file:
        json.dump(reformatted_demo_prompts_de, file, indent=4)

if __name__ == "__main__":
    main()
