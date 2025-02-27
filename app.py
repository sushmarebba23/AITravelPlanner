import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("⚠️ Google GenAI API key is missing! Please add it to `.streamlit/secrets.toml`.")
    st.stop()
def get_travel_options(source, destination):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips."
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination}. Suggest travel options with estimated cost, duration, and important details."
    )
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

st.title("🚀 AI-Powered Travel Planner")
st.markdown("Enter your travel details to get AI-generated travel options including cost estimates and travel tips.")

# ✅ User Inputs
source = st.text_input("🛫 Enter Source Location", placeholder="E.g.,  Hyderabad")
destination = st.text_input("🛬 Enter Destination", placeholder="E.g., London")

if st.button("🔍 Find Travel Options"):
    if source.strip() and destination.strip():
        with st.spinner("🔄 Fetching best travel options..."):
            travel_info = get_travel_options(source, destination)
            st.success("✅ Travel Recommendations:")
            st.markdown(travel_info)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")