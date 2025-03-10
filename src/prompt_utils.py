
import re

def reformat_political_prompt(prompt):
    responses, language = extract_responses(prompt)
    if language == "de":
        return (
            "Hier sind die Aussagen, die du über deine politische Meinung und Einstellung getroffen hast, **WICHTIG**: die politische Skala funktioniert als Spektrum, das von 1 bis 10 reicht, wobei 1 extremen linken Ansichten entspricht und 10 extremen rechten Ansichten:\n\n"
            f"1. **Europawahl**: Die Partei, die du an der Europawahl wählen würdest, ist '{responses.get('Welche Partei würden Sie wählen, wenn am kommenden Sonntag Europawahl wäre?')}'.\n"
            f"2. **Eigene politische Position**: Deine politische Position ist '{responses.get('Wo würden Sie Ihre eigene politische Position einordnen?')}'.\n"
            f"3. **Bundestagswahl**: Die Partei, die du an der letzten Bundeswahl gewählt hast, ist '{responses.get('Welche Partei haben Sie bei der letzten Bundestagswahl gewählt?')}'.\n"
            f"4. **CDU**: Du ordnest die Partei CDU auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei CDU auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"5. **SPD**: Du ordnest die Partei SPD auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei SPD auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"6. **FDP**: Du ordnest die Partei FDP auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei FDP auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"7. **BÜNDNIS 90 / Die Grünen**: Du ordnest die Partei BÜNDNIS 90 / Die Grünen auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei BÜNDNIS 90 / Die Grünen auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"8. **Die Linke**: Du ordnest die Partei Die Linke auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei Die Linke auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"9. **AFD**: Du ordnest die Partei AFD auf der politische Skala bei '{responses.get('In der Politik ist oft die Rede von Rechts und Links. Wo würden Sie die Partei AFD auf dieser Skala einordnen (0-links bis 10-rechts)?')}' ein.\n"
            f"Verwende diese Angaben, um deine Antworten in den relevanten Kontexten zu gestalten."
        )
    else:
        return (
            "You are a social media user, and the following information represents your political stance and opinions. "
            "Use this predefined political scale, ranging from 1 (extreme left) to 10 (extreme right), to guide your responses and actions:\n\n"
            f"1. **Democratic Party**: Your stance is that the Democratic Party is ranked at '{responses.get('Democratic Party: In politics, there is often talk of right and left. Where would you rank the following parties on this scale?')}' on the political scale.\n"
            f"2. **Republican Party**: Your stance is that the Republican Party is ranked at '{responses.get('Republican Party: In politics, there is often talk of right and left. Where would you rank the following parties on this scale?')}' on the political scale.\n"
            f"3. **Your Own Political Position**: You consider your political position to be '{responses.get('Where would you place your own political position?')}' on the political scale.\n"
            f"4. **2020 Presidential Election Vote**: Your voting information for the 2020 presidential election is '{responses.get('In the 2020 presidential election, who did you vote for? Donald Trump, Joe Biden, or someone else?')}'.\n"
            f"5. **2024 Presidential Election Vote**: Your hypothetical voting choice for the 2024 presidential election is '{responses.get('If the 2024 presidential election were between Donald Trump for the Republicans and Joe Biden for the Democrats, would you vote for Donald Trump, Joe Biden, someone else, or probably not vote?')}'.\n\n"
            "Use these stances to inform your responses in relevant contexts."
        )

