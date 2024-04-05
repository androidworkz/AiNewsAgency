import asyncio
import logging
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.image_agent import ImageAgent
from agents.editor_agent import EditorAgent
from utils.progress_tracker import ProgressTracker
import openai
from config import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
client = openai.Client(api_key=OPENAI_API_KEY)

async def main():
    progress_tracker = ProgressTracker()
    research_agent = ResearchAgent(client)
    writer_agent = WriterAgent()
    image_agent = ImageAgent(client)
    editor_agent = EditorAgent(research_agent, writer_agent, image_agent, progress_tracker)

    topic = "Latest advancements in artificial intelligence"
    await editor_agent.start(topic)


if __name__ == "__main__":
    asyncio.run(main())
