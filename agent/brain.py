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
            exit
        self.agent_model = agent_model
        self.prompt = prompt

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
        load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model=self.agent_model,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/png',
                ),
                self.prompt
                ]
            )

        if response.text is None:
            return "{\nError: Model Failed to run correctly\n}"

        return response.text.replace("'", '"')
