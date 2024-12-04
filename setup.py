from openai import OpenAI
from openai import OpenAIError, AuthenticationError
import time
import subprocess
import sys

print("\nRunning Setup.py ↘️")
print("Welcome to Stocker! 📉👁️📈")
time.sleep(1.5)  # for aesthetics


def validate_gpt_key(key):
    """
    Validates the GPT API key by checking its length and making a test API call.
    """
    client = OpenAI(api_key=key)  # Creates usable GPT API client
    # Check length and format
    if not key.startswith("sk-") or len(key) < 30:
        print("Error: The API key format is invalid. Ensure it starts with 'sk-' and is at least 30 characters long.")
        return False

    # Test usability with a small API call
    try:
        # Perform API call to validate the key
        msg = "Respond in 1 random emoji"
        print("Querying GPT API...")
        time.sleep(0.25)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}]
        )
        if response and response.choices:
            reply = response.choices[0].message.content
            time.sleep(0.5)
            print(f"GPT: {reply}")
            time.sleep(0.5)
            print("GPT API key successfully validated ✅")
            return True
    except AuthenticationError:
        print("Error: The API key is invalid or unauthorized.")
        return False
    except OpenAIError as e:
        print(f"Error: Unable to validate API key. Reason: {e}")
        return False

    return False


def validate_newsapi_key(key):
    """
    Validates the NewsAPI key by checking its length and format.
    """
    # Check length and format
    if len(key) != 32:  # NewsAPI keys are typically 32 characters long
        print("Error: The NewsAPI key format is invalid. Ensure it is exactly 32 characters long.")
        return False
    time.sleep(0.5)
    print("NewsAPI key format looks valid ✅")
    time.sleep(0.5)
    return True


def get_gpt_key():
    """
    Prompt the user to input their ChatGPT API key and validate it.
    """
    gpt_key = input("Enter your ChatGPT API key: ").strip()

    if not gpt_key:
        print("Error: API key cannot be empty.")
        return None

    if validate_gpt_key(gpt_key):
        return gpt_key
    else:
        return None


def get_newsapi_key():
    """
    Prompt the user to input their NewsAPI key and validate it.
    """
    newsapi_key = input("Enter your NewsAPI key: ").strip()
    time.sleep(0.5)

    if not newsapi_key:
        print("Error: NewsAPI key cannot be empty.")
        return None

    if validate_newsapi_key(newsapi_key):
        return newsapi_key
    else:
        return None


if __name__ == "__main__":
    # Check for command-line arguments
    gpt_key = sys.argv[1] if len(sys.argv) > 1 else None
    newsapi_key = sys.argv[2] if len(sys.argv) > 2 else None

    # Validate GPT key only once
    if not gpt_key:
        gpt_key = get_gpt_key()
    else:
        if not validate_gpt_key(gpt_key):
            print("Invalid GPT API key provided via command-line argument. Exiting...")
            sys.exit(1)

    # Validate NewsAPI key only once
    if not newsapi_key:
        newsapi_key = get_newsapi_key()
    else:
        if not validate_newsapi_key(newsapi_key):
            print("Invalid NewsAPI key provided via command-line argument. Exiting...")
            sys.exit(1)

    # Ensure both keys are available before proceeding
    if gpt_key and newsapi_key:
        print("Running main Stocker application...🏃‍♂️💨\n")
        time.sleep(1)
        subprocess.run(["python", "Stocker.py", gpt_key, newsapi_key])