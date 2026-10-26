import gradio as gr
from rag import ask

def chat(question):
    answer, sources = ask(question)
    return answer + "\n\nSources: " + ", ".join(sources)

gr.Interface(
    fn=chat,
    inputs="text",
    outputs="text",
    title="UniGuide AI",
    description="Ask questions about PTUK academic information."
).launch()