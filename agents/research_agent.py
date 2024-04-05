import openai
import logging
from openai import OpenAI
from duckduckgo_search import DDGS
from cachetools import TTLCache
from typing import List
from main import client

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


def get_plan_from_openai(prompt: str) -> List[str]:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            prompt=prompt,
            temperature=0.7,
            max_tokens=200,
            n=1,
            stop=None,
            logprobs=None
        )
        plan_text = response['choices'][0]['message']['content'].strip()
        return plan_text.split("\n")
    except openai.APIConnectionError as e:
        logging.error("The server could not be reached")
        logging.error(e.__cause__)
        raise
    except openai.RateLimitError as e:
        logging.error("A 429 status code was received; we should back off a bit.")
        raise
    except openai.APIStatusError as e:
        logging.error("Another non-200-range status code was received")
        logging.error(f"Status code: {e.status_code}")
        logging.error(f"Response: {e.response}")
        raise
    except openai.APIError as e:
        logging.error("An error occurred with the OpenAI API")
        logging.error(e)
        raise


class ResearchAgent:
    def __init__(self, cache_ttl: int = 3600):
        self.client = client
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
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            raise
