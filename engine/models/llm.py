import os
from typing import Optional
from langchain_openai import ChatOpenAI
from engine.core.configs import Config

class LLMClient:
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        temperature: float = 0.7,
    ):
        self.model = model or Config.MODEL
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.temperature = temperature
        self._client = None
    
    @property
    def client(self) -> ChatOpenAI:
        if self._client is None:
            base_url = "https://openrouter.ai/api/v1"
            
            self._client = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                base_url=base_url,
                temperature=self.temperature,
            )
        return self._client
    
    def invoke(self, messages: list, **kwargs):
        return self.client.invoke(messages, **kwargs)
    
    def stream(self, messages: list, **kwargs):
        return self.client.stream(messages, **kwargs)
    
    @classmethod
    def from_env(cls, model: str = None, temperature: float = 0.7):
        return cls(model=model, temperature=temperature)