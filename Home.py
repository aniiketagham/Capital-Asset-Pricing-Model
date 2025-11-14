import streamlit as st
from datetime import date

# --- PAGE SETUP ---
st.set_page_config(
    page_title="CAPM Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown(
    """
    <style>
    /* --- Banner Section --- */
    .banner {
        background: linear-gradient(90deg, #021B79, #0575E6);  /* deep blue to light blue */
        border-radius: 15px;
        padding: 35px 25px;
        text-align: center;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 46px;
        font-weight: 800;
        color: #FFD700;  /* gold */
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #E0FFFF;  /* soft cyan for readability */
        font-weight: 500;
        margin-top: 0;
    }

    /* --- Section Headers --- */
    h2 {
        color: #007BFF;
        margin-top: 30px;
    }

    /* --- Footer --- */
    .footer {
        text-align: center;
        color: grey;
        font-size: 14px;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER BANNER ---
st.markdown(
    """
    <div class="banner">
        <h1 class="main-title">📊 Capital Asset Pricing Model (CAPM)</h1>
        <p class="subtitle">Analyze stock market risk, volatility, and expected return using real-time financial data.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- INTRO SECTION ---
st.markdown(
    """
    ### 💡 What is CAPM?

    The **Capital Asset Pricing Model (CAPM)** is a foundational framework in modern finance that connects 
    a stock's **expected return** with its **systematic risk** (measured as Beta).

    **Formula:**
    > E(R) = R<sub>f</sub> + β × (R<sub>m</sub> − R<sub>f</sub>)

    **Where:**
    - *E(R)* → Expected return of the stock  
    - *R<sub>f</sub>* → Risk-free rate  
    - *β* → Beta (volatility relative to the market)  
    - *R<sub>m</sub>* → Expected market return  

    CAPM helps investors evaluate whether a stock’s return justifies its risk relative to the market.
    """,
    unsafe_allow_html=True
)

st.divider()

# --- FEATURES SECTION ---
st.markdown("## 🚀 Features at a Glance")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### 📈 CAPM Return Analysis  
        - Compare **multiple stocks** side by side  
        - Compute **Beta**, **Alpha**, and **Expected Return**  
        - Visualize **normalized prices** and raw price trends  
        - Generate interactive **Plotly** charts  
        """
    )

with col2:
    st.markdown(
        """
        #### 📉 Calculate Beta  
        - Focus on a **single stock**  
        - Calculate **β**, **α**, and **R²** using linear regression  
        - Measure volatility vs **S&P 500**  
        - Visualize CAPM regression relationships  
        """
    )

st.divider()

# --- TOOLS SECTION ---
st.markdown("## 🧰 Tools & Libraries Used")

tools = {
    "🐍": "Python 3.10+",
    "📊": "Streamlit & Plotly (Interactive UI)",
    "🧮": "Pandas & NumPy (Data Processing)",
    "💹": "Yahoo Finance API (Market Data)",
    "⚙️": "SciPy (Regression & Statistical Analysis)"
}

cols = st.columns(5)
for (emoji, tool), col in zip(tools.items(), cols):
    with col:
        st.markdown(f"### {emoji}")
        st.caption(tool)

st.divider()

# --- NAVIGATION SECTION ---
st.markdown("## 🧭 How to Navigate")

st.markdown(
    """
    - Use the **sidebar** on the left to access:
        - **CAPM Return Analysis** → Multi-stock performance & beta comparison  
        - **Calculate Beta** → Single-stock CAPM computation  
    - Data updates live using **Yahoo Finance API**  
    - Results are cached for speed and efficiency ⚡  
    """
)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    f"""
    <div class="footer">
        Built with ❤️ using <b>Streamlit</b> · Live Data from Yahoo Finance · © {date.today().year} <b>Aniket Agham</b>
    </div>
    """,
    unsafe_allow_html=True
)
