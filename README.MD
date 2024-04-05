# AI-Powered Research and Article Writing

This application is an AI-powered system that automates the process of researching a given topic, writing an article based on the research, and retrieving relevant images.

## Features

- Generates a dynamic research plan using the OpenAI GPT-3 API
- Executes the research by performing text searches using the `duckduckgo-search` package
- Writes an article based on the research results
- Retrieves relevant images using the `duckduckgo-search` package
- Provides an iterative process for reviewing and improving the research plan, research results, and article
- Tracks the progress of each agent (ResearchAgent, WriterAgent, ImageAgent, EditorAgent) and generates detailed reports
- Handles exceptions and errors gracefully

## Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - `aiohttp`
  - `python-dotenv`
  - `openai`
  - `cachetools`
  - `duckduckgo-search`

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-research-and-writing.git
```
2. navigate to the project directory:
```bash
cd ai-research-and-writing
```
3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
5. 5. Set the environment variables:

- Create a `.env` file in the project directory.
- Add the following variables to the `.env` file:
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```
- Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

To run the application, execute the following command:
```bash
python main.py
```
The application will start the research and article writing process for the topic "Latest advancements in artificial intelligence". You can modify the topic by changing the `topic` variable in the `main` function in the `main.py` file.

As the application runs, it will generate progress reports that include the status, duration, and completion of each agent's tasks. These reports will be logged using the `logging` module.

The final article will be saved in the `article_iteration_1.md` file, and any retrieved images will be saved as `image_1.jpg`, `image_2.jpg`, etc.

## Customization

You can customize the application by modifying the following:

- **Research Plan Generation**: Adjust the parameters in the `create_research_plan` method of the `ResearchAgent` class to customize the research plan generation.
- **Review Criteria**: Modify the review methods (`approve_research_plan`, `review_research`, `review_article`) in the `EditorAgent` class to change the criteria for approving the research plan, research results, and article.
- **Caching and Performance**: Adjust the `cache_ttl` parameter in the agent constructors to change the time-to-live for the caching mechanism.
- **Logging Configuration**: Update the logging configuration in the `main.py` file to customize the log format, log levels, and logging destinations.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).