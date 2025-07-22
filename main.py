import os
from crewai import Agent, Crew, LLM, Task, TaskOutput
from crewai_tools import SerperDevTool
from datetime import date
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from typing import Any, Tuple

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# This is the custom CrewAI Guardrail function
def validate_blog_content(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate blog content meets requirements."""
    try:
        # Check word count
        try:
            word_count = len(result.raw.split())
            print(f"Word count: {word_count}")
            if word_count > 100:
                return (False, "Blog content exceeds 100 words")
        except Exception as wc_error:
            print(f"Error during word count check: {wc_error}")
            return (False, f"Error during word count check: {wc_error}")
        # Additional validation logic goes here
        return (True, result.raw.strip())
    except Exception as e:
        print(f"Unexpected error during validation: {e}")
        return (False, f"Unexpected error during validation: {e}")

# LLM to be used by the Agent
llm = LLM(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Define the Agent with the Serper tool
blog_agent = Agent(
    role="Blog Writer",
    goal="Write blog post",
    backstory="An expert blog writer",
    tools=[SerperDevTool()],
    llm=llm,
    verbose=True
)

# Define the Task with the CrewAI Guardrail
blog_task = Task(
    description="Write a super DETAILED blog post about {prompt} for {year}",
    expected_output="""A properly structured blog post under 100 words.
    Blog format:
    # Title
    ## Subtitle
    Paragraphs...
    """,
    agent=blog_agent,
    markdown=True,
    guardrail=validate_blog_content,  # Add the CrewAI Guardrail function
    max_retries=4  # Set the maximum number of retries
)

# Build the Crew
crew = Crew(
    agents=[blog_agent],
    tasks=[blog_task],
    verbose=True
)

# Launch the Crew with the subject of "Climate Change" in the current calendar year
results = crew.kickoff(
    inputs={
        "prompt": "Climate Change",
        "year": date.today().year
    }
)

# Display the results in the terminal using the "rich" library
def display_results(content: str):
    """Display results with robust Markdown rendering."""
    try:
        # Create console with explicit terminal detection
        console = Console(force_terminal=True, color_system="auto")
        # Clean and prepare the content
        markdown_content = content.strip()
        # Check if content looks like Markdown
        if any(marker in markdown_content for marker in ['#', '**', '*', '`', '[']):
            console.print(Markdown(markdown_content))
        else:
            # If it doesn't look like Markdown, format it nicely
            console.print(f"[bold blue]Results:[/bold blue]")
            console.print(markdown_content)
    except Exception as e:
        print(f"Rich rendering failed: {e}")
        print("Falling back to plain text:")
        print("=" * 50)
        print(content)
        print("=" * 50)

# Display the results
display_results(results.raw)
