import yaml
import logging
from pydantic import BaseModel
from typing import Dict

class Paths(BaseModel):
    input: Dict[str, str]
    output: Dict[str, str]

class LoggingConfig(BaseModel):
    level: str
    format: str

class Settings(BaseModel):
    default_language: str
    additional_language: str
    supported_languages: Dict[str, str]
    supported_countries: Dict[str, str]
    llm_models: Dict[str, str]
    selected_model: str
    selected_language: str
    selected_country: str
    topic: str
    api_url: str = 'https://inf.cl.uni-trier.de/'  

class EventRegistryConfig(BaseModel):
    api_key: str
    topics_path: str

class Config(BaseModel):
    paths: Paths
    logging: LoggingConfig
    settings: Settings
    event_registry: EventRegistryConfig

def load_config(path: str = "config.yaml", selected_language: str = None) -> Config:
    with open(path, 'r') as stream:
        config = yaml.safe_load(stream)
    
    if selected_language:
        config["settings"]["selected_language"] = selected_language
        selected_country = "de" if selected_language == "de" else "us"
        config["settings"]["selected_country"] = selected_country
        
        # Update topics_path based on the selected language
        if selected_language == "de":
            config["event_registry"]["topics_path"] = "../data/topics_de.json"
        else:
            config["event_registry"]["topics_path"] = "../data/topics_us.json"
    
    paths = Paths(**config["paths"])
    logging_config = LoggingConfig(**config["logging"])
    settings = Settings(**config["settings"])
    event_registry = EventRegistryConfig(**config["event_registry"])

    logging.basicConfig(level=logging_config.level, format=logging_config.format)

    return Config(paths=paths, logging=logging_config, settings=settings, event_registry=event_registry)