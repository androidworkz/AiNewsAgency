import logging
from typing import List


class WriterAgent:
    def __init__(self, research_file: str = "research.md", article_file: str = "article.md"):
        self.research_file = research_file
        self.article_file = article_file

    def write_article(self, research_results: List[str], progress_tracker) -> str:
        progress_tracker.start_task("WriterAgent", "Write Article")

        try:
            with open(self.research_file, "r") as file:
                research_content = file.read()

            article = f"# Article on Latest Advancements in Artificial Intelligence\n\n{research_content}"

            with open(self.article_file, "w") as file:
                file.write(article)

            progress_tracker.complete_task("WriterAgent", "Write Article")
            return article
        except IOError as e:
            logging.error(f"Error reading research file or writing article: {e}")
            raise
