import streamlit as st
from main import generate_simple_set


st.title("Swim Set Maker")

level = st.selectbox("Swimmer level", ["beginner", "intermediate", "advanced"])
yards = st.selectbox("Desired yards", [500, 1000, 1500, 2000])
target_type = st.selectbox("Target type", ["main", "total"], index=0)
include_drills = st.checkbox("Include drills in workout", value=False)
seed = st.number_input("Random seed (optional)", value=0, min_value=0)

# If the user requests drills, force total-target mode (drill injection only implemented for total)
if include_drills and target_type != "total":
    st.info("Include drills requires Total target — switching Target type to 'total'.")
    target_type = "total"

if st.button("Generate"):
    if seed != 0:
        import random

        random.seed(int(seed))
    if target_type == "main":
        if include_drills:
            st.info("Including drills is only supported for Target type = 'total' in this version. Choose 'total' to inject drills.")
        warm, main, cool = generate_simple_set(level, yards)
    else:
        # call main's total matching helper by invoking main with args; import here to avoid circular issues
        from main import generate_simple_set as _gs  # ensure main module loaded
        # main.py exposes the total-matching logic via CLI path; call generate_simple_set if target main
        # but we implemented total logic inside main when target-type is used; to reuse, call main.generate_total_matched_set
        try:
            from main import generate_total_matched_set
            warm, main, cool = generate_total_matched_set(level, yards, include_drills=include_drills)
        except Exception:
            # fallback to simple
            warm, main, cool = _gs(level, yards)

    st.subheader("Generated set")
    st.markdown(f"**WARMUP:** {warm[1]} ({warm[0]} yds)")
    # main may be a list of descriptions
    if isinstance(main[1], list):
        st.markdown("**MAIN:**")
        for item in main[1]:
            if isinstance(item, tuple):
                st.markdown(f"- {item[1]}")
            else:
                st.markdown(f"- {item}")
        st.markdown(f"({main[0]} yds)")
    else:
        st.markdown(f"**MAIN:** {main[1]} ({main[0]} yds)")
    st.markdown(f"**COOLDOWN:** {cool[1]} ({cool[0]} yds)")
    total = (warm[0] or 0) + (main[0] or 0) + (cool[0] or 0)
    st.write(f"**Total:** {total} yds")
