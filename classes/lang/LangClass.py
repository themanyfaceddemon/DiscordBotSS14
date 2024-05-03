import toml


class LanguageManager:
    """
    A class for managing language files and retrieving localized strings.

    Attributes:
        lang (str): The selected language code.
    """

    def __init__(self) -> None:
        """
        Initializes the LanguageManager with the specified language.
        """
        with open("config.toml", "r") as file:
            config = toml.load(file)

        with open(f"lang/{config['bot']['lang']}.toml", "r") as file:
            # Load the contents of the TOML file into a dictionary
            self.lang = toml.load(file)
    
    def loc(self, section: str, key: str) -> str:
        """
        Retrieve a localized string from the language file.

        Args:
            section (str): The section name in the language file.
                           (e.g., 'general', 'errors', 'messages', etc.)
            key (str): The key corresponding to the desired string within the section.

        Returns:
            str: The localized string corresponding to the specified section and key.
        """
        # Access the specified section and retrieve the localized string using the key
        return self.lang[section][key]
