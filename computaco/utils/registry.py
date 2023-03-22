from langchain.llms import OpenAI, OpenAIChat
from langchain.llms.base import BaseLLM

from computils.computils.fns.exponential_backoff import ExponentialBackoff

_rate_limit = ExponentialBackoff(scale=5, max_wait=60)

small_completion_engine: BaseLLM = _rate_limit(
    OpenAI("text-curie-001")
)  # TODO: change to alpaca once it's available
large_completion_engine: BaseLLM = _rate_limit(
    OpenAI("text-davinci-003")
)  # TODO: change to alpaca once it's available
small_chat_engine: BaseLLM = _rate_limit(OpenAIChat(model_name="gpt-3.5-turbo"))
large_chat_engine: BaseLLM = _rate_limit(OpenAIChat(model_name="gpt-4"))
