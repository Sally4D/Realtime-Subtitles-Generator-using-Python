import argostranslate.package
import argostranslate.translate
from transformers import MarianMTModel, MarianTokenizer
import threading


# --- Base Translator Class ---
class BaseTranslator:
    """A base class for all translation backends."""

    def __init__(self, from_lang_name, to_lang_name, status_callback=None):
        self.from_lang_name = from_lang_name
        self.to_lang_name = to_lang_name
        self.status_callback = status_callback
        self.is_ready = False

    def translate(self, text):
        """Translates a given text."""
        raise NotImplementedError

    def check_and_install_model(self):
        """Checks if the required model is installed and downloads it if not."""
        pass

    def _update_status(self, message, color="gray"):
        if self.status_callback:
            self.status_callback(message, color)


class ArgosTranslator(BaseTranslator):
    """Translator using the Argos Translate library (offline)."""

    def __init__(self, from_lang_name, to_lang_name, status_callback=None):
        super().__init__(from_lang_name, to_lang_name, status_callback)
        self.translator = None
        self.from_lang = None
        self.to_lang = None
        self.check_model()

    def check_model(self):
        try:
            installed_languages = argostranslate.translate.get_installed_languages()
            self.from_lang = next((lang for lang in installed_languages if lang.name == self.from_lang_name), None)
            self.to_lang = next((lang for lang in installed_languages if lang.name == self.to_lang_name), None)

            if self.from_lang and self.to_lang:
                self.translator = self.from_lang.get_translation(self.to_lang)
                if self.translator:
                    self._update_status(f"Argos model for {self.from_lang_name} -> {self.to_lang_name} found.", "green")
                    self.is_ready = True
                else:
                    # Languages are installed, but the specific translation isn't
                    self._update_status(
                        f"Argos translation for {self.from_lang_name} -> {self.to_lang_name} not found. Please install from Settings.",
                        "orange")
                    self.is_ready = False
            else:
                # One or both languages are not installed
                self._update_status(
                    f"Argos language model for '{self.from_lang_name}' or '{self.to_lang_name}' not installed.",
                    "orange")
                self.is_ready = False

        except Exception as e:
            self._update_status(f"Error checking Argos model: {e}", "red")
            self.is_ready = False

    def translate(self, text):
        if not self.is_ready or not self.translator:
            return f"[No Argos Model] {text}"
        try:
            return self.translator.translate(text)
        except Exception as e:
            print(f"Argos translation error: {e}")
            return f"[Translation Error] {text}"


class MarianTranslator(BaseTranslator):
    """Translator using Hugging Face MarianMT models (offline)."""
    LANG_CODE_MAP = {
        "English": "en", "French": "fr", "German": "de", "Spanish": "es",
        "Russian": "ru", "Chinese": "zh", "Italian": "it", "Portuguese": "pt",
        "Dutch": "nl", "Japanese": "jap", "Arabic": "ar", "Hindi": "hi",
    }

    def __init__(self, from_lang_name, to_lang_name, status_callback=None):
        super().__init__(from_lang_name, to_lang_name, status_callback)
        self.model = None
        self.tokenizer = None
        self.model_name = None
        self.check_model()

    def check_model(self):
        from_code = self.LANG_CODE_MAP.get(self.from_lang_name)
        to_code = self.LANG_CODE_MAP.get(self.to_lang_name)

        if not from_code or not to_code:
            self._update_status(f"MarianMT does not support {self.from_lang_name} or {self.to_lang_name}.", "red")
            self.is_ready = False
            return

        self.model_name = f'Helsinki-NLP/opus-mt-{from_code}-{to_code}'
        self._update_status(f"Checking for MarianMT model: {self.model_name}...", "gray")

        try:
            # from_pretrained checks local cache first. This avoids re-downloading.
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = MarianMTModel.from_pretrained(self.model_name)
            self._update_status(f"MarianMT model '{self.model_name}' is ready.", "green")
            self.is_ready = True
        except Exception:
            self._update_status(f"Model '{self.model_name}' not found. Download from Settings.", "orange")
            self.is_ready = False

    def translate(self, text):
        if not self.is_ready or not self.model or not self.tokenizer:
            return f"[No MarianMT Model] {text}"

        try:
            tokenized_text = self.tokenizer(text, return_tensors="pt", padding=True)
            translated_tokens = self.model.generate(**tokenized_text)
            return self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        except Exception as e:
            print(f"MarianMT translation error: {e}")
            return f"[MarianMT Error] {text}"


def get_translator(settings, status_callback=None):
    """Factory function to get the correct translator instance."""
    if not settings.get("translation_enabled"):
        return None

    backend = settings.get("translation_backend", "ArgosTranslate")
    from_lang = settings.get("language", "English").split(" ")[0]
    to_lang = settings.get("translation_target_language", "Spanish")

    if backend == "ArgosTranslate":
        return ArgosTranslator(from_lang, to_lang, status_callback)
    elif backend == "MarianMT":
        return MarianTranslator(from_lang, to_lang, status_callback)

    return None


def get_available_argos_languages():
    """Helper to get a list of all unique language names from Argos packages."""
    try:
        argostranslate.package.update_package_index()
        packages = argostranslate.package.get_available_packages()
        lang_names = set()
        for pkg in packages:
            lang_names.add(pkg.from_name)
            lang_names.add(pkg.to_name)
        return sorted(list(lang_names))
    except Exception as e:
        print(f"Could not fetch Argos language list: {e}")
        return ["English", "Spanish", "French", "German"]  # Fallback