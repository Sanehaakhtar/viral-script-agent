import os
import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# --- WEB INTERFACE SETUP ---
st.set_page_config(page_title="ViralGen AI", page_icon="🚀")
st.title("🚀 ViralGen: Trend-to-Script")
st.write("I find the latest trends and write a viral TikTok/Insta script for you.")

# --- LOAD SECRETS ---
if "GROQ_API_KEY" in st.secrets and "TAVILY_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
    
    topic = st.text_input("Enter a topic (e.g. AI news, iPhone 16, Fitness hacks):")

    if st.button("Generate Viral Script") and topic:
        with st.spinner("Searching the internet and writing..."):
            try:
                # 1. Setup Brain and Tools
                llm = ChatGroq(model="llama3-70b-8192")
                search_tool = TavilySearchResults()

                # 2. Define the Team
                scout = Agent(
                    role='Trend Scout',
                    goal=f'Find 3 recent trending facts about {topic}.',
                    backstory='You are a master at finding what is trending right now.',
                    tools=[search_tool],
                    llm=llm,
                    verbose=True
                )

                writer = Agent(
                    role='Viral Scriptwriter',
                    goal='Write a high-energy TikTok script with hooks and visual cues.',
                    backstory='You make technical news sound exciting for social media.',
                    llm=llm,
                    verbose=True
                )

                # 3. Define Tasks
                t1 = Task(description=f'Find latest news on {topic}.', agent=scout, expected_output="3 points.")
                t2 = Task(description='Write a script with a HOOK, BODY, and CTA.', agent=writer, expected_output="A script.")

                # 4. Run the Crew
                crew = Crew(agents=[scout, writer], tasks=[t1, t2])
                result = crew.kickoff()
                
                st.success("Done!")
                st.markdown("### 🎬 Your Viral Script:")
                st.write(result.raw)
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.error("Missing API Keys! Please add them to Streamlit Secrets.")