from agno.agent import Agent
from agno.team import Team, TeamMode
from agno.models.groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.agents.tools import search_library

def build_research_team() -> Team:
    """Create exactly three collaborating agents coordinated by an Agno Team."""
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to your .env file.")

    model = Groq(id=GROQ_MODEL, api_key=GROQ_API_KEY)

    query_analyzer = Agent(
        name="Query Analyzer",
        role="Classify the user's research query and identify focused research questions.",
        model=model,
        instructions=[
            "Classify the research domain.",
            "Extract key concepts, entities, and constraints.",
            "Turn the request into concise, targeted research questions.",
            "Do not answer beyond the analysis task.",
        ],
    )

    research_agent = Agent(
        name="Research Agent",
        role="Find evidence in the provided local research library.",
        model=model,
        tools=[search_library],
        instructions=[
            "Use the search_library tool to look for relevant evidence.",
            "Report the exact source titles returned by the tool.",
            "Separate evidence from interpretation and state when the library is insufficient.",
            "Never invent sources, quotations, statistics, or citations.",
        ],
    )

    answer_reviewer = Agent(
        name="Answer Reviewer",
        role="Review evidence and prepare a careful, structured final research response.",
        model=model,
        instructions=[
            "Check each material claim against the research agent's evidence.",
            "Remove unsupported claims and disclose gaps or uncertainty.",
            "Provide a concise structured answer and list consulted source titles.",
            "Do not claim that sources were consulted if no source was returned.",
        ],
    )

    return Team(
        name="Research Analyst Team",
        mode=TeamMode.coordinate,
        model=model,
        members=[query_analyzer, research_agent, answer_reviewer],
        instructions=[
            "Coordinate the three specialist agents in sequence: analyze, research, review.",
            "Return a structured, evidence-aware research answer.",
            "Use only the local library evidence for source-backed claims.",
        ],
    )
