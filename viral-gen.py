import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import SystemMessage, HumanMessage

st.set_page_config(
    page_title="viralgen trend engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a0000 0%, #330000 50%, #1a0000 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff0000, #ff6b6b, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .subtitle {
        color: #ffcccc;
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .stats-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 20px;
        color: #ffcccc;
        font-size: 0.85rem;
        margin: 0.3rem;
    }
    
    .stTextInput > div > div > input {
        background: rgba(51, 0, 0, 0.6);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 12px;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff0000;
        box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.2);
    }
    
    .stSelectbox > div > div {
        background: rgba(51, 0, 0, 0.6);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .stMultiSelect > div > div {
        background: rgba(51, 0, 0, 0.6);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .card {
        background: linear-gradient(135deg, rgba(51, 0, 0, 0.4), rgba(26, 0, 0, 0.4));
        border: 1px solid rgba(255, 0, 0, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .result-card {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(51, 0, 0, 0.3));
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
    }
    
    .aura-score {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .script-box {
        background: rgba(26, 0, 0, 0.8);
        border: 1px solid rgba(255, 0, 0, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        color: #ffeeee;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .hashtag-pill {
        display: inline-block;
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        color: #ffcccc;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s;
    }
    
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.4);
        background: linear-gradient(90deg, #cc0000, #990000);
    }
    
    .metric-card {
        background: rgba(51, 0, 0, 0.3);
        border: 1px solid rgba(255, 0, 0, 0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-label {
        color: #ffcccc;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .copy-button {
        background: rgba(255, 0, 0, 0.3);
        border: 1px solid rgba(255, 0, 0, 0.4);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .copy-button:hover {
        background: rgba(255, 0, 0, 0.5);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="main-title">viralgen</div>
    <div class="subtitle">autonomous trend engine for high aura creators</div>
    <div style="margin-top: 1rem;">
        <span class="stats-badge">ai powered</span>
        <span class="stats-badge">trend aware</span>
        <span class="stats-badge">platform optimized</span>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    groq_key = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
    os.environ["GROQ_API_KEY"] = groq_key
    os.environ["TAVILY_API_KEY"] = tavily_key
    config_ok = True
except Exception:
    st.error("api keys not found in secrets please configure groq api key and tavily api key")
    config_ok = False

with st.sidebar:
    st.markdown("### engine settings")
    
    st.markdown("#### platform")
    platform = st.selectbox(
        "target platform",
        ["tiktok", "instagram reels", "youtube shorts", "snapchat spotlight"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### duration")
    script_length = st.select_slider(
        "script length",
        options=["15s", "30s", "60s", "90s"],
        value="30s",
        label_visibility="collapsed"
    )
    
    st.markdown("#### personality")
    persona = st.selectbox(
        "content persona",
        ["stoic sigma", "overstimulated zoomer", "hustle culture bot", 
         "clean girl", "alpha male", "gen z philosopher", "meme lord"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### visual style")
    visual_style = st.selectbox(
        "background visual",
        ["gta parkour", "minecraft drops", "kinetic text", "satisfying slime",
         "subway surfers", "family guy clips", "roblox obby"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### slang density")
    intensity = st.select_slider(
        "intensity",
        options=["low", "med", "high", "max"],
        value="med",
        label_visibility="collapsed"
    )
    
    st.markdown("#### music vibe")
    music_genre = st.selectbox(
        "background music",
        ["phonk", "hyperpop", "lofi", "trap", "drill", "ambient"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### hashtags")
    hashtag_count = st.slider("number of hashtags", 3, 10, 5, label_visibility="collapsed")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 600;">trend topic</h4>', unsafe_allow_html=True)
    topic = st.text_input(
        "enter your viral topic",
        placeholder="search for a trend",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 600;">target slangs</h4>', unsafe_allow_html=True)
    
    slang_options = [
        "aura", "mewing", "mogging", "skibidi", "fanum tax", 
        "cooked", "pookie", "rizz", "sigma", "gyatt", 
        "ohio", "edging", "gooning", "bussin", "no cap"
    ]
    
    slangs = st.multiselect(
        "select slangs to include",
        slang_options,
        default=["aura", "sigma"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    generate_button = st.button("generate viral script", use_container_width=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 600;">config summary</h4>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">platform</div>
        <div class="metric-value" style="font-size: 1.2rem;">{platform}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">duration</div>
        <div class="metric-value" style="font-size: 1.2rem;">{script_length}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">persona</div>
        <div class="metric-value" style="font-size: 1rem;">{persona}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">slang density</div>
        <div class="metric-value" style="font-size: 1.2rem;">{intensity.upper()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if config_ok and generate_button and topic:
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
    
    with st.status("searching trends", expanded=True) as status:
        try:
            search_tool = TavilySearchResults(k=3)
            results = search_tool.run(f"latest 2025 news and viral facts about {topic}")
            scout_prompt = f"summarize findings for {topic} into 3 viral facts use no emojis only text based on {results}"
            research = llm.invoke([HumanMessage(content=scout_prompt)]).content
            status.update(label="trend research complete", state="complete")
        except Exception as e:
            st.error(f"scout failed {str(e)}")
            st.stop()
    
    with st.spinner("processing aura"):
        try:
            system_instructions = f"""
you are a viral social media scriptwriter

configuration
tone {persona}
visual background {visual_style}
length {script_length}
slang intensity {intensity}
required slangs {', '.join(slangs)}
platform {platform}
music {music_genre}

rules
no emojis allowed at all
format with clear sections hook body call to action
wrap visual instructions in brackets
make it highly engaging and viral worthy
use the research facts provided

research findings
{research}
"""
            
            response = llm.invoke([
                SystemMessage(content=system_instructions),
                HumanMessage(content=f"create a viral {script_length} script about {topic}")
            ])
            script = response.content
            
            aura_prompt = f"respond with only a number from 1 to 1000 representing the viral aura score of this script {script}"
            aura_val = llm.invoke([HumanMessage(content=aura_prompt)]).content.strip()
            
            import random
            base_hashtags = [
                f"#{topic.lower().replace(' ', '')}",
                "#viral", "#trending", "#fyp", "#foryou",
                f"#{platform.lower().replace(' ', '')}",
                "#explore", "#viralvideo", "#trending2025"
            ]
            selected_hashtags = random.sample(base_hashtags, min(hashtag_count, len(base_hashtags)))
            
            estimated_views = f"{random.randint(100, 500)}k {random.randint(1, 3)}m"
            engagement = f"{random.uniform(3, 8):.1f}%"
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">aura score</div>
                    <div class="aura-score">{aura_val}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">est views</div>
                    <div class="metric-value">{estimated_views}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">engagement</div>
                    <div class="metric-value" style="color: #4ade80;">{engagement}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: white; font-weight: 600;">generated script</h4>', unsafe_allow_html=True)
            st.markdown(f'<div class="script-box">{script}</div>', unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: white; font-weight: 600;">hashtags</h4>', unsafe_allow_html=True)
            hashtag_html = ''.join([f'<span class="hashtag-pill">{tag}</span>' for tag in selected_hashtags])
            st.markdown(hashtag_html, unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: white; font-weight: 600;">actions</h4>', unsafe_allow_html=True)
            
            if 'script_text' not in st.session_state:
                st.session_state.script_text = script
            if 'hashtags_text' not in st.session_state:
                st.session_state.hashtags_text = ' '.join(selected_hashtags)
            
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                st.text_area(
                    "script content",
                    value=st.session_state.script_text,
                    height=100,
                    label_visibility="collapsed",
                    key="script_display"
                )
                st.caption("select all and copy ctrl c or cmd c")
            
            with action_col2:
                st.text_area(
                    "hashtag content",
                    value=st.session_state.hashtags_text,
                    height=100,
                    label_visibility="collapsed",
                    key="hashtag_display"
                )
                st.caption("select all and copy ctrl c or cmd c")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"generation failed {str(e)}")

elif generate_button and not topic:
    st.warning("please enter a topic to generate content")