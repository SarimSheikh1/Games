import random
import streamlit as st

# -------------------------------------------------------------------------
# 0) SIMPLE RERUN HELPER USING STREAMLIT'S BUILT-IN API
# -------------------------------------------------------------------------
def do_rerun():
    """
    Force a rerun using Streamlit's built-in st.experimental_rerun().
    This avoids relying on older internal RerunException paths.
    """
    st.experimental_rerun()

# -------------------------------------------------------------------------
# 1) HANGMAN LOGIC
# -------------------------------------------------------------------------
def display_hangman(tries):
    """
    Return a hangman ASCII art depending on the current tries.
    """
    stages = [
        """ 
          😵
          /|\\
          / \\
        """,
        """ 
          😨
          /|\\
          / 
        """,
        """
          😕
          /|\\
        """,
        """
          😐
          /|
        """,
        """
          🙁
          |
        """,
        """
          😶
        """,
        """
          😃
        """
    ]
    # Clamp tries to 0..6 to avoid IndexError
    tries = max(0, min(tries, len(stages) - 1))
    return stages[tries]

def get_word(difficulty):
    """
    Return a random uppercase word from various pools based on difficulty/category.
    """
    easy_words = [
        "cat", "dog", "book", "sun", "car", "tree", "milk", "ball", "bed", "pen",
        "cup", "road", "rain", "star", "bird", "lamb", "cake", "shoe", "fish", "leaf"
    ]
    normal_words = [
        "python", "station", "monitor", "function", "banana", "treadmill", "security",
        "variable", "happiness", "backlog", "meltdown", "ferocious", "developer",
        "parallels", "original", "shipping", "quantify", "essential", "relative", "monkey"
    ]
    hard_words = [
        "metamorphosis", "concurrency", "cryptography", "entrepreneurship", "photosynthesis",
        "conscientious", "synecdoche", "paraphernalia", "phantasmagoria", "multithreading",
        "isomorphism", "questionnaire", "bureaucratic", "philanthropic", "epidemiologist",
        "anthropomorphic", "configuration", "outmaneuver", "reconfiguration", "transubstantiation"
    ]
    pak_cricketer_words = [
        "BABAR", "RIZWAN", "SHAHEEN", "NASEEM", "FAKHAR",
        "ASIF", "HARIS", "SHADAB", "AZHAR", "MISBAH",
        "YOUNIS", "WASIM", "WAQAR", "IMRAN", "SARFRAZ",
        "INZAMAM", "SHOAIB", "AMIR", "HASAN", "RAUF"
    ]
    pak_actor_words = [
        "FAHADMUSTAFA", "HUMAYUNSAEED", "FAWADKHAN", "MAHIRAKHAN", "AYEZAKHAN",
        "SABAQAMAR", "SAJALALY", "IMRANABBAS", "ADNANSIDDIQUI", "SHEHERYARMUNAWAR",
        "OSMANKHALIDBUTT", "AHSANKHAN", "YASIRHUSSAIN", "BILALABBAS", "DANISHTAIMOOR",
        "ZAHIDAHMED", "SAMIKHAN", "MAWRAHOCANE", "HANIAAMIR", "SHEHROZSABZWARI"
    ]
    pak_politician_words = [
        "IMRANKHAN", "NAWAZSHARIF", "ASIFZARDARI", "BILAWALBHUTTO", "MARYAMNAWAZ",
        "SHAHBAZSHARIF", "FAWADCHAUDHRY", "SHEIKHRASHEED", "SHAHMAHMOODQURESHI", "PERVAIZELAHI"
    ]
    pak_singer_words = [
        "ATIFASLAM", "ALIZAFAR", "ABRARULHAQ", "NUSRATFATEHALI", "RAHATFATEHALI",
        "HADIQAKIANI", "MEEKALHASSAN", "FARHANSAEED", "HAROON", "STRINGS"
    ]

    color_words = [
        "RED", "BLUE", "GREEN", "YELLOW", "PURPLE",
        "ORANGE", "PINK", "BROWN", "BLACK", "WHITE",
        "BEIGE", "GRAY", "MAROON", "NAVY", "SILVER",
        "GOLD", "CRIMSON", "CYAN", "MAGENTA", "TURQUOISE"
    ]
    game_words = [
        "CHESS", "CRICKET", "FOOTBALL", "BASKETBALL", "MONOPOLY",
        "PUBG", "VALORANT", "MINECRAFT", "FORTNITE", "HIDEANDSEEK"
    ]
    food_words = [
        "BIRYANI", "PIZZA", "BURGER", "SUSHI", "TACOS",
        "PASTA", "STEAK", "DONUT", "SANDWICH", "NOODLES",
        "ICECREAM", "CURRY", "SAMOSA", "DIMSUM", "WAFFLES",
        "PANCAKES", "PUDDING", "BROWNIES", "FRIES", "LASAGNA"
    ]
    car_words = [
        "TOYOTA", "HONDA", "SUZUKI", "BMW", "MERCEDES",
        "AUDI", "TESLA", "NISSAN", "FORD", "CHEVROLET"
    ]
    drink_words = [
        "WATER", "TEA", "COFFEE", "JUICE", "SODA",
        "LEMONADE", "MILKSHAKE", "MOJITO", "LASSI", "COKE",
        "PEPSI", "FANTA", "SPRITE", "MIRINDA", "GINGERALE",
        "SMOOTHIE", "FRAPPE", "LATTE", "ICEDTEA", "CAPPUCCINO"
    ]
    city_words = [
        "KARACHI", "LAHORE", "ISLAMABAD", "RAWALPINDI", "MULTAN",
        "FAISALABAD", "PESHAWAR", "QUETTA", "GWADAR", "HYDERABAD"
    ]

    if difficulty == "Easy":
        return random.choice(easy_words).upper()
    elif difficulty == "Normal":
        return random.choice(normal_words).upper()
    elif difficulty == "Hard":
        return random.choice(hard_words).upper()
    elif difficulty == "PakCricketer":
        return random.choice(pak_cricketer_words)
    elif difficulty == "PakActor":
        return random.choice(pak_actor_words)
    elif difficulty == "PakPolitician":
        return random.choice(pak_politician_words)
    elif difficulty == "PakSinger":
        return random.choice(pak_singer_words)
    elif difficulty == "Color":
        return random.choice(color_words)
    elif difficulty == "Game":
        return random.choice(game_words)
    elif difficulty == "Food":
        return random.choice(food_words)
    elif difficulty == "Car":
        return random.choice(car_words)
    elif difficulty == "Drink":
        return random.choice(drink_words)
    elif difficulty == "City":
        return random.choice(city_words)
    else:
        return random.choice(easy_words).upper()

