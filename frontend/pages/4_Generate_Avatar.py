import streamlit as st
from backend_functions.generate_avatar import generate_avatar


character_option = st.selectbox(
    'What kind of Avatar would you like?',
    ('Wizard', 'Assassin', 'Warrior', 'Android', 'Zombie'),
    index=1,
)

character_era = st.selectbox(
    'What kind of era would you like?',
    ('Futuristic', 'Steampunk', 'Medieval', 'World War 2',
     'Space-Age', 'Prehistoric', 'Post-apocalyptic '),
     index=1,
)

character_gender = st.selectbox(
    'Gender?',
    ('Man', 'Woman', 'Non-Binary Character'),
     index=1,
)


if st.button("Generate Avatar"):
    avatar = generate_avatar(
        character_era=character_era,
        character_option=character_option,
        character_gender=character_gender
    )
    st.image(avatar, caption='Your Avatar from Stability')