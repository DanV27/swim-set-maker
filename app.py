import streamlit as st
from main import generate_simple_set


st.title("Swim Set Maker")

level = st.selectbox("Swimmer level", ["beginner", "intermediate", "advanced"])
yards = st.selectbox("Desired yards", [500, 1000, 1500, 2000])
seed = st.number_input("Random seed (optional)", value=0, min_value=0)

if st.button("Generate"):
    if seed != 0:
        import random

        random.seed(int(seed))
    warm, main, cool = generate_simple_set(level, yards)
    st.subheader("Generated set")
    st.markdown(f"**WARMUP:** {warm[1]} ({warm[0]} yds)")
    st.markdown(f"**MAIN:** {main[1]} ({main[0]} yds)")
    st.markdown(f"**COOLDOWN:** {cool[1]} ({cool[0]} yds)")
    total = (warm[0] or 0) + (main[0] or 0) + (cool[0] or 0)
    st.write(f"**Total:** {total} yds")
