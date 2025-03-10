import logging
import re
from difflib import get_close_matches

class CustomOutputParser:
    def parse(self, output: str) -> dict:
        try:
            sections = self.extract_sections(output)
            target_keys = ['Final Twitter (X) Post:', 'Twitter Post:', 'Final Twitter Post', 'Final Twitter(X)', 'Post', 'Text', 'Endgültiger Twitter (X) Post']
            final_post_key = self.find_closest_key(sections.keys(), target_keys)

            if not final_post_key:
                logging.error("Final Twitter (X) Post not found in the output.")
                return {"type": "raw_output", "content": output.strip()}

            final_post = sections[final_post_key]
            return {"type": "final_answer", "content": final_post.strip()}
        except Exception as e:
            logging.error(f"Error parsing LLM output: {e}")
            return {"type": "raw_output", "content": output.strip()}

    def extract_sections(self, text: str) -> dict:
        sections = {}
        current_section = None
        section_header_pattern = re.compile(r"^\*\*(.*?)\*\*$")

        for line in text.split('\n'):
            header_match = section_header_pattern.match(line)
            if header_match:
                current_section = header_match.group(1).strip()
                sections[current_section] = ""
            elif current_section:
                sections[current_section] += line + "\n"

        sections = {key: value.strip() for key, value in sections.items()}
        logging.debug(f"Extracted sections: {sections}")
        return sections

    def find_closest_key(self, keys, target_keys):
        all_keys = list(keys)
        for target in target_keys:
            closest_matches = get_close_matches(target, all_keys, n=1, cutoff=0.7)
            if closest_matches:
                return closest_matches[0]
        return None

class OutputParserException(Exception):
    pass

# Ensure logging is set up to show debug information
logging.basicConfig(level=logging.DEBUG)
