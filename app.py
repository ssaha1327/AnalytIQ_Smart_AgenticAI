import gradio as gr
from AnalytIQ import Analytiq


async def setup():
    analytiq = Analytiq()
    await analytiq.setup()
    return analytiq


async def process_message(analytiq, message, success_criteria, history):
    results = await analytiq.run_superstep(message, success_criteria, history)
    return results, analytiq


async def reset():
    new_analytiq = Analytiq()
    await new_analytiq.setup()
    return "", "", None, new_analytiq


def free_resources(analytiq):
    print("Cleaning up")
    try:
        if analytiq:
            analytiq.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")



import gradio as gr

with gr.Blocks(
    title="AnalytIQ — An Agentic AI that self-corrects its reasoning to deliver actionable insights(RAG)",
    theme=gr.themes.Base(
        primary_hue="emerald",
        secondary_hue="slate",
        neutral_hue="gray"
    ),
    css="""
        body {
            background-color: #0d1117; /* dark navy background */
            color: #e5e7eb; /* soft gray text */
            font-family: 'Inter', sans-serif;
        }
        #app-title {
            text-align:center;
            font-size:2.2rem;
            color:#000000; /* black */
            margin-top:1.2rem;
            font-weight:800;
            text-shadow:0px 0px 10px rgba(16,185,129,0.3);
        }
        #subtitle {
            text-align:center;
            color:#93c5fd;
            margin-bottom:2rem;
            font-size:1.1rem;
        }
        .gr-button-primary {
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            color: white !important;
            font-weight: 600;
            border: none;
            box-shadow: 0 0 10px rgba(16,185,129,0.3);
            transition: all 0.3s ease;
        }
        .gr-button-primary:hover {
            box-shadow: 0 0 15px rgba(16,185,129,0.6);
            transform: scale(1.02);
        }
        .gr-button-secondary {
            background: #1f2937;
            color: #e5e7eb;
            border: 1px solid #374151;
        }
        .gr-textbox textarea {
            border-radius: 10px;
            background-color: #111827;
            color: #f9fafb;
            font-size: 1rem;
        }
        .gr-chatbot {
            background-color: #111827;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        footer {
            text-align:center;
            font-size:0.85rem;
            color:#6b7280;
            margin-top:2rem;
        }
    """
) as ui:

    # --- HEADER ---
    gr.Markdown("<h1 id='app-title'>🧠 AnalytIQ — Smart AI Agent</h1>")
    gr.Markdown("<p id='subtitle'>An Agentic AI that self-corrects its reasoning to deliver actionable insights(RAG)</p>")

    # --- STATE ---
    sidekick = gr.State(delete_callback=free_resources)

    # --- CHAT DISPLAY ---
    with gr.Row():
        chatbot = gr.Chatbot(
            label="💬 Chat with AnalytIQ",
            height=420,
            type="messages",
            bubble_full_width=False,
            show_copy_button=True
        )

    # --- INPUT AREA ---
    with gr.Group():
        gr.Markdown("### 💡 Enter Your Request")
        message = gr.Textbox(
            show_label=False,
            placeholder="e.g., 'Searching the internet-flight tickets,book resturant etc, Providing summaries, Navigating through websites and extracting information'",
            lines=2,
            container=True
        )
        success_criteria = gr.Textbox(
            show_label=False,
            placeholder="(Optional) Define success criteria — e.g., 'confirm'",
            lines=2
        )

    # --- CONTROL BUTTONS ---
    with gr.Row(equal_height=True):
        reset_button = gr.Button("🔁 Reset", variant="secondary")
        go_button = gr.Button("🚀 Execute", variant="primary")

    # --- CAPABILITIES ACCORDION ---
    with gr.Accordion("⚙️ Sidekick Capabilities", open=False):
        gr.Markdown("""
    **I can assist with a variety of tasks, including but not limited to:**

    - 🌐 **Information Retrieval:** Searching the internet for information on a wide range of topics, such as flights, historical facts, or specific queries.  
    - ✍️ **Text Summarization:** Providing summaries of longer texts or articles to distill important information.  
    - 📊 **Data Processing:** Performing calculations and data manipulation using Python, such as analyzing numbers or generating data.  
    - 📁 **File Management:** Reading, writing, moving, and deleting files on the system as needed.  
    - 🧭 **Web Navigation:** Navigating through websites and extracting information, including text and links.  
    - 🔔 **Notification Sending:** Sending notifications, such as push notifications.  
    - 🤖 **Multi-Tool Coordination:** Using multiple tools simultaneously to perform complex tasks more efficiently.  
    - 💬 **Interactive Assistance:** Answering questions and providing guidance interactively based on user inputs.  
    """)

    # --- FUNCTIONALITY ---
    ui.load(setup, [], [sidekick])
    message.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    success_criteria.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    go_button.click(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])

    # --- FOOTER ---
    gr.Markdown("<footer>© 2025 AnalytIQ AI | Built by Saikat Saha | Dark Mode Edition 🌙</footer>")

ui.launch(inbrowser=True)
