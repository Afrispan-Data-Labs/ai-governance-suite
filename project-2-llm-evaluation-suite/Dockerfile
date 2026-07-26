# Production LLM Evaluation Suite, container image
#
# Packages the evaluation environment (RAGAS, DeepEval, Langfuse, Promptfoo,
# Chroma) with pinned dependency versions so the DeepEval regression suite
# in tests/test_governance_suite.py can run identically in CI and locally.
#
# Status: written and structurally correct, not yet built or run against a
# live registry. Pending funded API credits to verify the image actually
# executes the test suite end to end.
#
# ragas is pinned to 0.3.9: versions 0.4.x carry a broken import
# (ragas/llms/base.py references langchain_community.chat_models.vertexai,
# a path removed after ChatVertexAI moved to langchain-google-vertexai).
# See: github.com/vibrantlabsai/ragas/issues/2745

FROM python:3.11-slim AS base

# Node is required for Promptfoo (Phase 05), which is npm-distributed,
# not a Python package. Promptfoo 0.121.19 requires Node ^20.20.0 or
# >=22.22.0, so Node 22.x is installed explicitly rather than relying on
# whatever the base image ships.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY project-2-llm-evaluation-suite/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN npm install -g promptfoo@0.121.19

COPY project-2-llm-evaluation-suite/ ./project-2-llm-evaluation-suite/

# All red-team generation stays local, never falls back to OpenAI's API
# (which now owns Promptfoo as of March 2026), since this project uses
# Claude and Gemini only.
ENV PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION=true

# API keys and Langfuse credentials are injected at runtime, never baked
# into the image.
ENV GOOGLE_API_KEY=""
ENV ANTHROPIC_API_KEY=""
ENV LANGFUSE_PUBLIC_KEY=""
ENV LANGFUSE_SECRET_KEY=""
ENV LANGFUSE_HOST=""

CMD ["deepeval", "test", "run", "project-2-llm-evaluation-suite/tests/test_governance_suite.py"]
