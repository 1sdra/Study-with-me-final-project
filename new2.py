import streamlit as st
import requests
import PyPDF2
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

os.makedirs("drawings", exist_ok=True)

st.set_page_config(
    page_title="Study with me",
    page_icon="🎀",
    layout="centered"
)


def ai(prompt):
    key = st.secrets["GEMINI_API_KEY"]

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(
            url,
            headers={
                "x-goog-api-key": key,
                "Content-Type": "application/json"
            },
            json=data
        )

        result = response.json()

        if "error" in result:
            return "Gemini error"

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return "Something went wrong"


def read_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    reader = PyPDF2.PdfReader(file)

    return "".join(
        page.extract_text() or ""
        for page in reader.pages
    )


def go(page):
    st.session_state.page = page
    st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "Home"


# HOME

if st.session_state.page == "Home":

    st.title("🎀 Study with me")

    st.write("🎀 Lets Study Together With AI 🎀")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("📝 Notes"):
            go("Notes")

        if st.button("🧠 AI Quiz"):
            go("Quiz")

        if st.button("📅 Planner"):
            go("Planner")

    with col2:

        if st.button("🤖 AI Assistant"):
            go("AI")

        if st.button("📖 Dictionary"):
            go("Dictionary")

        if st.button("🎨 Drawing"):
            go("Drawing")


# NOTES

elif st.session_state.page == "Notes":
    st.title("Notes")

    if st.button("🏠 Home"):
        go("Home")

    notes = st.text_area("Write your notes 💌✨")
    file = st.file_uploader("Upload PDF or TXT ^_^", type=["pdf", "txt"])

    if st.button(" Summarize with Gemini 💛💛"):
        text = notes + ("\n" + read_file(file) if file else "")

        if text.strip():
            st.write(ai("Summarize this study material in simple bullet points:\n" + text))
        else:
            st.warning("Write notes or upload a file 🤝.")


# AI ASSISTANT

elif st.session_state.page == "AI":
    st.title("AI Assistant")

    if st.button("🏠 Home"):
        go("Home")

    question = st.text_input("Ask Gemini anything you want 😆🤷‍♂️")

    if st.button("Ask") and question:
        st.write(ai(question))


# QUIZ

elif st.session_state.page == "Quiz":

    st.title("AI Quiz")

    if st.button("🏠 Home"):
        go("Home")

    file = st.file_uploader(
        "Upload PDF or TXT ^_^",
        type=["pdf", "txt"]
    )

    if st.button("Generate Quiz"):

        if file:
            text = read_file(file)

            prompt = (
                "Create 5 multiple choice questions from this text.\n"
                "For each question give 4 options and show the correct answer.\n\n"
                "Text:\n" + text
            )

            st.write(ai(prompt))

        else:
            st.warning("Upload your study file 😊💌⏪.")


# DICTIONARY

elif st.session_state.page == "Dictionary":

    st.title("Dictionary")

    if st.button("🏠 Home"):
        go("Home")

    word = st.text_input("Enter a word you want to search for 🤷‍♂️🙄🌎")

    if st.button("Explain") and word:
        st.write(ai("Explain this word simply and give an example: " + word))


# PLANNER

elif st.session_state.page == "Planner":

    st.title("Study Planner")

    if st.button("🏠 Home"):
        go("Home")

    subject = st.text_input("Subject")
    date = st.date_input("Date")
    time = st.time_input("Time")

    if st.button("Add Session"):
        st.success(f"{subject} - {date} - {time}")


# DRAWING

elif st.session_state.page == "Drawing":

    st.title(" Drawing Notes 🖌📍")

    if st.button("🏠 Home"):
        go("Home")

    name = st.text_input(" Note name ")

    color = st.color_picker(" Choose a color 🎨 ", "#D13D56")

    canvas = st_canvas(
        stroke_width=st.slider(" Pen size ✏️", 1, 20, 3),
        stroke_color=color,
        background_color="white",
        height=400,
        width=700,
        key="drawing"
    )

    if st.button("💾 Save"):

        if name:

            Image.fromarray(
                canvas.image_data.astype("uint8")
            ).save(f"drawings/{name}.png")

            st.success("Saved 🎀💟")

    files = os.listdir("drawings")

    if files:

        selected = st.selectbox("📂 My Notes", files)

        st.image(f"drawings/{selected}")