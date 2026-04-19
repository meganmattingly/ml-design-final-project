import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify Churn Predictor",
    page_icon="🎵",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Circular+Std&family=DM+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0d0d0d;
    color: #f5f5f5;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #1DB954 0%, #158a3e 60%, #0d0d0d 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "♫";
    position: absolute;
    right: 2rem;
    top: 1rem;
    font-size: 5rem;
    opacity: 0.12;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    color: #fff;
    letter-spacing: -1px;
}
.hero p {
    color: rgba(255,255,255,0.75);
    font-size: 0.85rem;
    margin: 0;
}

/* Section labels */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1DB954;
    margin: 1.5rem 0 0.5rem 0;
    border-left: 3px solid #1DB954;
    padding-left: 0.5rem;
}

/* Result cards */
.result-churn {
    background: linear-gradient(135deg, #5a1010, #2a0000);
    border: 2px solid #e74c3c;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.result-safe {
    background: linear-gradient(135deg, #0f4d20, #002610);
    border: 2px solid #1DB954;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.result-label {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    color: #ffffff !important;
    text-shadow: 0 1px 6px rgba(0,0,0,0.9);
}
.result-sub {
    font-size: 0.85rem;
    color: #dddddd !important;
}

/* Probability bar */
.prob-bar-container {
    background: #1a1a1a;
    border-radius: 99px;
    height: 10px;
    margin: 1rem 0 0.25rem 0;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}

/* Streamlit overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stCheckbox"] label {
    font-size: 0.8rem !important;
    color: #aaa !important;
}
div[data-testid="stButton"] button {
    background-color: #1DB954 !important;
    color: #000 !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 99px !important;
    padding: 0.6rem 2.5rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    margin-top: 1rem;
}
div[data-testid="stButton"] button:hover {
    background-color: #17a349 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎵 Churn Predictor</h1>
    <p>Fill in the user profile below to predict whether they'll cancel their Spotify subscription.</p>
</div>
""", unsafe_allow_html=True)

# ── API health check ──────────────────────────────────────────────────────────
try:
    health = requests.get(f"{API_URL}/health", timeout=3)
    if health.status_code == 200:
        st.success("✅ API connected", icon=None)
    else:
        st.warning("⚠️ API returned unexpected status")
except Exception:
    st.error("❌ Cannot reach API at http://127.0.0.1:8000 — make sure uvicorn is running.")
    st.stop()

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">User Demographics</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("Country", [
        "US", "UK", "DE", "FR", "BR", "IN", "CA", "AU", "MX", "ES", "Other"
    ])
with col2:
    primary_device = st.selectbox("Primary Device", [
        "mobile", "desktop", "tablet", "smart_speaker"
    ])

st.markdown('<p class="section-label">Listening Behaviour</p>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    avg_listening_hours = st.number_input(
        "Avg Listening Hours / Week", min_value=0.0, max_value=168.0, value=10.0, step=0.5
    )
with col4:
    playlists_created = st.number_input(
        "Playlists Created", min_value=0, max_value=500, value=5, step=1
    )

col5, col6, col7 = st.columns(3)
with col5:
    heavy_listener = st.selectbox("Heavy Listener", ["No", "Yes"]) == "Yes"
with col6:
    new_user = st.selectbox("New User", ["No", "Yes"]) == "Yes"
with col7:
    likes_personalization = st.selectbox("Likes Personalization", ["No", "Yes"]) == "Yes"

st.markdown('<p class="section-label">Satisfaction & Features</p>', unsafe_allow_html=True)
music_rating = st.selectbox(
    "Music Suggestion Rating (1–5)",
    options=[1, 2, 3, 4, 5],
    index=2,
    format_func=lambda x: f"{'★' * x}{'☆' * (5 - x)}  ({x})"
)

col8, col9 = st.columns(2)
with col8:
    most_liked_feature = st.selectbox("Most Liked Feature", [
        "playlists", "recommendations", "podcasts", "offline_mode",
        "social_sharing", "audio_quality", "lyrics"
    ])
with col9:
    desired_future_feature = st.selectbox("Desired Future Feature", [
        "offline_mode", "better_recommendations", "lossless_audio",
        "video_content", "social_features", "cheaper_plan", "family_plan"
    ])

dislikes_suggestions = st.selectbox("Dislikes Music Suggestions", ["No", "Yes"]) == "Yes"

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("Predict Churn"):
    payload = {
        "country": country,
        "music_suggestion_rating_1_to_5": music_rating,
        "avg_listening_hours_per_week": avg_listening_hours,
        "most_liked_feature": most_liked_feature,
        "desired_future_feature": desired_future_feature,
        "primary_device": primary_device,
        "playlists_created": playlists_created,
        "likes_personalization": likes_personalization,
        "dislikes_suggestions": dislikes_suggestions,
        "heavy_listener": heavy_listener,
        "new_user": new_user,
    }

    with st.spinner("Running prediction..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

    prediction = result["prediction"]
    label = result["label"]
    prob = result.get("churn_probability", None)

    st.markdown("---")

    if prediction == 1:
        st.markdown(f"""
        <div class="result-churn">
            <div class="result-label">⚠️ Likely to Churn</div>
            <div class="result-sub">This user shows churn risk signals</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-label">✅ Likely to Stay</div>
            <div class="result-sub">This user appears engaged and retained</div>
        </div>
        """, unsafe_allow_html=True)

    if prob is not None:
        pct = int(prob * 100)
        bar_color = "#c0392b" if prediction == 1 else "#1DB954"
        st.markdown(f"""
        <div style="margin-top:1.25rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#aaa;">
                <span>Churn Probability</span>
                <span style="color:{bar_color}; font-weight:600;">{pct}%</span>
            </div>
            <div class="prob-bar-container">
                <div class="prob-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View raw API response"):
        st.json(result)