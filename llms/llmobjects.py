import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatDeepInfra
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import DeepInfra
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from langchain_community.chat_models import ChatOllama
from langchain_nvidia_ai_endpoints.chat_models import ChatNVIDIA


class LLMObject:
    model_mapping = {
        "ChatOpenAI": ChatOpenAI,
        "ChatAnthropic": ChatAnthropic,
        "ChatGroq": ChatGroq,
        "ChatDeepInfra": ChatDeepInfra,
        "ChatCohere": ChatCohere,
        "ChatGoogleGenerativeAI": ChatGoogleGenerativeAI,
        "ChatOllama": ChatOllama,
        "ChatNVIDIA": ChatNVIDIA,
    }

    max_token_param_mapping = {
        "ChatOpenAI": "max_tokens",
        "ChatAnthropic": "max_tokens",
        "ChatGroq": "max_tokens",
        "ChatDeepInfra": "max_tokens",
        "ChatCohere": "max_tokens",
        "ChatGoogleGenerativeAI": "max_output_tokens",
        "ChatOllama": "max_tokens",
        "ChatNVIDIA": "max_tokens",
    }

    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        model_class, model_specifier = model_name.split(":", 1)
        self.model_name = model_name
        if model_class in self.model_mapping:
            common_params = {
                "model": model_specifier,
                "temperature": kwargs.get("temperature", 0.7),
                "streaming": kwargs.get("streaming", False),
            }

            # Handle max_tokens separately due to the mapping
            max_tokens = kwargs.get("max_tokens", 256)
            max_tokens_param = self.max_token_param_mapping.get(model_class)
            if max_tokens_param:
                common_params[max_tokens_param] = max_tokens

            api_key_param = self.get_api_key_param(model_class)
            if api_key_param:
                common_params[api_key_param] = api_key or os.getenv(
                    api_key_param.upper()
                )

            # Additional parameters like repetition_penalty, max_new_tokens, top_p
            additional_params = [
                "repetition_penalty",
                "max_new_tokens",
                "top_p",
                "base_url",
                "seed",
                "stop",
            ]
            for param in additional_params:
                if param in kwargs:
                    common_params[param] = kwargs[param]

            self.llm_instance = self.model_mapping[model_class](**common_params)
        else:
            raise ValueError(f"Unsupported model class: {model_class}")

    def get_api_key_param(self, model_class: str) -> Optional[str]:
        api_key_params = {
            "ChatOpenAI": "openai_api_key",
            "ChatAnthropic": "anthropic_api_key",
            "ChatGroq": "groq_api_key",
            "ChatDeepInfra": "deepinfra_api_token",
            "ChatCohere": "cohere_api_key",
            "ChatGoogleGenerativeAI": "google_api_key",
            "ChatOllama": None,  # Ollama may not require an API key
            "ChatNVIDIA": "nvidia_api_key",
        }
        return api_key_params.get(model_class)

    def send_message(self, message: str) -> str:
        try:
            if self.llm_instance.streaming:
                response_chunks = []
                for chunk in self.llm_instance._stream([HumanMessage(content=message)]):
                    response_chunks.append(chunk.message.content)
                return "".join(response_chunks)
            else:
                return self.llm_instance.invoke([HumanMessage(content=message)])
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def testsend_message(self, message: str) -> str:
        if self.llm_instance.streaming:
            response_chunks = []
            for chunk in self.llm_instance._stream([HumanMessage(content=message)]):
                response_chunks.append(chunk.message.content)
            return "".join(response_chunks)
        else:
            return self.llm_instance.invoke([HumanMessage(content=message)])
