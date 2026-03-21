# Prompt Token Rewriter

**Domain:** `optimization`
**Skill ID:** `optimization/prompt_rewriter`

A middleware skill that acts as a powerful compression logic gate for agents. It ingests a massive, bloated prompt or conversation history and "rewrites" it to use fewer tokens while aggressively retaining semantic meaning and core instructions.

This is critical for complex agents facing strict token constraints or high LLM API costs.

## Manifest Details

**Inputs Schema:**
*   `raw_text` (string): The bloated, repetitive prompt or extensive conversation history to compress.
*   `compression_aggression` (string): The level of compression: 'low', 'medium', or 'high'.

**Outputs Schema:**
*   `compressed_text` (string): The aggressively shortened prompt retaining semantic constraints.
*   `original_tokens` (integer): The approximate original length.
*   `new_tokens` (integer): The approximate new length.
*   `tokens_saved` (integer): The absolute number of tokens removed.

## Usage Guide
The agent invokes this tool automatically when faced with an excessively long string of context or when instructed to compress a payload. The heuristic removes filler words, repetitive structures, and optionally standardizes whitespace and grammar depending on the specified aggression level.
