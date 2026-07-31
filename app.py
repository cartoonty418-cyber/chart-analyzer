import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Candlestick Analyzer", page_icon="📈")

st.title("Candlestick Chart Analyzer AI 📈")
st.write("আপনার চার্টের স্ক্রিনশট আপলোড করুন এবং পরবর্তী ক্যান্ডেলের সম্ভাবনা জানুন।")

# Sidebar for API Key
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

uploaded_file = st.file_uploader("চার্টের স্ক্রিনশট ড্রপ/আপলোড করুন", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_container_width=True)
    
    if st.button("Analyze Chart"):
        if not api_key:
            st.error("দয়া করে সাইডবারে আপনার Gemini API Key দিন!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = """
                You are an expert candlestick and price action trader. Analyze this trading chart image carefully:
                1. Identify current market trend (Uptrend/Downtrend/Sideways).
                2. Identify key Support/Resistance levels or recent candlestick patterns near the latest candle.
                3. Predict the probability of the NEXT candle (Up/Call or Down/Put).
                
                Please format your response strictly as follows:
                - **Market Trend:** [Uptrend/Downtrend/Sideways]
                - **Key Pattern Detected:** [Name of pattern, e.g., Bullish Engulfing, Hammer]
                - **Next Candle Signal:** [CALL / PUT / NEUTRAL]
                - **Probability:** [e.g., 70% Call]
                - **Brief Explanation:** [2-3 sentences reasoning in simple terms]
                """
                
                with st.spinner("ক্যান্ডেলস্টিক এনালাইসিস করা হচ্ছে..."):
                    response = model.generate_content([prompt, image])
                    st.success("Analysis Complete!")
                    st.markdown("### 📊 এনালাইসিস ফলাফল")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
