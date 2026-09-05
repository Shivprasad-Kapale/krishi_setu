"""
Dynamic Deep Translator Module using deep-translator with robust rate-limit fallback
"""

from deep_translator import GoogleTranslator
import streamlit as st
import time

@st.cache_data(show_spinner=False)
def translate_text(text, target_lang="mr"):
    """
    Translates text dynamically using GoogleTranslator with caching and fallback.
    Target lang: 'mr' for Marathi, 'hi' for Hindi, 'en' for English.
    """
    if target_lang == "en" or not text or not str(text).strip():
        return text
        
    try:
        # Use GoogleTranslator with a small pause or clean retry
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(str(text))
        return translated if translated else text
    except Exception:
        # Fallback to original text if Google rate limits or blocks requests
        return text

