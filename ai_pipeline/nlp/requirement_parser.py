import spacy

class RequirementParser:
    """
    Parses a natural language user story to extract key entities.
    This is a simplified PoC parser.
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading 'en_core_web_sm' model. This may take a moment.")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def parse_user_story(self, text: str) -> dict:
        """
        Extracts Actor, Action, and Object from a user story.
        Example: "As a registered user, I want to add a product to the cart."
        """
        doc = self.nlp(text)
        
        actor = "user" # Default
        action = None
        main_object = None

        # Simple rule-based extraction
        for token in doc:
            if token.dep_ == "nsubj" and "user" in token.text.lower():
                actor = token.text
            if token.pos_ == "VERB":
                action = token.lemma_ # Use lemma for consistency (e.g., adds -> add)
            if token.dep_ == "dobj" and token.pos_ == "NOUN":
                main_object = token.text
        
        if not action or not main_object:
            print("Warning: Could not reliably parse action and object. Using defaults.")
            return {
                "actor": "user",
                "action": "add_to_cart",
                "object": "product"
            }
            
        return {
            "actor": actor,
            "action": f"{action}_{main_object}", # e.g., "add_product"
            "object": main_object
        }