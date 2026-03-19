import os
import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage

from config.settings import APP_TITLE, APP_ICON, LAYOUT, TEMP_DIR
from graph.builder import build_graph
from utils.helpers import ensure_dir, generate_thread_id


@st.cache_resource
def get_graph():
    return build_graph()


graph = get_graph()

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=LAYOUT)
st.title("🎙️ AI Technical Interviewer")

# Session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()
if "started" not in st.session_state:
    st.session_state.started = False

thread = {"configurable": {"thread_id": st.session_state.thread_id}}

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")

    if uploaded_file and not st.session_state.started:
        if st.button("Start Interview", type="primary", use_container_width=True):

            ensure_dir(TEMP_DIR)
            pdf_path = os.path.join(TEMP_DIR, f"{st.session_state.thread_id}.pdf")

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Parsing CV & Generating Agenda..."):
                for _ in graph.stream({"pdf_path": pdf_path}, thread):
                    pass

            st.session_state.started = True
            st.rerun()

    if st.session_state.started:
        st.divider()
        st.subheader("📋 Interview Agenda")

        state = graph.get_state(thread)
        if state and state.values:
            current = state.values.get("current_topic")
            plan = state.values.get("interview_plan", [])

            if current:
                st.info(f"**👉 Discussing:** {current}")

            if plan:
                st.write("**Up Next:**")
                for p in plan:
                    st.write(f"- {p}")

# Main UI
if not st.session_state.started:
    st.info("👈 Please enter your API key and upload a CV in the sidebar to begin.")


    state = graph.get_state(thread)

    if state and state.values.get("messages"):
        for msg in state.values["messages"]:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            with st.chat_message(role):
                st.markdown(msg.content)

    is_complete = not state.next if state else False

    if is_complete:
        st.chat_input("Interview Complete.", disabled=True)
    elif user_input := st.chat_input("Type your answer here..."):
        with st.chat_message("user"):
            st.markdown(user_input)

        graph.update_state(thread, {"messages": [HumanMessage(content=user_input)]})

        with st.spinner("Analyzing..."):
            for _ in graph.stream(None, thread):
                pass

        st.rerun()