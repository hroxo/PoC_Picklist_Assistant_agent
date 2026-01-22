import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


class Agent:

    def __init__(self,
                 agent_model: str = 'gemini-3-flash-preview',
                 prompt: str = 'agent/prompt/few_shot.txt'):
        try:
            with open(prompt, 'r') as file:
                prompt = file.read()
        except Exception as e:
            print(f"Error {e}\nVerify path to prompt. Terminating script")
            sys.exit(1)
        self.agent_model = agent_model
        self.prompt = prompt
        self.image: bytes | None = None

        try:
            load_dotenv()
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        except Exception as e:
            print(f"Error {e}\nGemini key missing or invalid.\nExiting...")

    def think(self, image_bytes: bytes) -> str:
        """
        Analyzes an image using the Gemini model to extract inventory data.

        Reads a few-shot prompt from a file, initializes the
        Gemini client using environment variables,
        and sends the provided image bytes
        along with the prompt to the model.

        Args:
            image_bytes (bytes): The raw bytes of the image to be analyzed

        Returns:
            str: The text response from the model, expected to be a JSON string
                containing inventory details, or an error message JSON if the
                model fails to generate text.
        """
        self.image = image_bytes

        client = genai.Client(api_key=self.gemini_api_key)
        response = client.models.generate_content(
            model=self.agent_model,
            contents=[
                types.Part.from_bytes(
                    data=self.image,
                    mime_type='image/png',
                ),
                self.prompt
                ]
            )

        if response.text is None:
            return "{\nError: Model Failed to run correctly\n}"

        return response.text.replace("'", '"')

    def recall(self, recall_prompt: str) -> str:
        """
        Docstring for recall
        """
        try:
            client = genai.Client(api_key=self.gemini_api_key)
            response = client.models.generate_content(
                model=self.agent_model,
                contents=[
                    types.Part.from_bytes(
                        data=self.image,
                        mime_type='image/png',
                    ),
                    recall_prompt
                    ]
                )
        except Exception as e:
            print(f"Error {e}\nTo recall you have to call think prev",
                  "\nExiting...")
            sys.exit(1)

        if response.text is None:
            return "{\nError: Model Failed to run correctly\n}"

        return response.text.replace("'", '"')
