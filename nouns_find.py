import stanza
import gradio as gr
from collections import Counter

stanza.download('uk')
nlp = stanza.Pipeline('uk')

def extract_nouns_from_file(file):
    try:
        with open(file.name, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return f"Помилка читання файлу: {e}", None

    doc = nlp(text)
    nouns = [word.text.lower() for sentence in doc.sentences for word in sentence.words if word.upos == "NOUN"]
    nouns_count = Counter(nouns)
    nouns_result = ", ".join([f"{noun}: {count}" for noun, count in nouns_count.items()])

    output_file = "nouns_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(nouns_result)

    return nouns_result, output_file

custom_css = """
body {
    background-color: white;
    color: #ff66b2;
}
.gr-button {
    background-color: white;
    color: black;
    border: 2px solid #ff99c8;
    font-weight: bold;
    border-radius: 8px;
    padding: 8px 16px;
}
.gr-button:hover {
    background-color: #ff99c8;
    color: white;
}
.gr-textbox, .gr-file {
    border: 2px solid #ff99c8;
    border-radius: 8px;
    padding: 8px;
    font-size: 16px;
    color: black;
}
"""

with gr.Blocks(css=custom_css) as interface:
    gr.Markdown(
        """
        <h1>Витяг іменників з тексту</h1>
        <p>Завантажте файл із текстом українською, щоб отримати список іменників.</p>
        """
    )
    with gr.Row():
        file_input = gr.File(label="Завантажте файл із текстом", file_types=[".txt"])
    with gr.Row():
        text_output = gr.Textbox(label="Іменники в тексті", lines=10, max_lines=20)
    with gr.Row():
        file_output = gr.File(label="Файл із результатом")
    with gr.Row():
        btn = gr.Button("Аналізувати текст")

    btn.click(extract_nouns_from_file, inputs=file_input, outputs=[text_output, file_output])

interface.launch()