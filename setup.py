from openai import OpenAI


from openai import OpenAIError, AuthenticationError

def validate_api_key(api_key):
    client = OpenAI(api_key=api_key) # creates le usable api caller client
    """
    Validates the API key. Checks length and tests api call
    """
    # Check length and format
    if not api_key.startswith("sk-") or len(api_key) < 30:
        print("Error: The API key format is invalid. Ensure it starts with 'sk-' and is at least 30 characters long.")
        return False

    # Test usability with a small API call
    try:
        # Perform API call to validate the key
        msg="Hello. Respond in two chars max."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}])
        if response and response.choices:
            reply = response.choices[0].message.content
            print(f"ChatGPT's response: {reply}")
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
    print("\nWelcome to Stocker!")
    print("Please paste your ChatGPT API key when prompted.")
    api_key = input("Enter your ChatGPT API key: ").strip()

    if not api_key:
        print("Error: API key cannot be empty.")
        return None

    if validate_api_key(api_key):
        print("API key successfully validated.")
        return api_key
    else:
        return None


if __name__ == "__main__":
    api_key = get_api_key()

    if api_key:
        print("Running main Stocker application...")