from elevenlabs_unleashed.account import create_account
from elevenlabs_unleashed.manager import ELUAccountManager
from elevenlabs import generate, set_api_key, play, api


# ----------------------------- Create an account ---------------------------- #
username, password, api_key = create_account()


# ------------------------- Automatic API key renewal ------------------------ #
eluac = ELUAccountManager(set_api_key, nb_accounts= 2) # Creates a queue of API keys
eluac.next() # First call will block the thread until keys are generated, and call set_api_key

def speak(self, message: str):
    try:
        audio = generate(
            text=message,
            voice="Josh", # I like this one
            model="eleven_multilingual_v1"
        )
    except elevenlabs.api.error.RateLimitError as e:
        print("[ElevenLabs] Maximum number of requests reached. Getting a new API key...")
        eluac.next() # Uses next API key in queue, should be instant as nb_accounts > 1, and will generate a new key in a background thread.
        speak(message)
        return

    print("[ElevenLabs] Starting the stream...")
    play(audio)


from elevenlabs_unleashed.tts import UnleashedTTS

tts = UnleashedTTS(nb_accounts=2, create_accounts_threads=2)
"""
Will automatically generate 2 accounts in 2 threads. Takes a few seconds.
"""

tts.speak("Hello world!", voice="Josh", model="eleven_multilingual_v1")