# -------------------------------------------------------------------------
# 2) DIFFICULTY (CATEGORY) SELECTION
# -------------------------------------------------------------------------
if "difficulty" not in st.session_state:
    st.title("🎮 Hangman Game 🎮")
    st.subheader(" Dubble Click game ")
    st.subheader("Choose a Difficulty / Category:")

    # ROW 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("😌 Easy"):
            st.session_state.difficulty = "Easy"
    with col2:
        if st.button("😬 Normal"):
            st.session_state.difficulty = "Normal"
    with col3:
        if st.button("😈 Hard"):
            st.session_state.difficulty = "Hard"
    with col4:
        if st.button("🏏 Pak Cricketer"):
            st.session_state.difficulty = "PakCricketer"

    # ROW 2
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("🎬 Pak Actor"):
            st.session_state.difficulty = "PakActor"
    with col6:
        if st.button("🏛️ Pak Politician"):
            st.session_state.difficulty = "PakPolitician"
    with col7:
        if st.button("🎤 Pak Singer"):
            st.session_state.difficulty = "PakSinger"
    with col8:
        if st.button("🌈 Color"):
            st.session_state.difficulty = "Color"

    # ROW 3
    col9, col10, col11, col12 = st.columns(4)
    with col9:
        if st.button("🎮 Game"):
            st.session_state.difficulty = "Game"
    with col10:
        if st.button("🍕 Food"):
            st.session_state.difficulty = "Food"
    with col11:
        if st.button("🚗 Car"):
            st.session_state.difficulty = "Car"
    with col12:
        if st.button("🥤 Drink"):
            st.session_state.difficulty = "Drink"

    # ROW 4
    col13, col14, col15, col16 = st.columns(4)
    with col13:
        if st.button("🌆 City"):
            st.session_state.difficulty = "City"

    st.stop()
