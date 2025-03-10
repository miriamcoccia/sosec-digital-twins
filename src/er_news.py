import json
from eventregistry import EventRegistry, QueryArticles, QueryItems, RequestArticlesInfo
from config import load_config
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

class News:
    def __init__(self, config):
        self.er = EventRegistry(API_KEY)
        self.config_file = config.event_registry.topics_path
        with open(self.config_file, "r") as f:
            self.topic_parameters = json.load(f)
            self.available_topics = list(self.topic_parameters.keys())

    def set_topic(self, topic):
        self.topic = topic
        if self.topic in self.topic_parameters:
            self.keywords = self.topic_parameters[self.topic]["keywords"]
            self.people_uris = self.topic_parameters[self.topic]["people_uris"]
            self.orgs_uris = self.topic_parameters[self.topic]["orgs_uris"]
            self.source_location_uri = self.topic_parameters[self.topic]["source_location_uri"]
        else:
            raise ValueError(f"Topic not found. The available topics are: {self.available_topics}")

    def get_news(self):
        all_uris = self.people_uris + self.orgs_uris
        base_query = QueryArticles(
            keywords=QueryItems.OR(self.keywords),
            conceptUri=QueryItems.OR(all_uris),
            sourceLocationUri=self.source_location_uri,
            lang="eng" if self.config_file.endswith("us.json") else "deu",
            isDuplicateFilter="skipDuplicates",
            keywordsLoc="body,title",
            eventFilter="skipArticlesWithoutEvent"
        )
        request_articles_info = RequestArticlesInfo(count=1, sortBy="socialScore")
        res = self.er.execQuery(base_query, request_articles_info)
        articles = res.get("articles", {}).get("results", [])
        return articles[1] if len(articles) > 1 else articles[0]
