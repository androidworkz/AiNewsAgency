import openai
import logging
from openai.error import OpenAIError
from config import OPENAI_API_KEY
from duckduckgo_search import DDGS
from cachetools import TTLCache
from typing import List


def write_results_to_file(results: List[str]) -> None:
    try:
        with open("research.md", "w") as file:
            file.write("\n".join(results))
    except IOError as e:
        logging.error(f"Error writing research results to file: {e}")
        raise


async def execute_research(plan: List[str]) -> List[str]:
    results = []
    for topic in plan:
        search_results = DDGS.text(topic, max_results=5)
        summaries = [result["body"] for result in search_results]
        results.extend(summaries)
    return results


def prepare_prompt(topic: str) -> str:
    return f"Create a research plan for the topic: {topic}\n\nPlan:"


def get_plan_from_openai(client: OpenAI, prompt: str) -> List[str]:
    response = client.create_completion(
        model="gpt-3.5-turbo-0125",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None,
        logprobs=None
    )
    plan_text = response['choices'][0]['message']['content'].strip()
    return plan_text.split("\n")


class ResearchAgent:
    def __init__(self, cache_ttl: int = 3600):
        self.openai_api_key = openai_api_key
        self.client = openai.Client(api_key=openai_api_key)
        self.cache = TTLCache(maxsize=100, ttl=cache_ttl)

    async def execute_and_write_research(self, plan: List[str], progress_tracker) -> List[str]:
        progress_tracker.start_task("ResearchAgent", "Execute Research")
        search_results = execute_research(plan)
        write_results_to_file(search_results)
        progress_tracker.complete_task("ResearchAgent", "Execute Research")
        return search_results

    async def create_research_plan(self, topic: str, progress_tracker) -> List[str]:
        progress_tracker.start_task("ResearchAgent", "Create Research Plan")
        if topic in self.cache:
            progress_tracker.complete_task("ResearchAgent", "Create Research Plan")
            return self.cache[topic]
        try:
            prompt = prepare_prompt(topic)
            plan = get_plan_from_openai(self.client, prompt)
            self.cache[topic] = plan
            progress_tracker.complete_task("ResearchAgent", "Create Research Plan")
            return plan
        except OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            raise
