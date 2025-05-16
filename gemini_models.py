import google.generativeai as genai

# from dotenv import load_dotenv # No longer needed
# import os # No longer needed for getenv
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Directly Hardcoded API Key ---
# !!! WARNING: Hardcoding API keys is a security risk. !!!
# !!! Consider using environment variables or a .env file for production or shared code. !!!
HARDCODED_API_KEY = "GEMINI_API_KEY"  # Replace with your actual key if different
# --- End Hardcoded API Key ---


def list_models():
    """Lists available Gemini models and checks for generateContent support."""
    try:
        api_key = HARDCODED_API_KEY

        if not api_key:
            # This case should ideally not be hit if HARDCODED_API_KEY is set
            logging.error(
                "API key is not set in the script. Please edit the HARDCODED_API_KEY variable."
            )
            return

        # Check if the key is the placeholder
        if (
            api_key == "GEMINI_API_KEY"
            and api_key.startswith("AIzaSy")
            and len(api_key) < 40
        ):
            pass  # Allow the provided key, assuming it's the one to test
        elif "your_actual_api_key_here" in api_key or not api_key.startswith("AIzaSy"):
            logging.warning(
                "The hardcoded API key looks like a placeholder or is invalid. Please replace HARDCODED_API_KEY with your actual Gemini API key in the script."
            )
            # Optionally, you could return here if you don't want to proceed with a suspected placeholder
            # return

        genai.configure(api_key=api_key)
        logging.info("Successfully configured with API key.")

        print("\nAvailable Gemini Models:")
        model_count = 0
        for model in genai.list_models():
            model_count += 1
            # Check if the model supports the 'generateContent' method
            # The user's apitest.py was trying 'gemini-pro' which is often 'models/gemini-pro'
            # For listing, we just show the names and if they support generate content
            if "generateContent" in model.supported_generation_methods:
                print(f"  - {model.name} (supports generateContent)")
            else:
                print(f"  - {model.name} (does NOT support generateContent)")

        if model_count == 0:
            logging.warning(
                "No models were returned. This might indicate an issue with the API key (e.g., permissions) or the API service."
            )
        else:
            logging.info(f"Found {model_count} models.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(
            "Ensure your API_KEY is valid and the Google Generative AI API is enabled for your project."
        )


if __name__ == "__main__":
    list_models()
