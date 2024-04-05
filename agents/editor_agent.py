import logging
from typing import List
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.image_agent import ImageAgent


class EditorAgent:
    def __init__(self, research_agent: ResearchAgent, writer_agent: WriterAgent, image_agent: ImageAgent,
                 progress_tracker):
        self.research_agent = research_agent
        self.writer_agent = writer_agent
        self.image_agent = image_agent
        self.progress_tracker = progress_tracker

    async def start(self, topic: str, max_iterations: int = 3):
        self.progress_tracker.start_task("EditorAgent", "Start Editing Process")
        iteration = 1
        while iteration <= max_iterations:
            logging.info(f"Starting iteration {iteration}")

            research_plan = await self.research_agent.create_research_plan(topic, self.progress_tracker)

            if self.approve_research_plan(research_plan):
                research_results = await self.research_agent.execute_research(research_plan, self.progress_tracker)

                if self.review_research(research_results):
                    article = self.writer_agent.write_article(research_results, self.progress_tracker)

                    if self.review_article(article, research_results):
                        self.save_article(article, iteration)
                        images = await self.image_agent.retrieve_images(topic, self.progress_tracker)
                        logging.info(f"Iteration {iteration} completed successfully.")
                        break
                    else:
                        feedback = self.generate_article_feedback(article, research_results)
                        logging.info(f"Article needs revision. Feedback: {feedback}")
                        topic = self.update_topic(topic, feedback)
                else:
                    feedback = self.generate_research_feedback(research_results)
                    logging.info(f"More research is needed. Feedback: {feedback}")
                    topic = self.update_topic(topic, feedback)
            else:
                feedback = self.generate_plan_feedback(research_plan)
                logging.info(f"Research plan not approved. Feedback: {feedback}")
                topic = self.update_topic(topic, feedback)

            iteration += 1

        if iteration > max_iterations:
            logging.warning("Maximum iterations reached. Article may not be complete.")

        self.progress_tracker.complete_task("EditorAgent", "Start Editing Process")
        await self.progress_tracker.generate_report()

    def approve_research_plan(self, plan: List[str]) -> bool:
        required_sections = ["introduction", "background", "current_state", "future_developments", "conclusion"]
        return all(section in plan for section in required_sections)

    def review_research(self, research: List[str]) -> bool:
        min_sources = 5
        min_length = 200
        relevant_keywords = ["artificial intelligence", "machine learning", "deep learning", "neural networks"]

        if len(research) < min_sources:
            return False

        for result in research:
            if len(result) < min_length or not any(keyword in result.lower() for keyword in relevant_keywords):
                return False

        return True

    def review_article(self, article: str, research: List[str]) -> bool:
        min_length = 1000
        max_plagiarism_ratio = 0.1

        if len(article) < min_length:
            return False

        article_words = article.lower().split()
        research_words = [word.lower() for result in research for word in result.split()]
        common_words = set(article_words) & set(research_words)
        plagiarism_ratio = len(common_words) / len(article_words)

        if plagiarism_ratio > max_plagiarism_ratio:
            return False

        return True

    def save_article(self, article: str, iteration: int):
        try:
            with open(f"article_iteration_{iteration}.md", "w") as file:
                file.write(article)
        except IOError as e:
            logging.error(f"Error saving article: {e}")
            raise

    def generate_plan_feedback(self, plan: List[str]) -> str:
        if not self.approve_research_plan(plan):
            missing_sections = [section for section in
                                ["introduction", "background", "current_state", "future_developments", "conclusion"] if
                                section not in plan]
            return f"The research plan is missing the following sections: {', '.join(missing_sections)}. Please include them in the next iteration."
        return "The research plan looks good. No further changes needed."

    def generate_research_feedback(self, research: List[str]) -> str:
        if not self.review_research(research):
            if len(research) < 5:
                return "The research results need more sources. Please include at least 5 relevant sources in the next iteration."
            elif any(len(result) < 200 for result in research):
                return "Some research results are too short. Please provide more detailed information for each result."
            else:
                return "The research results should include more relevant keywords related to artificial intelligence. Please focus on topics such as machine learning, deep learning, and neural networks."
        return "The research results are sufficient. No further changes needed."

    def generate_article_feedback(self, article: str, research: List[str]) -> str:
        if not self.review_article(article, research):
            if len(article) < 1000:
                return "The article is too short. Please elaborate on the topic and aim for at least 1000 words."
            else:
                return "The article contains too much plagiarism. Please rephrase the content and ensure it is original."
        return "The article looks good. No further changes needed."

    def update_topic(self, topic: str, feedback: str) -> str:
        if "missing sections" in feedback:
            missing_sections = feedback.split(": ")[1].split(". ")[0]
            return f"{topic} (Focus on adding: {missing_sections})"
        elif "more sources" in feedback:
            return f"{topic} (Include more sources)"
        elif "too short" in feedback:
            return f"{topic} (Provide more detailed information)"
        elif "more relevant keywords" in feedback:
            return f"{topic} (Focus on AI, machine learning, deep learning, neural networks)"
        elif "elaborate" in feedback:
            return f"{topic} (Elaborate on the topic)"
        elif "plagiarism" in feedback:
            return f"{topic} (Rephrase and ensure originality)"
        else:
            return topic
