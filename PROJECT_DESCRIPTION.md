The AI Research and Article Writing project is an automated system that performs the following tasks:

1. Research Plan Generation:
   - The ResearchAgent uses the OpenAI GPT-3 API to generate a dynamic research plan based on the given topic.
   - The research plan includes the following sections: introduction, background, current state, future developments, and conclusion.
   - The generated research plan is cached to improve performance for repeated topics.

2. Research Execution:
   - The ResearchAgent uses the `duckduckgo-search` package to perform text searches for each subtopic in the research plan.
   - The top 5 search results are extracted as research summaries and saved to a "research.md" file.
   - Asynchronous requests are used to fetch the research results concurrently, improving the overall execution time.
   - Exceptions are handled gracefully, logging any errors that occur during the research process.

3. Article Writing:
   - The WriterAgent reads the research results from the "research.md" file and generates an article based on the content.
   - The article is formatted with a title and the research summaries.
   - The article is saved to an "article.md" file.

4. Image Retrieval:
   - The ImageAgent uses the `duckduckgo-search` package to search for and retrieve the top 5 relevant images for the given topic.
   - The images are downloaded and saved as "image_1.jpg", "image_2.jpg", etc.
   - Asynchronous requests are used to download the images concurrently, improving the overall performance.
   - Exceptions are handled when downloading the images, logging any errors that occur.

5. Iterative Review and Feedback:
   - The EditorAgent orchestrates the entire workflow, coordinating the actions of the ResearchAgent, WriterAgent, and ImageAgent.
   - The EditorAgent reviews the research plan, research results, and article, providing feedback and opportunities for improvement.
   - If the research plan, research results, or article do not meet the specified criteria, the EditorAgent generates feedback and updates the topic accordingly for the next iteration.
   - The iterative process continues until the article is approved or the maximum number of iterations is reached.

6. Progress Tracking and Reporting:
   - The ProgressTracker class is responsible for tracking the progress of each agent's tasks, including the start time, end time, and status.
   - When each task is started and completed, the ProgressTracker logs the relevant information.
   - At the end of the workflow, the ProgressTracker generates a detailed progress report, which is logged using the `logging` module.

7. Exception Handling and Error Logging:
   - The application implements robust exception handling, using try-except blocks to catch and handle specific exceptions, such as OpenAI API errors, `aiohttp` client errors, and file I/O errors.
   - When an exception occurs, the application logs the error message with relevant context to aid in debugging and troubleshooting.

8. Modular and Maintainable Structure:
   - The codebase is organized into separate modules (agents, utils, config) to improve modularity and maintainability.
   - The agents (ResearchAgent, WriterAgent, ImageAgent, EditorAgent) encapsulate the specific functionalities, making the code more modular and reusable.
   - The ProgressTracker and configuration management are handled in separate utility modules, further enhancing the overall structure.

9. Configurability and Customization:
   - The application's configuration, such as API keys and file paths, is managed through environment variables and a dedicated `config.py` module.
   - Users can customize various aspects of the application, including the research plan generation, review criteria, caching settings, and logging configuration.

10. Asynchronous and Concurrent Processing:
    - The application leverages asynchronous programming using `asyncio` and `aiohttp` to perform concurrent tasks, such as fetching research results and downloading images.
    - This approach improves the overall execution time and performance of the application.
