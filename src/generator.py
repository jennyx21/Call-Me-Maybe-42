from src.parse import Definition
from typing import Any
from llm_sdk import Small_LLM_Model
from enum import Enum


def generator(text: str, llm: Small_LLM_Model) -> tuple[str, dict[str, Any]]:


