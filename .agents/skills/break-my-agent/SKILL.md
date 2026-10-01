---
name: break-my-agent
description: Interview a user about a RAG or agent system one question at a time, then produce a prioritized risk list, a practical evaluation plan, and a handoff to the relevant engineering skills.
license: Apache-2.0
---

# Break My Agent

Use when a user wants to pressure-test a RAG or agent design before implementation or release.
Ask exactly one consequential question per turn and wait for the answer before continuing.
Adapt follow-up questions to the answers; cover goals, data and permissions, retrieval or tools, failure handling, human control, and constraints.
Ask only about unknowns that could change a design, risk, or evaluation; stop when remaining unknowns can be stated as assumptions.
Do not request confidential records, credentials, or production data; ask for a sanitized system description.
Conclude with a concise system summary and clearly marked assumptions.
Give a prioritized risk list with evidence or uncertainty, consequence, and a practical mitigation for each item.
Give an evaluation plan with representative tasks, baseline, metrics, acceptance gates, safety cases, and regression checks.
Hand off by naming the relevant specialist skills: ai-system-design, rag-engineering, mcp-engineering, llm-evaluation, agent-engineering, python-production, security-review, and code-review.
Do not imply that an interview or proposed plan proves readiness; ask which handoff the user wants to run next.
