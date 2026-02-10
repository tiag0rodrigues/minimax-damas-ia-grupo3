import streamlit as st
import MinimaxAlfaBeta
from CheckersGame import CheckersGame

initial_board = [
    [".", "b", ".", "b", ".", "b", ".", "b"],
    ["b", ".", "b", ".", "b", ".", "b", "."],
    [".", "b", ".", "b", ".", "b", ".", "b"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["w", ".", "w", ".", "w", ".", "w", "."],
    [".", "w", ".", "w", ".", "w", ".", "w"],
    ["w", ".", "w", ".", "w", ".", "w", "."]
]
initial_state = {
    "board": initial_board,
    "player": "b"  # MAX começa
}
size = 8
depth = 6
game = CheckersGame(size)

if "state" not in st.session_state:
    st.session_state.state = initial_state
st.set_page_config(layout="wide")
st.title("Bem vindo ao Jogo de Damas")

if "start_ai" not in st.session_state:
    st.session_state.start_ai = False
if st.button("Iniciar jogada da IA"):
    st.session_state.start_ai = True

if "action" not in st.session_state:
    st.session_state.action = ((), ()) 

def valid_move(dest_line, dest_col):
    act = (st.session_state.action[0], (dest_line, dest_col))
    if act in game.ACTIONS(st.session_state.state):
        return True
    return False
        
def update_state():
    st.session_state.state = game.RESULT(st.session_state.state, st.session_state.action)
    st.rerun()

st.markdown("""
<style>
[class*="dark-square"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button){
    width: 68px;
    height: 68px;
    display: flex;
    border-radius: 0%;
    background-color: #7b3f00; /* Cor de madeira escura */
    background-image: repeating-linear-gradient(-45deg, rgba(0,0,0,0.1) 0px, rgba(0,0,0,0.1) 2px, transparent 2px, transparent 4px);
}        

[class*="light-square"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button){                    
    width: 68px;
    height: 68px;
    display: flex;      
    border-radius: 0%;
    background-color: #e9c48c; /* Cor de madeira clara */
    background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 2px, transparent 2px, transparent 4px);
}

[class*="piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div{
    width: 45px;
    height: 45px;
    border-radius: 50%;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.4), inset -2px -2px 4px rgba(0,0,0,0.3);
    position: relative;
}
            
[class*="piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div::after  {
    content: '';
    position: absolute;
    top: 10%; left: 10%; right: 10%; bottom: 10%;
    border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
}
            
        
[class*="black-piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div{   
    background: radial-gradient(circle at 30% 30%, #444, #111);
    border: 1px solid #000;
}    
        
[class*="white-piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div{
    background: radial-gradient(circle at 30% 30%, #fff, #d2b48c);
    border: 1px solid #bda078;
}

[class="st-emotion-cache-13tbzbm"] {
    margin-left: -140px !important;
}
</style>
""", unsafe_allow_html=True)

# Renderiza o tabuleiro
for i in range(size):
    cols = st.columns(size)
    for j in range(size):
        if st.session_state.state['board'][i][j] == ".":
            if (i + j) % 2 != 0:
                if cols[j].button(" ", key=f"dark-square-{i}-{j}") and st.session_state.state['player'] in ['w', ' W'] and st.session_state.action[0] != () and valid_move(i, j):
                    st.session_state.action = (st.session_state.action[0], (i, j)) 
                    update_state()
            else:
                cols[j].button(" ", key=f"light-square-{i}-{j}")
        elif st.session_state.state['board'][i][j] in ['b', 'B']:
            cols[j].button(" ", key=f"black-piece-dark-square-{i}-{j}")
        else:
            if cols[j].button(" ", key=f"white-piece-dark-square-{i}-{j}") and st.session_state.state['player'] in ['w', 'W']:
                st.session_state.action = ((i, j), ())


if st.session_state.start_ai and st.session_state.state['player'] in ['b', 'B']:
    move = MinimaxAlfaBeta.ALPHA_BETA_SEARCH(game, st.session_state.state, depth=depth)
    if move is not None:
        st.session_state.state = game.RESULT(st.session_state.state, move)
        st.rerun()