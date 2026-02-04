import streamlit as st
import ollama
import time

# =============================
# Configuration
# =============================
MODEL_NAME = "dolphin3:8b" 

# Optimized for 4GB VRAM
CHUNK_SIZE = 15_000   # Characters per chunk (~4k tokens)
MAX_FILE_SIZE = 20_000_000 # 20MB limit
TEMPERATURE = 0.0

# =============================
# Utility helpers
# =============================

def build_dolphin_prompt(code: str, chunk_num=None, total_chunks=None) -> str:
    chunk_info = f" (Chunk {chunk_num}/{total_chunks})" if chunk_num else ""
    return f"""
Role:
You are an elite Red Team Security Researcher. Your goal is to find exploitable vulnerabilities{chunk_info}.
Be technical, blunt, and precise.

Task:
Perform a deep security audit on the following JavaScript code.

Report on:
1. ATTACK SURFACE: API endpoints, hardcoded URLs, and data entry points.
2. INJECTION: Trace untrusted data into sinks (innerHTML, eval, document.write).
3. SECRETS: Hardcoded API keys, JWTs, or internal credentials.
4. LOGIC: Client-side auth bypasses or insecure local storage usage.

For each finding:
- SEVERITY: (Critical | High | Medium | Low)
- LOCATION: Line number/code snippet
- EXPLOIT: How an attacker triggers it
- FIX: Technical remediation

CODE:
---
{code}
---
"""

# =============================
# Streamlit UI
# =============================
st.set_page_config(
    page_title="Dolphin 3.0 Large File Scanner",
    page_icon="🐬",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0b0d10; color: #00ff41; }
    .stCodeBlock { border: 1px solid #00ff41; }
    .stMarkdown h1, h2, h3 { color: #00ff41 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("🐬 Dolphin Settings")
    st.info("Target: RTX 3050 Ti (4GB)")

    ctx_limit = st.select_slider(
        "VRAM Context Window",
        options=[2048, 4096, 8192],
        value=2048
    )
    
    st.divider()
    st.write("⚙️ **Large File Mode**")
    use_chunking = st.toggle("Enable Auto-Chunking", value=True)
    
    if "bug_count" not in st.session_state:
        st.session_state.bug_count = 0
    st.metric("Total Vulnerabilities Found", st.session_state.bug_count)

# Main
st.title("🔓 Large-Scale JS Security Audit")
st.caption(f"Engine: {MODEL_NAME} | Hardware Optimized")

uploaded_file = st.file_uploader("Upload .js file", type=["js"])

if uploaded_file:
    raw_code = uploaded_file.read().decode("utf-8", errors="ignore")
    
    # Logic for chunking
    if use_chunking and len(raw_code) > CHUNK_SIZE:
        chunks = [raw_code[i:i+CHUNK_SIZE] for i in range(0, len(raw_code), CHUNK_SIZE)]
        st.warning(f"Large file detected. Split into {len(chunks)} chunks for VRAM safety.")
    else:
        chunks = [raw_code]

    if st.button("🚀 Start Deep Audit"):
        st.session_state.bug_count = 0
        full_report = ""
        start_time = time.time()
        
        # Progress bar for the user
        progress_bar = st.progress(0)
        
        for idx, chunk_content in enumerate(chunks):
            chunk_label = f"Part {idx+1} of {len(chunks)}"
            st.subheader(f"🔍 Analyzing {chunk_label}")
            
            report_area = st.empty()
            chunk_report = ""
            
            try:
                stream = ollama.generate(
                    model=MODEL_NAME,
                    prompt=build_dolphin_prompt(chunk_content, idx+1, len(chunks)),
                    stream=True,
                    options={
                        "num_ctx": ctx_limit,
                        "temperature": TEMPERATURE,
                        "num_gpu": 32,
                        "low_vram": True,
                    }
                )

                for chunk in stream:
                    content = chunk.get("response", "")
                    chunk_report += content
                    report_area.markdown(chunk_report + "▌")
                
                # Update global report and counter
                full_report += f"\n\n--- REPORT FOR {chunk_label} ---\n\n" + chunk_report
                st.session_state.bug_count += chunk_report.lower().count("severity:")
                
                # Update progress
                progress_bar.progress((idx + 1) / len(chunks))

            except Exception as e:
                st.error(f"Error on {chunk_label}: {e}")
                break

        duration = round(time.time() - start_time, 2)
        st.success(f"Full audit complete in {duration}s")
        st.download_button("📩 Download Full Report", full_report, "full_audit.md")

else:
    st.info("Upload a file to begin.")