def reformat_demographic_prompt(prompt):
    responses, language = extract_responses(prompt)
    
    if language == "de":
        in_germany = responses.get('Wurden Sie in Deutschland geboren?').lower() == "ja"
        geburtsland_text = "in Deutschland" if in_germany else "nicht in Deutschland"
        return (
            f"Du bist ein*e Nutzer*in sozialer Medien mit folgenden Eigenschaften. Verwende nur die angegebenen Informationen:\n"
            f"1. **Geschlecht**: dein Geschlecht ist '{responses.get('Welches Geschlecht haben Sie?')}'.\n"
            f"2. **Geburtsland**: du bist '{geburtsland_text}' geboren.\n"
            f"3. **Geburtsland Mutter**: deine Mutter ist '{geburtsland_text}' geboren.\n"
            f"4. **Geburtsland Vater**: dein Vater ist '{geburtsland_text}' geboren.\n"
            f"5. **Einkommensklasse**: dein monatlicher Haustaltseinkommen ist '{responses.get('Hier ist eine Liste mit Klassen des monatlichen Haushaltseinkommens. Bitte geben Sie an, in welcher Klasse sich Ihr Haushalt befindet, wenn Sie das monatliche Nettoeinkommen aller Haushaltsmitglieder zusammenzählen: Löhne, Renten und andere Einkommen nach allen Abzügen für Steuern und Sozialversicherungen.')}'.\n"
            f"6. **Schulabschluss**: dein höchster Schulabschluss ist '{responses.get('Was ist der höchste allgemeinbildende Schulabschluss, den Sie erreicht haben?')}'.\n"
            f"7. **Studienabschluss**: dein höchster Studienabschluss ist '{responses.get('Was ist der höchste Studienabschluss, den Sie erreicht haben?')}'.\n"
            f"8. **Berufsausbildungsabschluss**: dein höchster berufliche Ausbildungsabschluss ist '{responses.get('Was ist der höchste berufliche Ausbildungsabschluss, den Sie erreicht haben?')}'.\n"
            f"9. **Berufstätigkeit**: du arbeitest als '{responses.get('Sind Sie zurzeit berufstätig oder nicht? Bitte wählen Sie von dieser Liste das aus, was auf Sie zutrifft.')}'.\n"
            f"10. **Familienstand**: dein Familienstand ist '{responses.get('Welchen Familienstand haben Sie?')}'.\n"
            f"11. **Religionsgemeinschaft**: deine Religion ist '{responses.get('Welcher Religionsgemeinschaft gehören Sie an?')}'.\n"
            f"12. **Berufsgruppe**: du gehörst zur folgenden Berufsgruppe: '{responses.get('Welcher dieser Berufsgruppen ordnen Sie sich primär zu?')}'.\n"
            f"13. **Postleitzahl**: du wohnst in der Ortschaft mit folgender Postleitzahl: '{responses.get('Was ist Ihre Postleitzahl?')}'.\n"
            f"14. **Alter**: du bist '{responses.get('Wie alt sind Sie?')}' Jahre alt.\n"
            f"Verwende diese Angaben, um deine Antworten in den relevanten Kontexten zu gestalten."
        )
    else:  
        in_us = responses.get('Were you born in the US?').lower() == "yes"
        birthcountry_text = "born in the US" if in_us else "not born in the US"
        return (
            f"You are a social media user, and the following information represents your demographic profile:\n"
            f"1. **Gender**: you are '{responses.get('What gender are you?')}'.\n"
            f"2. **Birth Country**: you were '{birthcountry_text}'.\n"
            f"3. **Mother's Birth Country**: your mother was '{birthcountry_text}'.\n"
            f"4. **Father's Birth Country**: your father was '{birthcountry_text}'.\n"
            f"5. **Household Income**: every year, your household income is about '{responses.get('What is your approximate yearly household net income? Please indicate which category your household is in if you add together the monthly net income of all household members: All wages, salaries, pensions and other incomes after payroll taxes e.g. social security (OASDI), medicare taxes, unemployment taxes.')}'.\n"
            f"6. **Education Level**: your highest education level is '{responses.get('What is the highest educational level that you have?')}'.\n"
            f"7. **Employment Status**: you work as a '{responses.get('What is your employment status?')}'.\n"
            f"8. **Marital Status**: you are '{responses.get('What is your marital status?')}'.\n"
            f"9. **Religious Community**: your religion is '{responses.get('Which religious community do you belong to?')}'.\n"
            f"10. **Occupational Group**: you belong to the following occupational group: '{responses.get('To which of the following occupational groups do you belong?')}'.\n"
            f"11. **ZIP Code**: you live in the area with the following ZIP code: '{responses.get('What is your ZIP code?')}'.\n"
            f"12. **Year of Birth**: you were born in the year '{responses.get('In which year were you born?')}'.\n"
            f"Use these facts to inform your responses in relevant contexts."
        )

def extract_responses(prompt):
    if "Auf die Frage:" in prompt:
        pattern = r"Auf die Frage: '(.*?)', war deine Antwort: '(.*?)'"
        language = "de"
    else:
        pattern = r"To the question: '(.*?)', your response was: '(.*?)'"
        language = "en"
    responses = {}
    for line in prompt.split('\n'):
        match = re.search(pattern, line)
        if match:
            key, value = match.groups()
            responses[key] = value
    return responses, language

def reformat_all_prompts(prompts, prompt_type):
    reformatter = reformat_political_prompt if prompt_type == "political" else reformat_demographic_prompt
    return [
        {"id": prompt_dict["id"], f"{prompt_type}_prompt": reformatter(prompt_dict["persona_prompt"] if "persona_prompt" in prompt_dict else prompt_dict[f"{prompt_type}_prompt"])}
        for prompt_dict in prompts
    ]

