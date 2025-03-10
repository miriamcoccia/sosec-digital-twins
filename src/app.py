import streamlit as st
import json
from pathlib import Path
import logging
from agent import Agent
from config import load_config
from llm import CustomLLM
from er_news import News
from prompt_utils import get_input_text_dem, get_input_text_pol
import re

logging.basicConfig(level=logging.ERROR)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #1e1e2f;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e2f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

local_css("styles.css")

def format_persona_info(persona_prompt):
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', persona_prompt)
    return formatted_text.replace('\n', '<br>')

def load_persona_file(filename):
    try:
        return json.loads(Path(filename).read_text())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading JSON file {filename}: {e}")
        st.error(f"Error reading JSON file {filename}: {e}")
        st.stop()

def main():
    st.markdown('<div class="title-box"><h1>SOSEC Digital Twins</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="box"><h2>Introduction</h2><p>How can we leverage LLMs to mimic believable human behavior and reaction in response to emotionally charged global events? In this application, we create agents using in-context learning by providing a LLM with prompts describing the persona it should mimic, either considering their demographics or their political stance. Such instructions are based on data provided by human respondents to the SOSEC questionnaire.</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.radio("Select Language", ["English", "German"])
    
    with col2:
        persona_type = st.radio("Select Persona Type", ["Political", "Demographic"])
    
    language_map = {
        "English": "en",
        "German": "de"
    }
    selected_language = language_map[language]
    config = load_config(selected_language=selected_language)
    news = News(config)
    available_topics = news.available_topics

    # Load both persona files first
    demographic_file_de = "../data/reformatted_de_demographic_personas.json"
    demographic_file_us = "../data/reformatted_us_demographic_personas.json"
    political_file_de = "../data/reformatted_de_political_personas.json"
    political_file_us = "../data/reformatted_us_political_personas.json"

    demographic_personas = load_persona_file(demographic_file_de if selected_language == "de" else demographic_file_us)
    political_personas = load_persona_file(political_file_de if selected_language == "de" else political_file_us)

    # Combine persona IDs with an indication of their type
    persona_options = [{'id': persona['id'], 'type': 'Demographic'} for persona in demographic_personas]
    persona_options += [{'id': persona['id'], 'type': 'Political'} for persona in political_personas]

    # Filter persona options based on the selected type
    filtered_persona_ids = [option['id'] for option in persona_options if option['type'] == persona_type]
    if not filtered_persona_ids:
        st.error("No personas found for the selected type.")
        st.stop()
    
    selected_persona_id = st.selectbox("Select Persona ID", filtered_persona_ids)

    # Retrieve the selected persona's data
    if persona_type == "Demographic":
        selected_persona = next((persona for persona in demographic_personas if persona['id'] == selected_persona_id), None)
    else:
        selected_persona = next((persona for persona in political_personas if persona['id'] == selected_persona_id), None)

    if selected_persona is None:
        st.error("Persona ID not found in the selected file.")
        st.stop()

    # Determine the prompt text based on the persona type
    if persona_type == "Political":
        prompt_text = selected_persona['political_prompt']
    else:
        prompt_text = selected_persona['demographic_prompt']

    formatted_persona_info = format_persona_info(prompt_text)
    st.markdown(f'<div class="box"><h2>Selected Persona</h2><p class="persona-info">Selected {persona_type.lower()} persona ID: {selected_persona_id}</p><p class="persona-info">{formatted_persona_info}</p></div>', unsafe_allow_html=True)

    selected_topic = st.selectbox("Select Topic", available_topics)
    available_models = list(config.settings.llm_models.keys())
    selected_model_key = st.selectbox("Select Model", available_models)
    selected_model = config.settings.llm_models[selected_model_key]

    if 'response' not in st.session_state:
        st.session_state.response = ""
    if 'article' not in st.session_state:
        st.session_state.article = None

    if st.button("Generate Content"):
        llm = CustomLLM(model=selected_model, api_url=config.settings.api_url)
        agent = Agent(llm, persona_id=selected_persona_id, lang=selected_language)

        news.set_topic(selected_topic)
        article = None
        try:
            article = news.get_news()
        except Exception as e:
            if "User has been disabled" in str(e):
                st.warning("The news service is temporarily unavailable due to extensive usage. Generating response without news article.")
            else:
                st.error(f"An error occurred while fetching the news: {e}")
                return

        if not article:
            st.warning("No article found. Generating response without news article.")
            if persona_type == "Political":
                if selected_language == "en":
                    input_text = f"Generate a Twitter (X) post in maximum 260 characters about the topic of {selected_topic} based on your political stance provided above. "
                else:
                    input_text = f"Erstellen Sie einen Twitter (X) Beitrag im 260  zum Thema {selected_topic} basierend auf der politischen Haltung, die du obenan angegeben hast."
            else:
                if selected_language == "en":
                    input_text = f"Generate a Twitter (X) post in maximum 260 characters about the topic of {selected_topic} based on your demographic data provided above."
                else:
                    input_text = f"Erstellen Sie einen Twitter (X) Beitrag zum Thema {selected_topic} basierend auf deinen demographischen Daten, die du obenan angegeben hast."
        else:
            if persona_type == "Political":
                input_text = get_input_text_pol(selected_topic, article, selected_language)
            else:
                input_text = get_input_text_dem(selected_topic, article, selected_language)

        st.session_state.response = agent.handle_input(input_text)
        st.session_state.article = article

    st.markdown(f'<div class="box"><h2>Generated Response</h2><p>{st.session_state.response}</p></div>', unsafe_allow_html=True)

    if st.session_state.article:
        article_data = f"""Title: {st.session_state.article['title']}
Source: {st.session_state.article['source']['title']}
Date: {st.session_state.article['date']}
{st.session_state.article['body']}"""
        article_data = article_data.replace("\n", "<br>")
        st.markdown(f'<div class="box"><h2>Article Data</h2><p>{article_data}</p></div>', unsafe_allow_html=True)

    # Persistent slider for rating the response
    stars = st.slider("Rate the response (1-5 stars)", 1, 5, 3, key="rating_slider")

    if st.button("Save Response"):
        response_data = {
            "persona_id": selected_persona_id,
            "persona_prompt": prompt_text,
            "language": selected_language,
            "dataset_type": persona_type,
            "response": st.session_state.response,
            "article_title": st.session_state.article.get('title') if st.session_state.article else None,
            "article_url": st.session_state.article.get('url') if st.session_state.article else None,
            "article_topic": selected_topic,
            "rating": stars
        }
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
        st.success("Response saved successfully!")

if __name__ == "__main__":
    main()
