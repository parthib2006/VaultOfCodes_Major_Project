# prompt_templates.py

PROMPTS = {
    "answer": {
        "short": (
            "You are a concise expert. Answer the question directly in 2-3 sentences. "
            "If you are unsure, say 'I don't know'.\n\nQuestion: {USER_TEXT}"
        ),
        "medium": (
            "You are an expert teacher. Answer clearly and explain the main idea, "
            "then provide one short example. Keep it under 150 words.\n\nQuestion: {USER_TEXT}"
        ),
        "long": (
            "You are an academic explainer. Provide a structured answer:\n"
            "1) Short direct answer\n2) Background / reasoning (3-6 bullets)\n3) Short example or analogy\n4) Suggested search terms for further reading\n\nQuestion: {USER_TEXT}"
        )
    },
    "summarize": {
        "short": (
            "Summarize the following text in one short paragraph (2–3 sentences):\n\n{USER_TEXT}"
        ),
        "medium": (
            "Read the text below and provide a concise summary in 4–6 bullet points that capture the main points, conclusions, and any action items.\n\nText:\n{USER_TEXT}"
        ),
        "long": (
            "Context: The audience is {AUDIENCE}.\nSummarize the text in three sections:\nA) One-sentence summary\nB) Key points (numbered bullets)\nC) One-sentence takeaway or recommended next step for the audience.\n\nText:\n{USER_TEXT}"
        )
    },
    "create": {
        "short": (
            "Write a short (200–300 words) {STYLE} about: {USER_TEXT}. Keep language vivid and emotive."
        ),
        "medium": (
            "Write a {STYLE} (~400 words) about {USER_TEXT}. Use a {TONE} tone (e.g., melancholic, hopeful). "
            "Include one surprising image/metaphor and end with a one-line hook."
        ),
        "long": (
            "You are an award-winning author. Create a {STYLE} using the following brief:\n"
            "- Theme: {THEME}\n- Main motifs: {MOTIFS}\n- POV: {POV}\n- Opening line (optional): {OPENING}\n- Word target: ~{WORDS}\nMake sure the piece shows, not tells. Use evocative sensory details."
        )
    }
}