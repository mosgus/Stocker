from openai import OpenAI
from openai import OpenAIError, AuthenticationError
import time

print("\nRunning Setup.py ↘️")

def validate_api_key(key):
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
        msg="Say 'yo' or 'hi'"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}])
        if response and response.choices:
            reply = response.choices[0].message.content
            print(f"GPT: {reply}")
            return True
    except AuthenticationError:
        print("Error: The API key is invalid or unauthorized.")
        return False
    except OpenAIError as e:
        print(f"Error: Unable to validate API key. Reason: {e}")
        return False

    return False


def get_api_key():
    """
    Prompt the user to input their ChatGPT API key and validate it.
    """
    print("Welcome to Stocker! 📉👁️📈")
    time.sleep(2) # for aesthetics
    key = input("Enter your ChatGPT API key: ").strip()

    if not key:
        print("Error: API key cannot be empty.")
        return None

    if validate_api_key(key):
        print("✅API key successfully validated.")
        return key
    else:
        return None

import subprocess

if __name__ == "__main__":
    key = get_api_key()

    if key:
        print("Running main Stocker application...🏃‍♂️💨\n")
        subprocess.run(["python", "Stocker.py", key])