else:
    st.sidebar.write(f"🔰 **Selected Category:** {st.session_state.difficulty}")

    # REFRESH BUTTON
    if st.sidebar.button("🔄 Refresh Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        do_rerun()

    # GO BACK BUTTON
    if st.sidebar.button("🔙 Go Back"):
        for key in [
            "difficulty", "word", "word_letters", "guessed_letters",
            "tries", "won", "lost"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        do_rerun()

# -------------------------------------------------------------------------
# 3) INITIALIZE SESSION STATE
# -------------------------------------------------------------------------
if "word" not in st.session_state:
    st.session_state.word = get_word(st.session_state.difficulty)

if "word_letters" not in st.session_state:
    st.session_state.word_letters = set(st.session_state.word)

if "guessed_letters" not in st.session_state:
    st.session_state.guessed_letters = set()

if "tries" not in st.session_state:
    if st.session_state.difficulty == "Easy":
        st.session_state.tries = 8
    else:
        st.session_state.tries = 6

if "won" not in st.session_state:
    st.session_state.won = False

if "lost" not in st.session_state:
    st.session_state.lost = False

# -------------------------------------------------------------------------
# 4) DISPLAY HANGMAN STATE
# -------------------------------------------------------------------------
current_word_display = [
    letter if letter in st.session_state.guessed_letters else "_"
    for letter in st.session_state.word
]

st.markdown(f"**🔠 Word:** {' '.join(current_word_display)}")

#  IMPORTANT FIX HERE (kept on a single line):
st.markdown(f"**🧍 Hangman:**\n{display_hangman(st.session_state.tries)}")

st.write(f"📝 **Guessed Letters:** {', '.join(sorted(st.session_state.guessed_letters))}")
st.write(f"❤️ **Remaining Tries:** {st.session_state.tries}")

# -------------------------------------------------------------------------
# 5) GUESSING A LETTER
# -------------------------------------------------------------------------
if not st.session_state.won and not st.session_state.lost:
    guess = st.text_input("📝 Guess a letter:", max_chars=1).upper()

    if st.button("✅ Submit Guess"):
        if guess:
            # Already guessed
            if guess in st.session_state.guessed_letters:
                st.warning("⚠️ You already guessed that letter! Try another one.")
            # Correct
            elif guess in st.session_state.word_letters:
                st.session_state.guessed_letters.add(guess)
                st.session_state.word_letters.remove(guess)
                st.success(f"🎉 Good job! {guess} is in the word.")
            # Wrong
            else:
                st.session_state.guessed_letters.add(guess)
                if st.session_state.tries > 0:
                    st.session_state.tries -= 1
                st.error(f"❌ Oops! {guess} is not in the word.")

            # Check win/lose
            if len(st.session_state.word_letters) == 0:
                st.session_state.won = True
            if st.session_state.tries == 0:
                st.session_state.lost = True

# -------------------------------------------------------------------------
# 6) END OF GAME MESSAGES & PLAY AGAIN
# -------------------------------------------------------------------------
if st.session_state.won:
    st.balloons()
    st.success(f"🏆 **Congratulations!** You guessed the word: {st.session_state.word}!")
    if st.button("🔄 Play Again"):
        for key in [
            "difficulty", "word", "word_letters", "guessed_letters",
            "tries", "won", "lost"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        do_rerun()

if st.session_state.lost:
    st.error(f"💀 **Game Over!** The word was: {st.session_state.word}")
    if st.button("🔄 Play Again"):
        for key in [
            "difficulty", "word", "word_letters", "guessed_letters",
            "tries", "won", "lost"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        do_rerun()
