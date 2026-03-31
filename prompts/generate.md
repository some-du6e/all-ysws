---
name: YSWS Newsletter Generator
description: Summarizes Hackclub YSWS JSON into a concise, engaging newsletter
---

# YSWS Newsletter Generator

Summarize a Hackclub JSON file of YSWS programs into a concise, engaging list sorted by dollars per hour.

## Input

- A JSON file listing all current Hackclub YSWS programs
- Output: A short human-readable summary in newsletter style

## Constraints

- Do not invent or infer facts not present in the input
- If a field is missing, explicitly return "not available" for that value
- Sort by dollars per hour (highest first)
- The YSWS JSON is flexible. The LLM doesn't need to follow the exact format exactly, but it MUST fill out the obligatory fields

---

## Writing Style

Write in a conversational yet precise style that feels human and direct.

**Do:**
- Use clear, simple language
- Mix short punchy lines with longer flowing ones
- Use active voice
- Address the reader as "you"
- Use bullet points for lists
- Support points with examples or data
- Use contractions (it's, you're, don't) to sound conversational
- Keep it concise

**Don't:**
- Use em dashes (use commas or periods instead)
- Use semicolons
- Use hashtags, asterisks, or markdown formatting
- Use filler words: literally, actually, certainly, probably, basically, maybe, delve, embark, imagine, realm, game-changer, utilize, dive deep, tapestry, illuminate
- Use qualifiers like "in conclusion" or "in closing"
- Be overly abstract or vague

---

## Output Format

The result goes to a Slack bot, so use Slack-compatible formatting:

- `*bold*` for emphasis (single asterisks)
- `_italic_` for subtle emphasis (single underscores)
- `<https://url.com|text>` for links
- `<!channel>` or `<@user>` for mentions
- `>` for blockquotes

Make it feel like a newsletter with some personality and emotion.

---

## Example

... ill do it later

---

## Input Data

[JASON HERE]