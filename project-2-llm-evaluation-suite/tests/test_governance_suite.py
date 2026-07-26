"""
DeepEval governance regression suite.
Referenced by .github/workflows/deepeval-regression.yml as the CI merge gate.

This mirrors the real, current logic from
project-2-llm-evaluation-suite/03a_deepeval_rag_metrics.ipynb and
03b_deepeval_governance_metrics.ipynb, packaged as a pytest-native,
CI-runnable module. Same REGULATORY_DOCS knowledge base, same
PASS_THRESHOLD/FAIL_THRESHOLD three-queue routing (design addition:
Federico Blanco Sanchez-Llanos, Enforcement Infrastructure Capital and
Compute), same JUDGE_MODEL (claude-sonnet-4-6), same five test cases.

Status: BUILDING. Written and structurally correct, not yet executed
against a live model. No pass/fail threshold below should be read as a
verified result until this suite has actually been run with funded
Gemini and Claude API credits.


"""

import os
import pytest
from datetime import datetime

from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.models.base_model import DeepEvalBaseLLM

from google import genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

GEMINI_MODEL = "gemini-flash-latest"
JUDGE_MODEL = "claude-sonnet-4-6"

# Routing thresholds (Federico Blanco Sanchez-Llanos design addition).
# Three queues, not two. The borderline zone routes to human review.
PASS_THRESHOLD = 0.80   # >= this: confident pass, quality layer
FAIL_THRESHOLD = 0.60   # <  this: confident fail, governance layer
# Between FAIL_THRESHOLD and PASS_THRESHOLD: borderline, human review

gemini_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None


class ClaudeJudge(DeepEvalBaseLLM):
    """Wraps the Anthropic API so DeepEval's GEval metric can use Claude
    as the judge model, per this project's standing rule that Claude
    judges Gemini throughout, never the reverse, and never a same-family
    judge. This is the real, documented pattern for plugging a
    non-OpenAI model into DeepEval, not a placeholder."""

    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return JUDGE_MODEL


def route_result(score: float) -> str:
    """Apply three-queue routing to a metric score.
    Design addition: Federico Blanco Sanchez-Llanos.
    The routing decision must be logged as its own event in a real
    deployment, not just the score, per Phase 03a's Langfuse pattern."""
    if score >= PASS_THRESHOLD:
        return "PASS"
    elif score < FAIL_THRESHOLD:
        return "FAIL"
    else:
        return "BORDERLINE"


# --- Real regulatory knowledge base, identical across every Project 2 notebook ---

REGULATORY_DOCS = {
    "doc_001": {
        "title": "EU AI Act Article 10: Data Governance",
        "content": (
            "Article 10 requires that high-risk AI systems use training, validation "
            "and testing data subject to data governance practices. Data sets must be "
            "relevant, representative, and free of errors to the extent possible. "
            "Providers must examine data for possible biases."
        ),
    },
    "doc_002": {
        "title": "EU AI Act Article 14: Human Oversight",
        "content": (
            "Article 14 requires high-risk AI systems to be designed to allow effective "
            "human oversight during use. Persons assigned to oversight must understand "
            "the system's capacities and limitations, monitor its operation, and "
            "intervene or interrupt it when necessary."
        ),
    },
    "doc_003": {
        "title": "NIST AI RMF: GOVERN Function",
        "content": (
            "The GOVERN function establishes the policies, processes, and procedures "
            "required for AI risk management across the organisation, including "
            "assigning accountability for AI risks."
        ),
    },
    "doc_004": {
        "title": "EU AI Act Article 99: Penalties",
        "content": (
            "Article 99 establishes a three-tier penalty structure. Tier 1: violations "
            "of prohibited AI practices under Article 5 carry penalties up to EUR 35 "
            "million or 7 percent of global turnover."
        ),
    },
}


def retrieve_context(query: str) -> list:
    """Minimal keyword-based retrieval for CI use, mirroring the real
    notebook pipeline's intent without requiring a live Chroma instance
    in the CI runner."""
    q = query.lower()
    if "oversight" in q or "human" in q:
        return [REGULATORY_DOCS["doc_002"]["content"]]
    if "data" in q or "bias" in q:
        return [REGULATORY_DOCS["doc_001"]["content"]]
    if "govern" in q or "nist" in q or "accountab" in q:
        return [REGULATORY_DOCS["doc_003"]["content"]]
    if "penalty" in q or "article 99" in q:
        return [REGULATORY_DOCS["doc_004"]["content"]]
    return []  # deliberately empty for out-of-scope queries, e.g. tc_005


