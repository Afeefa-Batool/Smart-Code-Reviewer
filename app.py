import os
import gradio as gr
from groq import Groq

# Get API key from Hugging Face Secrets
api_key = os.environ.get("GROQ_API_KEY")

# Initialize client only if key exists
if api_key:
    client = Groq(api_key=api_key)
else:
    client = None


def review_code(code):
    if not code.strip():
        return "Please paste some code."

    if client is None:
        return "Groq API key not found. Please add GROQ_API_KEY in Hugging Face Space Secrets."

    prompt = f"""
You are an expert software engineer acting as a code reviewer.

Analyze the following code and give feedback on:

1. Readability
2. Structure
3. Maintainability
4. Best Practices

Also suggest an improved version of the code.

Code:
{code}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error while reviewing code: {str(e)}"


demo = gr.Interface(
    fn=review_code,
    inputs=gr.Code(label="Paste your code here", language="python"),
    outputs=gr.Markdown(label="AI Code Review"),
    title="Smart Code Reviewer",
    description="AI assistant that reviews code for readability, structure, maintainability, and best practices."
)

demo.launch()