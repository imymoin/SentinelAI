import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIG
# ============================================================

DEFAULT_API_URL = os.getenv(
    "SENTINEL_API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(14, 165, 233, 0.08),
                transparent 25%
            ),
            #080b12;
    }

    .main {
        padding-top: 1rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Hide Streamlit branding */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: #0b0f18;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* -------------------------------------------------------
       BRAND
    ------------------------------------------------------- */

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #06b6d4
            );

        box-shadow:
            0 8px 30px rgba(99,102,241,0.28);

        font-size: 23px;
    }

    .brand-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #f8fafc;
    }

    .brand-subtitle {
        color: #64748b;
        font-size: 11px;
        margin-top: -2px;
    }

    /* -------------------------------------------------------
       HERO
    ------------------------------------------------------- */

    .hero {
        padding: 20px 0 10px 0;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 850;
        line-height: 1.05;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #a5b4fc,
                #67e8f9
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        letter-spacing: -1.5px;
    }

    

    /* -------------------------------------------------------
       STATUS CARDS
    ------------------------------------------------------- */

    .status-card {
        background: rgba(15,23,42,0.68);
        border: 1px solid rgba(148,163,184,0.10);
        border-radius: 16px;

        padding: 15px 17px;

        backdrop-filter: blur(14px);

        min-height: 85px;
    }

    .status-label {
        color: #64748b;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
    }

    .status-value {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 750;
        margin-top: 7px;
    }

    .online {
        color: #34d399;
    }

    .offline {
        color: #fb7185;
    }

    /* -------------------------------------------------------
       CHAT
    ------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: rgba(15,23,42,0.45);
        border: 1px solid rgba(148,163,184,0.08);
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    /* -------------------------------------------------------
       GLASS PANEL
    ------------------------------------------------------- */

    .glass-panel {
        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,0.80),
                rgba(15,23,42,0.48)
            );

        border: 1px solid rgba(148,163,184,0.10);

        border-radius: 20px;

        padding: 20px;

        backdrop-filter: blur(18px);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.18);
    }

    /* -------------------------------------------------------
       TOOL BADGES
    ------------------------------------------------------- */

    .badge {
        display: inline-block;

        padding: 5px 10px;

        border-radius: 999px;

        font-size: 11px;
        font-weight: 700;

        margin: 2px;
    }

    .badge-purple {
        background: rgba(99,102,241,0.14);
        color: #a5b4fc;
        border: 1px solid rgba(99,102,241,0.20);
    }

    .badge-cyan {
        background: rgba(6,182,212,0.12);
        color: #67e8f9;
        border: 1px solid rgba(6,182,212,0.18);
    }

    .badge-green {
        background: rgba(16,185,129,0.12);
        color: #6ee7b7;
        border: 1px solid rgba(16,185,129,0.18);
    }


    /* -------------------------------------------------------
       METRICS
    ------------------------------------------------------- */

    .metric-box {
        background: rgba(15,23,42,0.55);
        border: 1px solid rgba(148,163,184,0.08);
        border-radius: 14px;
        padding: 13px;
        text-align: center;
    }

    .metric-number {
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
    }

    .metric-label {
        font-size: 10px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* -------------------------------------------------------
       DIVIDER
    ------------------------------------------------------- */

    .soft-divider {
        height: 1px;
        background: rgba(148,163,184,0.08);
        margin: 20px 0;
    }

    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(148,163,184,0.10);
        background: rgba(15,23,42,0.65);
        color: #cbd5e1;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(99,102,241,0.45);
        color: white;
        transform: translateY(-1px);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_url" not in st.session_state:
    st.session_state.api_url = DEFAULT_API_URL

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("SENTINEL_API_KEY", "")

if "server_status" not in st.session_state:
    st.session_state.server_status = None

if "last_request_id" not in st.session_state:
    st.session_state.last_request_id = None

if "last_latency" not in st.session_state:
    st.session_state.last_latency = None


# ============================================================
# API HELPERS
# ============================================================

def get_headers():
    api_key = st.session_state.api_key.strip()


    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def check_health():
    try:
        start = time.perf_counter()

        response = requests.get(
            f"{st.session_state.api_url}/health",
            timeout=5,
        )

        latency = (
            time.perf_counter() - start
        ) * 1000

        if response.status_code == 200:
            return True, round(latency, 2)

        return False, round(latency, 2)

    except requests.RequestException:
        return False, None


def get_metrics():
    try:
        response = requests.get(
            f"{st.session_state.api_url}/metrics",
            timeout=5,
        )

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        pass

    return None


def send_message(query):
    start = time.perf_counter()

    response = requests.post(
        f"{st.session_state.api_url}/chat",
        headers=get_headers(),
        json={
            "query": query,
        },
        timeout=120,
    )

    latency = (
        time.perf_counter() - start
    ) * 1000

    return response, round(latency, 2)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🛡️</div>
            <div>
                <div class="brand-title">SentinelAI</div>
                <div class="brand-subtitle">
                    Secure AI Gateway
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    st.markdown("### ⚙️ Configuration")

    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="URL of the SentinelAI FastAPI backend.",
    )

    st.session_state.api_url = api_url.rstrip("/")

    if st.button(
        "🔌 Test Connection",
        use_container_width=True,
    ):
        status, latency = check_health()

        if status:
            st.success(
                f"Connected • {latency} ms"
            )
        else:
            st.error(
                "Unable to connect to API"
            )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 🧠 AI Stack")

    st.markdown(
        """
        <span class="badge badge-purple">LangGraph</span>
        <span class="badge badge-purple">LiteLLM</span>
        <span class="badge badge-cyan">Groq</span>
        <span class="badge badge-cyan">ChromaDB</span>
        <span class="badge badge-green">MCP</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 🛡️ Security")

    security_items = [
        "API authentication",
        "Input guardrail",
        "Tool authorization",
        "Argument validation",
        "Output guardrail",
        "Request tracing",
    ]

    for item in security_items:
        st.markdown(
            f"✓ {item}"
        )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div style="
            position: fixed;
            bottom: 20px;
            color: #475569;
            font-size: 11px;
        ">
            SentinelAI v1.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            Intelligent. Secure. Observable.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# STATUS
# ============================================================

health, health_latency = check_health()

col1, col2, col3, col4 = st.columns(4)

with col1:
    status_text = "Online" if health else "Offline"
    status_class = "online" if health else "offline"

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">API Status</div>
            <div class="status-value {status_class}">
                ● {status_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-label">LLM Gateway</div>
            <div class="status-value">
                LiteLLM
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-label">Orchestration</div>
            <div class="status-value">
                LangGraph
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    latency_text = (
        f"{health_latency} ms"
        if health_latency is not None
        else "—"
    )

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">API Latency</div>
            <div class="status-value">
                {latency_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# MAIN LAYOUT
# ============================================================

chat_col, info_col = st.columns(
    [2.8, 1],
    gap="large",
)


# ============================================================
# CHAT
# ============================================================

with chat_col:

    st.markdown(
        """
        <div class="glass-panel">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 💬 SentinelAI Assistant"
    )

    st.caption(
        "Ask a question. SentinelAI automatically determines "
        "whether to use direct LLM, RAG or MCP."
    )

    if not st.session_state.messages:

        st.markdown(
            """
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("metadata")
            ):

                metadata = message["metadata"]

                st.caption(
                    f"⚡ {metadata.get('latency', '—')} ms"
                    f"  •  🆔 {metadata.get('request_id', '—')}"
                )

    prompt = st.chat_input(
        "Message SentinelAI..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "SentinelAI is thinking..."
            ):

                try:

                    response, latency = send_message(
                        prompt
                    )

                    if response.status_code == 200:

                        data = response.json()

                        # Support different response field names
                        answer = (
                            data.get("response")
                            or data.get("answer")
                            or data.get("message")
                            or data.get("result")
                        )

                        if isinstance(
                            answer,
                            dict,
                        ):
                            answer = str(answer)

                        if not answer:
                            answer = str(data)

                        request_id = (
                            response.headers.get(
                                "X-Request-ID"
                            )
                            or data.get(
                                "request_id"
                            )
                        )

                        st.markdown(answer)

                        st.caption(
                            f"⚡ {latency} ms"
                            f"  •  🆔 "
                            f"{request_id or 'N/A'}"
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                                "metadata": {
                                    "latency": latency,
                                    "request_id": (
                                        request_id
                                        or "N/A"
                                    ),
                                },
                            }
                        )

                        st.session_state.last_request_id = (
                            request_id
                        )

                        st.session_state.last_latency = (
                            latency
                        )

                    else:

                        try:
                            error_data = response.json()
                        except Exception:
                            error_data = response.text

                        error_message = (
                            f"API Error "
                            f"{response.status_code}: "
                            f"{error_data}"
                        )

                        st.error(
                            error_message
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": error_message,
                            }
                        )

                except requests.exceptions.ConnectionError:

                    error_message = (
                        "❌ Cannot connect to SentinelAI API.\n\n"
                        "Make sure FastAPI is running."
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

                except requests.exceptions.Timeout:

                    error_message = (
                        "⏱️ The request timed out. "
                        "The model may still be processing."
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

                except Exception as exc:

                    error_message = (
                        f"Unexpected error: {exc}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# RIGHT PANEL
# ============================================================

with info_col:

    st.markdown(
        """
        <div class="glass-panel">

        <h3 style="
            color:#f8fafc;
            margin-bottom:15px;
        ">
            🧩 System
        </h3>

        <div style="
            color:#94a3b8;
            font-size:13px;
            line-height:2;
        ">

        <div>🧠 <b>LangGraph</b> — Agent routing</div>
        <div>📚 <b>RAG</b> — ChromaDB retrieval</div>
        <div>🔌 <b>MCP</b> — Tool execution</div>
        <div>⚡ <b>Groq</b> — LLM inference</div>
        <div>🛡️ <b>Guardrails</b> — Security</div>
        <div>📊 <b>Metrics</b> — Observability</div>

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-panel">

        <h3 style="
            color:#f8fafc;
            margin-bottom:15px;
        ">
            🔐 MCP Tools
        </h3>

        <div style="
            color:#94a3b8;
            font-size:12px;
            line-height:1.9;
        ">

        <div>📄 file_get_project_info</div>
        <div>📄 file_get_project_status</div>
        <div>👤 db_get_employee</div>
        <div>📊 db_get_project_status</div>
        <div>👥 db_get_team_members</div>

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metrics = get_metrics()

    if metrics:

        st.markdown(
            """
            <div class="glass-panel">
            <h3 style="
                color:#f8fafc;
                margin-bottom:15px;
            ">
                📊 Live Metrics
            </h3>
            """,
            unsafe_allow_html=True,
        )

        total = metrics.get(
            "requests_total",
            0,
        )

        failed = metrics.get(
            "requests_failed",
            0,
        )

        avg_latency = metrics.get(
            "average_request_duration_ms",
            0,
        )

        m1, m2 = st.columns(2)

        with m1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-number">
                        {total}
                    </div>
                    <div class="metric-label">
                        Requests
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-number">
                        {failed}
                    </div>
                    <div class="metric-label">
                        Failed
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.metric(
            "Average Latency",
            f"{avg_latency} ms",
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#475569;
        font-size:11px;
        margin-top:35px;
        padding:20px;
    ">
        🛡️ SentinelAI
        &nbsp;•&nbsp;
        Secure AI Gateway
        &nbsp;•&nbsp;
        LangGraph + RAG + MCP + LiteLLM
    </div>
    """,
    unsafe_allow_html=True,
)
