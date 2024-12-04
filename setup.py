from openai import OpenAI
from openai import OpenAIError, AuthenticationError
from newsapi import NewsApiClient
import time
import subprocess

print("\nRunning Setup.py ↘️")
print("Welcome to Stocker! 📉👁️📈")
time.sleep(2) # for aesthetics

def validate_gpt_key(key):
    client = OpenAI(api_key=key) # creates le usable api caller client
    """
    Validates the API key. Checks length and tests api call
    """
    # Check length and format
    if not key.startswith("sk-") or len(key) < 30:
        print("Error: The API key format is invalid. Ensure it starts with 'sk-' and is at least 30 characters long.")
        return False

    # Test usability with a small API call
    try:
        # Perform API call to validate the key
        msg="Respond in 1 random emoji"
        print("Querying GPT API...")
        time.sleep(1)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}])
        if response and response.choices:
            reply = response.choices[0].message.content
            time.sleep(1)
            print(f"GPT: {reply}")
            return True
    except AuthenticationError:
        print("Error: The API key is invalid or unauthorized.")
        return False
    except OpenAIError as e:
        print(f"Error: Unable to validate API key. Reason: {e}")
        return False

    return False


def get_gpt_key():
    """
    Prompt the user to input their ChatGPT API key and validate it.
    """
    gpt_key = input("Enter your ChatGPT API key: ").strip()

    if not gpt_key:
        print("Error: API key cannot be empty.")
        return None

    if validate_gpt_key(gpt_key):
        print("GPT API key successfully validated ✅")
        return gpt_key
    else:
        return None

def get_newsapi_key():
    """
    Prompt the user to input their NewsAPI key without validation.
    """
    newsapi_key = input("Enter your NewsAPI key: ").strip()
    if not newsapi_key:
        print("Error: NewsAPI key cannot be empty.")
        return None
    return newsapi_key

if __name__ == "__main__":
    gpt_key = get_gpt_key()
    newsapi_key = get_newsapi_key()

    if gpt_key:
        print("Running main Stocker application...🏃‍♂️💨\n")
        subprocess.run(["python", "Stocker.py", gpt_key, newsapi_key])