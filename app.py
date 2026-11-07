
import gradio as gr

from rag import ask, rewrite_question

def chat(message, history):
    print("History received:", repr(history))
    standalone_question = rewrite_question(message, history)

    print("Original question:", message)
    print("Rewritten question:", standalone_question)

    answer, sources = ask(standalone_question)

    if sources:
        source_text = "\n".join(
            f"- {source}" for source in sources
        )
        return f"{answer}\n\n---\n\n**Sources:**\n{source_text}"

    return answer



custom_css = """
.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    background: #F5F8F3 !important;
}

#header {
    text-align: center;
    padding: 22px;
    background: #142D5A;
    color: white;
    border-radius: 16px;
}

#header h1, #header p {
    color: white !important;
}

#chat-area {
    border: 1px solid #DCE6DE;
    border-radius: 14px;
}

footer {
    display: none !important;
}
"""


theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="blue",
    neutral_hue="slate"
)


with gr.Blocks(theme=theme, css=custom_css) as demo:

    gr.HTML("""
        <div id="header">
            <h1>🎓 UniGuide AI</h1>
            <p>Palestine Technical University - Kadoorie</p>
            <p>Your Smart Academic Assistant</p>
        </div>
    """)

    gr.ChatInterface(
        fn=chat,
        chatbot=gr.Chatbot(
            height=500,
            elem_id="chat-area"
        ),
        examples=[
            "When are the first semester midterm exams?",
            "What is the sibling tuition discount?",
            "How do I calculate my cumulative GPA?"
        ]
    )


demo.launch(server_port=7861)