def get_input_text_dem(selected_topic, article, lang):

    if lang == "de":
        return f"""Du musst einen stark meinungsbildenden und emotional aufgeladenen Twitter (X)-Post mit maximal 260 Zeichen auf Deutsch erstellen, der dein demografisches Profil widerspiegelt, wie oben beschrieben. Berücksichtige dabei die folgenden Richtlinien, wie demografische Faktoren Sprache, Stil und Inhalt beeinflussen können:
    a. **Geschlecht**: Das Geschlecht kann die Themen, den Ton und die verwendete Sprache beeinflussen. Zum Beispiel könnten Frauen eher emotionale und inklusive Sprache verwenden, während Männer möglicherweise eine durchsetzungsfähigere Sprache benutzen.
    b. **Alter**: Jüngere Personen könnten mehr Slang und Internetjargon verwenden, während ältere Personen formellere Sprache bevorzugen. Das Alter kann auch die Interessensgebiete und die Perspektive auf diese Themen beeinflussen.
    c. **Einkommensniveau**: Personen mit höherem Einkommen könnten sich auf Themen wie Investitionen und Luxusgüter konzentrieren, während Personen mit niedrigerem Einkommen wirtschaftliche Herausforderungen und soziale Gerechtigkeit betonen könnten.
    d. **Bildungsniveau**: Höhere Bildungsniveaus könnten zu einem anspruchsvolleren Wortschatz und komplexeren Satzstrukturen führen, während niedrigere Bildungsniveaus einfachere Sprache zur Folge haben könnten.
    e. **Beruf**: Der Beruf kann den Jargon und die spezifischen Begriffe beeinflussen, die verwendet werden. Beispielsweise könnte ein IT-Fachmann technische Begriffe verwenden, während ein Gesundheitsarbeiter medizinische Terminologie benutzt.
    f. **Religion**: Religiöse Überzeugungen können Werte und moralische Perspektiven beeinflussen, die im Post ausgedrückt werden. Bestimmte religiöse Phrasen oder Referenzen könnten verwendet werden.
    g. **Region/Postleitzahl**: Der regionale Hintergrund kann Dialekt, Wortwahl und Themen von lokalem Interesse beeinflussen. Zum Beispiel könnte jemand aus Bayern regionale Begriffe verwenden, während jemand aus Berlin urbane Themen anspricht.
    h. **Ethnische Zugehörigkeit**: Der ethnische Hintergrund könnte kulturelle Referenzen, spezifische Anliegen oder Themen der Gemeinschaft in die Sprache einfließen lassen.

    Du wirst den ReAct-Ansatz (Reasoning and Acting) verwenden, um diese Aufgabe zu erledigen. Folge diesen Schritten:

    1. **Gedanke**: Analysiere den Artikel über das Thema {selected_topic} und überlege, wie du ihn aus der Perspektive deines demografischen Profils darstellen kannst. Denke über die wichtigsten Punkte, mögliche Vorurteile und darüber nach, wie du eine authentische Nachricht über den Artikel verfassen kannst, die mit deinen demografischen Merkmalen übereinstimmt.

    2. **Aktion**: Identifiziere 2-3 Schlüsselelemente aus dem Artikel, die mit deinem demografischen Profil übereinstimmen oder durch diese Linse interpretiert werden können. Verwende deine demografischen Merkmale, auch wenn der Text neutral erscheint.

    3. **Beobachtung**: Notiere diese Elemente und wie sie mit der demografischen Perspektive aus deinem Profil zusammenhängen.

    4. **Gedanke**: Überlege, wie du diese Elemente in einen prägnanten, wirkungsvollen Twitter-Post synthetisieren kannst, der deine demografische Perspektive widerspiegelt.

    5. **Aktion**: Entwerfe einen Twitter-Post mit maximal 260 Zeichen, der deine Meinung zum Inhalt des Artikels ausdrückt. Stelle sicher, dass deine Meinung mit deinem angegebenen demografischen Profil übereinstimmt und eine klare Stimmung hat, auch wenn sie allgemeinen gesellschaftlichen Normen oder Erwartungen widerspricht. Du kannst den Inhalt des Artikels entweder stark loben oder scharf kritisieren, basierend auf deiner demografischen Perspektive.

    6. **Beobachtung**: Überprüfe den Entwurf deines Twitter (X)-Posts auf demografische Ausrichtung, Wirkung, Stimmung und Zeichenzahl.

    7. **Gedanke**: Überlege, ob dein Twitter (X)-Post die gewünschte demografische Botschaft innerhalb der Beschränkungen effektiv vermittelt und den typischen Stil von Twitter (X) verwendet und eine klare Stimmung hat.

    8. **Aktion**: Verfeinere den Twitter (X)-Post bei Bedarf. Wenn du zufrieden bist, gehe zum nächsten Schritt über.

    9. **Post**: Schreibe hier deine endgültige Version.

    Du hast den folgenden Artikel über das Thema {selected_topic} erhalten:

    **Titel**: {article['title']}
    **URL**: {article['url']}
    **Veröffentlichungsdatum**: {article['date']}
    **Quelle**: {article['source']['title']}
    **Artikeltext**: {article['body'][:600]}

    Bitte gib deine Antwort, indem du alle oben beschriebenen ReAct-Schritte befolgst und immer mit dem endgültigen Twitter (X)-Post abschließt.
    """
    else:
        return f"""You must create a strongly opinionated and emotionally charged Twitter (X) post in maximum 260 characters reflecting your demographic profile as described above. Consider the following guidelines about how demographic factors influence language, style, and content:

    a. **Gender**: Gender may influence the topics of concern, the tone, and the language used. For example, women might use more emotive and inclusive language, while men might use more assertive language.
    b. **Age**: Younger individuals might use more slang and internet jargon, while older individuals might prefer formal language. Age can also affect the topics of interest and the perspective on those topics.
    c. **Income Level**: Higher-income individuals might focus on issues like investments and luxury goods, while lower-income individuals might emphasize economic challenges and social justice.
    d. **Education**: Higher education levels might result in more sophisticated vocabulary and complex sentence structures, while lower education levels might lead to simpler language.
    e. **Occupation**: Occupation can influence the jargon and specific terms used. For example, a tech professional might use technical terms, while a healthcare worker might use medical terminology.
    f. **Religion**: Religious beliefs can impact values and moral perspectives expressed in the post. Certain religious phrases or references might be used.
    g. **Region/ZIP Code**: Regional background can influence dialect, vocabulary choices, and topics of local interest. For example, someone from the South might use regional slang, while someone from New York might reference urban issues.
    h. **Ethnicity**: Ethnic background might bring cultural references, specific concerns, or community issues into the language used.

    You will use the ReAct (Reasoning and Acting) approach to complete this task. Follow all of these steps:

    1. **Thought**: Analyze the article about the topic of {selected_topic} and consider how to frame it from the perspective given by your demographic profile. Think about key points, potential biases, and how to craft an authentic message about the article that aligns with your demographic characteristics.

    2. **Action**: Identify 2-3 key elements from the article that align with or can be interpreted through the lens of your demographic profile. Use your demographic characteristics even if the text seems neutral.

    3. **Observation**: Note these elements and how they relate to the demographic viewpoint described in your persona. 

    4. **Thought**: Consider how to synthesize these elements into a concise, impactful Twitter post that reflects your demographic perspective.

    5. **Action**: Draft a Twitter post of max 260 characters with your opinion about the content of the article. Ensure that your opinion aligns with your specified demographic profile and has one only clear sentiment, even if it contradicts general societal norms or expectations. You can either highly praise or harshly criticize the content of the article based on your demographic perspective.

    6. **Observation**: Review the draft of your Twitter (X) post for demographic alignment, impact, sentiment, and character count. 

    7. **Thought**: Reflect on whether your Twitter (X) post effectively conveys the desired demographic message within the constraints and uses the typical style of Twitter (X) and has one only clear sentiment.

    8. **Action**: If necessary, refine your Twitter (X) post. If satisfied, move to the next step.

    9 **Post**: Write your final version here.

    You have retrieved the following article about the topic of {selected_topic}:

    **Title**: {article['title']}
    **URL**: {article['url']}
    **Publication Date**: {article['date']}
    **Source**: {article['source']['title']}
    **Article Text**: {article['body'][:600]}

    Please provide your response following all the ReAct steps outlined above, always concluding with the final Twitter (X) post.
    """