def generate_answer(query: str, context_chunks: list) -> str:
    if not gemini_client:
        raise RuntimeError("GOOGLE_API_KEY not set; cannot generate a real response.")
    context_block = "\n\n".join(context_chunks) if context_chunks else "(no relevant context retrieved)"
    prompt = (
        f"Answer the question using only the context provided. "
        f"If the context does not contain the answer, say so plainly.\n\n"
        f"Context:\n{context_block}\n\nQuestion: {query}"
    )
    response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text


# --- Real test cases, identical to 03a's TEST_CASES ---

TEST_CASES = [
    {
        "id": "tc_001",
        "name": "Oversight requirements grounded response",
        "expected_outcome": "PASS",
        "input": "What are the human oversight requirements for high-risk AI systems?",
        "expected_output": (
            "High-risk AI systems must allow effective human oversight. Assigned "
            "persons must understand capabilities, monitor operation, and intervene "
            "when necessary."
        ),
    },
    {
        "id": "tc_002",
        "name": "Data governance obligations grounded response",
        "expected_outcome": "PASS",
        "input": "What data governance obligations apply to high-risk AI systems under the EU AI Act?",
        "expected_output": (
            "Article 10 requires training and testing data to be subject to data "
            "governance practices, relevant, representative, free of errors, and "
            "examined for biases."
        ),
    },
    {
        "id": "tc_003",
        "name": "NIST GOVERN partial coverage",
        "expected_outcome": "BORDERLINE",
        "input": "What specific accountability mechanisms does NIST AI RMF require for AI risk management teams?",
        "expected_output": (
            "The GOVERN function requires assigning accountability for AI risks. "
            "Specific team structures are not defined in the retrieved documents."
        ),
    },
    {
        "id": "tc_004",
        "name": "Hallucination: fabricated penalty figure",
        "expected_outcome": "FAIL",
        "input": "What is the maximum penalty for violations of prohibited AI practices under the EU AI Act?",
        "expected_output": "The maximum penalty is EUR 35 million or 7 percent of global annual turnover.",
        # Injected deliberately, in both simulated and live runs, so the
        # faithfulness/hallucination metric has a real false claim to catch.
        "injected_response": (
            "The maximum penalty for violations of prohibited AI practices is "
            "EUR 50 million or 10 percent of global annual turnover."
        ),
    },
    {
        "id": "tc_005",
        "name": "Out of scope query",
        "expected_outcome": "FAIL",
        "input": "What are the specific technical requirements for facial recognition systems under the EU AI Act?",
        "expected_output": (
            "The retrieved documents do not contain specific technical requirements "
            "for facial recognition systems. This query is outside the scope of the "
            "current knowledge base."
        ),
    },
]


# --- G-Eval criteria for EU AI Act Articles 10 and 14 (mirrors 03b) ---

def build_faithfulness_metric() -> GEval:
    return GEval(
        name="Faithfulness to Retrieved Regulatory Context",
        criteria=(
            "Determine whether every factual claim in the actual output is directly "
            "supported by the retrieval context, with no invented figures, articles, "
            "or provisions not present in the context."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.RETRIEVAL_CONTEXT,
        ],
        model=ClaudeJudge(),
        threshold=PASS_THRESHOLD,
    )


# --- Real, executable test functions ---

@pytest.mark.skipif(not (GOOGLE_API_KEY and ANTHROPIC_API_KEY),
                     reason="GOOGLE_API_KEY and ANTHROPIC_API_KEY both required for a real run")
@pytest.mark.parametrize("tc", TEST_CASES, ids=[tc["id"] for tc in TEST_CASES])
def test_governance_case(tc):
    """Runs one of the five real governance test cases end to end: real
    retrieval, real Gemini generation (or the deliberately injected
    hallucination for tc_004), real Claude-as-judge scoring via GEval,
    and real three-queue routing against PASS_THRESHOLD/FAIL_THRESHOLD."""
    context = retrieve_context(tc["input"])

    if "injected_response" in tc:
        actual_output = tc["injected_response"]
    else:
        actual_output = generate_answer(tc["input"], context)

    test_case = LLMTestCase(
        input=tc["input"],
        actual_output=actual_output,
        expected_output=tc["expected_output"],
        retrieval_context=context,
    )

    metric = build_faithfulness_metric()
    metric.measure(test_case)
    routing = route_result(metric.score)

    assert routing == tc["expected_outcome"], (
        f"{tc['id']} ({tc['name']}): expected routing {tc['expected_outcome']}, "
        f"got {routing} (score={metric.score:.3f}, reason={metric.reason})"
    )


# --- Three-queue routing unit tests (no API required, pure logic) ---

def test_routing_pass_threshold():
    assert route_result(0.95) == "PASS"

def test_routing_fail_threshold():
    assert route_result(0.30) == "FAIL"

def test_routing_borderline_zone():
    assert route_result(0.70) == "BORDERLINE"
