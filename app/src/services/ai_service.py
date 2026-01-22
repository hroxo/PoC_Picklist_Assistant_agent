from google import genai
from google.genai import types
from app.src.config.settings import settings


class AIService:
    """
    Service for interacting with the Google Gemini AI model.
    """

    def __init__(self,
                 model_name: str = settings.AGENT_MODEL,
                 prompt_path: str = settings.PROMPT_PATH):
        """
        Initializes the AI Service.

        Args:
            model_name: The name of the Gemini model to use.
            prompt_path: Path to the text file containing the prompt.
        """
        self.model_name = model_name
        self.api_key = settings.GEMINI_API_KEY
        self.prompt = self._load_prompt(prompt_path)
        self.last_image_bytes = None

        if not self.api_key:
            print("Error: Gemini API key missing.")

    def _load_prompt(self, path: str) -> str:
        """
        Loads the prompt text from a file.

        Args:
            path: Path to the prompt file.

        Returns:
            The content of the prompt file, or empty string on error.
        """
        if not path:
            return ""
        try:
            with open(path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error loading prompt from {path}: {e}")
            return ""

    def analyze_image(self, image_bytes: bytes) -> str:
        """
        Analyzes an image to extract inventory data.

        Args:
            image_bytes: The image data in bytes.

        Returns:
            The model's response as a JSON string.
        """
        self.last_image_bytes = image_bytes

        if not self.api_key:
            return '{"Error": "API Key missing"}'

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type='image/png',
                    ),
                    self.prompt
                ]
            )

            if response.text is None:
                return '{"Error": "Model Failed to run correctly"}'

            return response.text.replace("'", '"')
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            return '{"Error": "Exception during analysis"}'

    def refine_analysis(self, refinement_prompt: str) -> str:
        """
        Refines the previous analysis with a new prompt.

        Args:
            refinement_prompt: The prompt to send for refinement.

        Returns:
            The model's refined response.
        """
        if self.last_image_bytes is None:
            return '{"Error": "No image to refine analysis for"}'

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(
                        data=self.last_image_bytes,
                        mime_type='image/png',
                    ),
                    refinement_prompt
                ]
            )

            if response.text is None:
                return '{"Error": "Model Failed to run correctly"}'

            return response.text.replace("'", '"')
        except Exception as e:
            print(f"Error in refine_analysis: {e}")
            return '{"Error": "Exception during refinement"}'
