import os
import traceback
import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage

from config.settings import APP_TITLE, APP_ICON, LAYOUT, TEMP_DIR
from graph.builder import build_graph
from utils.helpers import ensure_dir, generate_thread_id
from utils.logger import get_logger
from utils.debug_view import format_state_debug

logger = get_logger("main")


@st.cache_resource
def get_graph():
    logger.info("Building graph...")
    return build_graph()


graph = get_graph()

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
)

# -------------------------------
# Session Initialization
# -------------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "started" not in st.session_state:
    st.session_state.started = False

if "initial_plan_len" not in st.session_state:
    st.session_state.initial_plan_len = 0

if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = True

thread = {"configurable": {"thread_id": st.session_state.thread_id}}

# -------------------------------
# Header
# -------------------------------
st.title("🎙️ AI Technical Interviewer")
st.caption("CV-driven mock interview powered by LangGraph + Ollama")

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.header("⚙️ Interview Setup")

    uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")
    st.session_state.debug_mode = st.toggle("Debug mode", value=st.session_state.debug_mode)

    col1, col2 = st.columns(2)

    with col1:
        start_clicked = st.button(
            "Start Interview",
            type="primary",
            use_container_width=True,
            disabled=(uploaded_file is None or st.session_state.started)
        )

    with col2:
        reset_clicked = st.button(
            "Reset",
            use_container_width=True
        )

    if reset_clicked:
        logger.info("Resetting session...")
        st.session_state.thread_id = generate_thread_id()
        st.session_state.started = False
        st.session_state.initial_plan_len = 0
        st.rerun()

    if start_clicked and uploaded_file:
        try:
            logger.info("Starting interview for thread_id=%s", st.session_state.thread_id)

            ensure_dir(TEMP_DIR)
            pdf_path = os.path.join(TEMP_DIR, f"{st.session_state.thread_id}.pdf")

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            logger.info("Saved uploaded CV to %s", pdf_path)

            with st.spinner("Parsing CV and preparing interview agenda..."):
                for _ in graph.stream({"pdf_path": pdf_path}, thread):
                    pass

            state = graph.get_state(thread)
            if state and state.values:
                current_topic = state.values.get("current_topic")
                remaining = state.values.get("interview_plan", [])
                total = (1 if current_topic else 0) + len(remaining)
                st.session_state.initial_plan_len = total
                logger.info("Initial interview plan length=%s", total)

            st.session_state.started = True
            st.rerun()

        except Exception as e:
            logger.exception("Failed to start interview")
            st.error(f"Failed to start interview: {e}")

    # -------------------------------
    # Live Interview Status
    # -------------------------------
    if st.session_state.started:
        st.divider()
        st.subheader("📋 Interview Agenda")

        try:
            state = graph.get_state(thread)

            if state and state.values:
                current = state.values.get("current_topic")
                plan = state.values.get("interview_plan", [])

                total_topics = max(st.session_state.initial_plan_len, 1)
                remaining_topics = len(plan) + (1 if current else 0)
                completed_topics = total_topics - remaining_topics
                progress = min(max(completed_topics / total_topics, 0.0), 1.0)

                st.progress(progress, text=f"Progress: {completed_topics}/{total_topics} topics completed")

                if current:
                    st.info(f"**Current Topic:** {current}")
                else:
                    st.success("All interview topics completed.")

                if plan:
                    st.write("**Up Next:**")
                    for idx, p in enumerate(plan, start=1):
                        st.write(f"{idx}. {p}")

        except Exception:
            logger.exception("Error rendering sidebar agenda")
            st.warning("Could not load interview agenda.")

# -------------------------------
# Main Content
# -------------------------------
if not st.session_state.started:
    st.info("👈 Upload a CV from the sidebar and click **Start Interview**.")

    st.markdown("""
### How it works
1. Upload the candidate CV as PDF  
2. The system extracts CV content  
3. It plans interview topics  
4. It asks CV-based interview questions  
5. It evaluates answers and may ask follow-ups  
6. It generates a final interview report
""")
else:
    try:
        state = graph.get_state(thread)

        # -------------------------------
        # Chat History
        # -------------------------------
        st.subheader("💬 Interview")

        if state and state.values and state.values.get("messages"):
            for msg in state.values["messages"]:
                role = "assistant" if isinstance(msg, AIMessage) else "user"
                avatar = "🎙️" if role == "assistant" else "🧑"
                with st.chat_message(role, avatar=avatar):
                    st.markdown(msg.content)

        # -------------------------------
        # Completion Status
        # -------------------------------
        is_complete = not state.next if state else False

        if is_complete:
            st.success("Interview completed.")
            st.chat_input("Interview Complete.", disabled=True)
        else:
            user_input = st.chat_input("Type your answer here...")

            if user_input:
                logger.info("User submitted answer. thread_id=%s", st.session_state.thread_id)

                # show instantly
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(user_input)

                graph.update_state(thread, {"messages": [HumanMessage(content=user_input)]})

                with st.spinner("Analyzing your response..."):
                    for _ in graph.stream(None, thread):
                        pass

                logger.info("Graph advanced after user input.")
                st.rerun()


        if st.session_state.debug_mode:
            st.divider()
            with st.expander("🛠 Debug State", expanded=False):
                st.code(format_state_debug(state), language="text")

    except Exception as e:
        logger.exception("Main UI rendering failed")
        st.error(f"Something went wrong: {e}")

        if st.session_state.debug_mode:
            st.code(traceback.format_exc(), language="python")