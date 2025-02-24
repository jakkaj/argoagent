import os
import traceback
from typing import Optional
from openai import OpenAI

class LLMHelper:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name

    def send(
        self,
        messages: list = None, 
        temperature: float = 0.7,          
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Send text to OpenAI model and get the response.
        
        Args:
            text: The input text to send to the model
            model: The OpenAI model to use (default: gpt-4)
            temperature: Controls randomness in the output (0.0-1.0)
            max_tokens: Maximum number of tokens in the response (optional)
        
        Returns:
            The model's response as a string
        
        Raises:
            Exception: If OPENAI_API_KEY is not set or if the API call fails
        """
        # Load API key from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OPENAI_API_KEY not found in .env file")
        client = OpenAI(api_key=api_key)

        try:
            if self.model_name.startswith("gpt"):
                # For chat models like GPT-4, GPT-3.5
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            else:
                # For completion models
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages                                 
                )
                return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}\n{traceback.format_exc()}")