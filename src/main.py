import logging
import random
from config import load_config
from llm import CustomLLM
from agent import Agent
from er_news import News
from prompt_utils import get_input_text_dem, get_input_text_pol
from pathlib import Path
import json
import sys

def select_language():
    while True:
        selected_language = input("Select the language of country in your data: German (de) or English (en): ").strip().lower()
        if selected_language in ['de', 'en']:
            return selected_language
        print("Invalid input. Please enter 'de' for German or 'en' for English.")

def select_prompt_type():
    while True:
        choice = input("Select the type of prompt to use: demographics (d) or political (p): ").strip().lower()
        if choice in ['d', 'p']:
            return choice
        print("Invalid input. Please enter 'd' for demographics or 'p' for political.")

def load_persona_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading JSON file {filename}: {e}")
        sys.exit(1)

def select_topic(news):
    available_topics = news.available_topics
    print("Available topics:")
    for index, topic in enumerate(available_topics, start=1):
        print(f"{index}. {topic}")
    
    while True:
        try:
            selected_topic_index = int(input("Please select a topic by entering its number: ")) - 1
            if 0 <= selected_topic_index < len(available_topics):
                return available_topics[selected_topic_index]
        except ValueError:
            pass
        print("Invalid selection. Please choose a valid topic number.")

def get_response_data(dataset_type, selected_language, persona_id, persona_prompt, response, article, selected_topic):
    return {
        "persona_id": persona_id,
        "persona_prompt": persona_prompt,
        "language": selected_language,
        "dataset_type": dataset_type,
        "response": response,
        "article_title": article.get('title'),
        "article_url": article.get('url'),
        "article_topic": selected_topic,
    }

def save_response(stars, response_data):
    if stars > 3:
        save_file = Path("good_responses.json")
    else:
        save_file = Path("bad_responses.json")

    if save_file.exists():
        existing_data = json.loads(save_file.read_text())
    else:
        existing_data = []

    existing_data.append(response_data)
    save_file.write_text(json.dumps(existing_data, indent=4))

def rate_response():
    while True:
        try:
            stars = int(input("Rate the response (1-5 stars): "))
            if 1 <= stars <= 5:
                return stars
        except ValueError:
            pass
        print("Invalid input. Please enter a number between 1 and 5.")

def main():
    logging.basicConfig(level=logging.DEBUG)
    
    selected_language = select_language()
    config = load_config(selected_language=selected_language)
    llm = CustomLLM(model=config.settings.selected_model, api_url=config.settings.api_url)
    choice = select_prompt_type()

    if choice == 'd':
        key = 'demographic_prompt'
        dataset_type = 'demographic'
        filename = "../data/reformatted_de_demographic_personas.json" if selected_language == "de" else "../data/reformatted_us_demographic_personas.json"
    else:
        key = 'political_prompt'
        dataset_type = 'political'
        filename = "../data/reformatted_de_political_personas.json" if selected_language == "de" else "../data/reformatted_us_political_personas.json"

    data = load_persona_file(filename)
    persona_id = random.choice(data)['id']
    agent = Agent(llm, persona_id, selected_language)
    persona_prompt = agent.read_prompt_by_id(filename, key)

    print(f"Selected {dataset_type} persona ID: {persona_id}")
    print(f"{dataset_type.capitalize()} prompt used: {persona_prompt}")

    news = News(config)
    selected_topic = select_topic(news)
    print(f"Selected topic: {selected_topic}")
    news.set_topic(selected_topic)

    try:
        article = news.get_news()
        logging.debug(f"Article: {article}")
        if not article:
            logging.error("No article found")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to fetch news article: {e}")
        sys.exit(1)

    input_text = get_input_text_dem(selected_topic, article, selected_language) if dataset_type == 'demographic' else get_input_text_pol(selected_topic, article, selected_language)
    response = agent.handle_input(input_text)
    print(f"{dataset_type.capitalize()} Response:", response)

    stars = rate_response()
    response_data = get_response_data(dataset_type, selected_language, persona_id, persona_prompt, response, article, selected_topic)
    save_response(stars, response_data)

if __name__ == "__main__":
    main()
