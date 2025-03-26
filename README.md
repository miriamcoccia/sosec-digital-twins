
```markdown
 ```
# SOSEC Digital Twins

This project develops generative agents modeled after SOSEC panel participants. These agents autonomously fetch the latest news on topics pertinent to the SOSEC questionnaire and generate corresponding posts for the X platform (formerly known as Twitter). The project includes a **Streamlit app** for easy interaction with the system.

## Features

- **News Retrieval**: Agents automatically search for the latest news articles related to specified topics.
- **Content Generation**: Utilizing advanced natural language processing techniques, agents craft concise and relevant posts suitable for the X platform.
- **Streamlit App**: A user-friendly interface to configure agents, monitor activity, and review generated content.
- **Customization**: Agents can be tailored to represent different SOSEC panel participants, allowing for diverse perspectives in content generation.

## Installation

To set up the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/miriamcoccia/sosec-digital-twins.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd sosec-digital-twins
   ```

3. **Set Up a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

   This will launch the app in your default web browser.

2. **Configure the Agents**: Use the app interface to set agent parameters and select topics of interest.

3. **Generate & Review Posts**: The app will fetch the latest news, generate content, and display it for review before posting.


## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for more details.

