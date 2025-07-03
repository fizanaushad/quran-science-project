
import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("science_in_quran_hadith_utf8.csv", encoding='utf-8-sig')
    return df

df = load_data()

# Page title
st.title("📖 Quran & Hadith: Scientific Miracles")
st.markdown("""
Explore how verses from the **Quran** and **Hadith** align with modern **scientific knowledge**.
""")

# Sidebar filter
st.sidebar.header("🔍 Filter")
topics = df["Scientific Topic"].dropna().unique().tolist()
topics.sort()
selected_topic = st.sidebar.selectbox("Choose a scientific topic:", ["All"] + topics)

# Search bar
search_query = st.text_input("🔎 Search by Verse, Arabic, Translation or Scientific Explanation:").strip().lower()

# Filter by topic
if selected_topic != "All":
    filtered_df = df[df["Scientific Topic"] == selected_topic]
else:
    filtered_df = df

# Apply search filter (include Arabic)
if search_query:
    filtered_df = filtered_df[
        df.apply(lambda row: search_query in str(row['Verse/Reference']).lower()
                            or search_query in str(row['Arabic']).lower()
                            or search_query in str(row['Translation']).lower()
                            or search_query in str(row['Explanation']).lower(), axis=1)]

# Display entries
if filtered_df.empty:
    st.warning("No results found. Try another keyword.")
else:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"{row['Verse/Reference']} – {row['Scientific Topic']}"):
            st.markdown(f"**Arabic:** {row['Arabic']}")
            st.markdown(f"**Translation:** {row['Translation']}")
            st.markdown(f"**Scientific Insight:** {row['Explanation']}")
            st.markdown(f"🔗 [Source]({row['Source']})")

st.markdown("---")
st.markdown("Made with ❤️ by Fiza Naushad")
