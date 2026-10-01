# RAG review comparison

This example keeps the input and prompt fixed and compares two review styles.

- Input: [pipeline.py](pipeline.py)
- Prompt in both conditions: [prompt.md](prompt.md)
- Generic example output: [without-stack.md](without-stack.md)
- Skill-guided example output: [with-stack.md](with-stack.md)

The two outputs are manually written illustrations based on the same code sample and prompt. They demonstrate the expected difference in coverage and evidence, not actual model executions or measured performance. To make a real comparison, run both conditions with the same model/version, surrounding instructions, tools, and prompt on a representative blinded set, then score using a rubric chosen before the run.