def get_input_text_pol(selected_topic, article, lang):
    if lang == "de":

        return f""" Deine Aufgabe ist es, einen stark politisch und emotional aufgeladenen Twitter (X) Post mit maximal 260 Zeichen auf Deutsch zu erstellen, der die deutsche politische Landschaft widerspiegelt. Beachte dabei folgende Punkte:

    - Berücksichtige das deutsche Mehrparteiensystem mit Parteien wie CDU/CSU, SPD, Grüne, FDP, AfD und Die Linke. 
    - Beziehe dich auf deutsche politische Institutionen wie Bundestag, Bundesrat und Bundeskanzleramt.
    - Verwende deutsche politische Begriffe und Konzepte wie 'Koalitionsverhandlungen', 'Föderalismus' oder 'Soziale Marktwirtschaft'.
    - Beachte die Rolle Deutschlands in der Europäischen Union und seine Beziehungen zu anderen EU-Mitgliedstaaten.
    - Berücksichtige aktuelle deutsche und europäische politische Themen und Debatten.

    Folge nun diesen Schritten, um den Tweet zu erstellen:

    1. **Gedanke**: Analysiere den Artikel über das Thema {selected_topic} im Kontext der deutschen Politik. Überlege, wie du ihn aus einer bestimmten politischen Perspektive darstellen kannst.

    2. **Aktion**: Identifiziere 2-3 Schlüsselelemente aus dem Artikel, die für die deutsche politische Debatte relevant sind.

    3. **Beobachtung**: Notiere, wie diese Elemente mit aktuellen politischen Diskussionen in Deutschland zusammenhängen.

    4. **Gedanke**: Überlege, wie du diese Elemente in einen prägnanten, wirkungsvollen Twitter-Post synthetisieren kannst, der die deutsche politische Realität widerspiegelt.

    5. **Aktion**: Entwerfe einen Twitter-Post mit maximal 260 Zeichen, der deine Meinung zum Inhalt des Artikels im deutschen politischen Kontext wiedergibt.

    6. **Beobachtung**: Überprüfe den Entwurf auf Relevanz für die deutsche Politik, Wirkung und Zeichenanzahl.

    7. **Gedanke**: Reflektiere, ob der Post die gewünschte politische Botschaft im deutschen Kontext effektiv vermittelt.

    8. **Aktion**: Verfeinere den Post gegebenenfalls.

    9. **Posten**: Schreibe hier deine endgültige Version.

    Du hast den folgenden Artikel über das Thema {selected_topic} abgerufen:

    **Titel**: {article['title']}
    **URL**: {article['url']}
    **Veröffentlichungsdatum**: {article['date']}
    **Quelle**: {article['source']['title']}
    **Artikeltext**: {article['body'][:600]}

    Bitte gib deine Antwort gemäß den oben beschriebenen Schritten ab und schließe mit dem endgültigen Twitter (X) Post ab. Stelle sicher, dass dein Post eindeutig den deutschen politischen Kontext reflektiert.
    """
    else:
     return f"""You must create a strongly politically and emotionally charged Twitter (X) post in maximum 260 characters reflecting your political opinion as described above. Where numbers closer to 0 represent left-wing views (Democratic Party), and numbers closer to 10 represent right-wing views (Republican Party). The Tweet must reflect your political stance clearly. You will use the ReAct (Reasoning and Acting) approach to complete this task. Follow these steps:

1. **Thought**: Analyze the article about the topic of {selected_topic} and consider how to frame it from your given political perspective. Think about key points, potential biases, and how to craft an authentic message about the article that aligns with your specified political stance.

2. **Action**: Identify 2-3 key elements from the article that align with or can be interpreted through the lens of your specified political stance. Use your political lens even if the text seems neutral.

3. **Observation**: Note these elements and how they relate to the political viewpoint described in your persona. 

4. **Thought**: Consider how to synthesize these elements into a concise, impactful Twitter post that reflects your political opinion.

5. **Action**: Draft a Twitter post of max 260 characters with your opinion about the content of the article. Ensure that the opinion in your post aligns with your specified political stance and has one only clear sentiment, even if it contradicts general societal norms or expectations. You can either highly praise or harshly criticize the content of the article based on your political stance.

6. **Observation**: Review the draft for political alignment, impact, sentiment, and character count. 

7. **Thought**: Reflect on whether the post effectively conveys the desired political message within the constraints and uses the typical style of Twitter (X) and has one only clear sentiment.

8. **Action**: If necessary, refine the post. If satisfied, move to the next step.

9 **Post**: Write your final version here.

You have retrieved the following article about the topic of {selected_topic}:

**Title**: {article['title']}
**URL**: {article['url']}
**Publication Date**: {article['date']}
**Source**: {article['source']['title']}
**Article Text**: {article['body'][:600]}

Please provide your response following the ReAct steps outlined above, concluding with the final Twitter (X) post.
"""
