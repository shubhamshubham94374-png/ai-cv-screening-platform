import spacy

nlp = spacy.load("en_core_web_sm")

def extract_name(text: str) -> str | None:
    first_chunk = "\n".join(text.strip().split("\n")[:5])

    doc = nlp(first_chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Take only the first line of the matched entity,
            # in case spaCy's span accidentally crosses a line break
            name = ent.text.split("\n")[0].strip()
            return name

    return None