import time
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
    "player": "b",  # MAX começa
    "must_capture_with": None,
    "history": set()
}
size = 8
depth = 6
draw_condition = 40
draw_condition_checkers = 10
game = CheckersGame(size)

if "state" not in st.session_state:
    st.session_state.state = initial_state

if "action" not in st.session_state:
    st.session_state.action = ((), ())

if "selected" not in st.session_state:
    st.session_state.selected = None

if "game_over" not in st.session_state:
    st.session_state.game_over = None

if "moves_without_capture" not in st.session_state:
    st.session_state.moves_without_capture = 0

if "last_move_ai" not in st.session_state:
    st.session_state.last_move_ai = "Nenhuma jogada ainda"

if "last_move_player" not in st.session_state:
    st.session_state.last_move_player = "Nenhuma jogada ainda"

st.set_page_config(layout="centered")
st.title("Bem vindo ao Jogo de Damas")

if st.session_state.game_over:
    st.markdown("## 🏆 Fim de Jogo")
    st.error(st.session_state.game_over)

    if st.button("🔄 Reiniciar Partida"):
        st.session_state.state = initial_state
        st.session_state.game_over = None
        st.session_state.last_move_ai = "Nenhuma jogada ainda"
        st.session_state.last_move_player = "Nenhuma jogada ainda"
        st.session_state.moves_without_capture = 0
        st.rerun()

    st.stop()

st.markdown("### 🤖 Última Jogada da IA")
st.write(st.session_state.last_move_ai)


def check_game_over(state):
    board = state["board"]

    white_pieces = []
    black_pieces = []

    for row in board:
        for piece in row:
            if piece in ['w', 'W']:
                white_pieces.append(piece)
            if piece in ['b', 'B']:
                black_pieces.append(piece)

    if not white_pieces:
        return "Pretas venceram!"
    if not black_pieces:
        return "Brancas venceram!"

    possible_moves = game.ACTIONS(state)
    if len(possible_moves) == 0:
        if state["player"] in ['w', 'W']:
            return "Pretas venceram! (Sem movimentos)"
        else:
            return "Brancas venceram! (Sem movimentos)"

    # Empate por estagnação
    if len(white_pieces) == 1 and len(black_pieces) == 1:
        if white_pieces[0] == 'W' and black_pieces[0] == 'B':
            if st.session_state.moves_without_capture >= draw_condition_checkers:
                return "Empate! (1 dama vs 1 dama sem captura)"

    # Empate por muitas jogadas sem capturas
    if st.session_state.moves_without_capture >= draw_condition:
        return "Empate! (Muitas jogadas sem captura)"

    return None

    # Verificar se o jogador atual tem movimentos
    possible_moves = game.ACTIONS(state)
    if len(possible_moves) == 0:
        if state["player"] in ['w', 'W']:
            return "Pretas venceram! (Sem movimentos)"
        else:
            return "Brancas venceram! (Sem movimentos)"

    return None


def valid_move(dest_line, dest_col):
    act = (st.session_state.action[0], (dest_line, dest_col))
    if act in game.ACTIONS(st.session_state.state):
        return True
    return False


def to_notation(pos):
    row, col = pos
    col_letter = chr(ord('a') + col)
    row_number = size - row
    return f"{col_letter}{row_number}"


def coord_to_notation(pos):
    row, col = pos
    letter = chr(ord('a') + col)
    number = 8 - row
    return f"{letter}{number}"


def update_state():
    source, dest = st.session_state.action

    old_board = st.session_state.state["board"]

    old_pieces = sum(
        row.count('b') + row.count('B') +
        row.count('w') + row.count('W')
        for row in old_board
    )

    st.session_state.state = game.RESULT(
        st.session_state.state,
        st.session_state.action
    )

    new_board = st.session_state.state["board"]

    new_pieces = sum(
        row.count('b') + row.count('B') +
        row.count('w') + row.count('W')
        for row in new_board
    )

    if new_pieces < old_pieces:
        move_text = f"{to_notation(source)} → {to_notation(dest)} (captura)"
        st.session_state.moves_without_capture = 0
    else:
        move_text = f"{to_notation(source)} → {to_notation(dest)}"
        st.session_state.moves_without_capture += 1

    st.session_state.last_move_player = move_text

    st.session_state.selected = None
    st.session_state.action = ((), ())

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
            
[class*="selected"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button){
    box-shadow: 
        0 0 0 3px rgba(255, 215, 0, 0.8),
        0 0 15px rgba(255, 215, 0, 0.6);
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
            
[class*="black-king"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div::before  {
    content: '♛';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
    color: white;
    text-shadow: 0 0 5px rgba(0,0,0,0.5);
}
            
[class*="white-king"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div::before  {
    content: '♛';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
    color: black;
    text-shadow: 0 0 5px rgba(0,0,0,0.5);
}
        
[class*="black-piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div{   
    background: radial-gradient(circle at 30% 30%, #444, #111);
    border: 1px solid #000;
}    
        
[class*="white-piece"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button) > div{
    background: radial-gradient(circle at 30% 30%, #fff, #d2b48c);
    border: 1px solid #bda078;
}
</style>
""", unsafe_allow_html=True)

# Renderiza o tabuleiro
top_cols = st.columns(size + 1)
top_cols[0].write("")
for j in range(size):
    top_cols[j + 1].write(chr(ord('a') + j))
for i in range(size):
    cols = st.columns(size + 1)

    cols[0].write(size - i)

    for j in range(size):
        if st.session_state.state['board'][i][j] == ".":
            if (i + j) % 2 != 0:
                if cols[j + 1].button(" ", key=f"dark-square-{i}-{j}") and st.session_state.state['player'] in ['w', 'W'] and st.session_state.action[0] != () and valid_move(i, j):
                    st.session_state.action = (
                        st.session_state.action[0], (i, j))
                    update_state()
            else:
                cols[j + 1].button(" ", key=f"light-square-{i}-{j}")
        elif st.session_state.state['board'][i][j] == 'b':
            cols[j + 1].button(" ", key=f"black-piece-dark-square-{i}-{j}")
        elif st.session_state.state['board'][i][j] == 'B':
            cols[j + 1].button(
                " ", key=f"black-piece-black-king-dark-square-{i}-{j}")
        elif st.session_state.state['board'][i][j] == 'w':
            if (i, j) == st.session_state.selected and cols[j + 1].button(" ", key=f"white-piece-dark-square-selected-{i}-{j}") and st.session_state.state['player'] == 'w':
                st.session_state.selected = (i, j)
                st.session_state.action = ((i, j), ())
                st.rerun()
            elif (i, j) != st.session_state.selected and cols[j + 1].button(" ", key=f"white-piece-dark-square-{i}-{j}") and st.session_state.state['player'] == 'w':
                st.session_state.selected = (i, j)
                st.session_state.action = ((i, j), ())
                st.rerun()
        else:
            if (i, j) == st.session_state.selected and cols[j + 1].button(" ", key=f"white-piece-white-king-dark-square-selected-{i}-{j}") and st.session_state.state['player'] == 'w':
                st.session_state.selected = (i, j)
                st.session_state.action = ((i, j), ())
                st.rerun()
            elif (i, j) != st.session_state.selected and cols[j + 1].button(" ", key=f"white-piece-white-king-dark-square-{i}-{j}") and st.session_state.state['player'] == 'w':
                st.session_state.selected = (i, j)
                st.session_state.action = ((i, j), ())
                st.rerun()

st.markdown("### 👤 Última Jogada do Jogador")
st.write(st.session_state.last_move_player)


if st.session_state.state['player'] == 'b':
    with st.spinner("IA pensando..."):
        time.sleep(0.5)

        move = MinimaxAlfaBeta.ALPHA_BETA_SEARCH(
            game,
            st.session_state.state,
            depth=depth
        )

        if move is not None:
            source, dest = move

            old_board = st.session_state.state["board"]

            old_pieces = sum(
                row.count('b') + row.count('B') +
                row.count('w') + row.count('W')
                for row in old_board
            )

            st.session_state.state = game.RESULT(
                st.session_state.state,
                move
            )

            new_board = st.session_state.state["board"]

            new_pieces = sum(
                row.count('b') + row.count('B') +
                row.count('w') + row.count('W')
                for row in new_board
            )

            if new_pieces < old_pieces:
                move_text = f"{to_notation(source)} → {to_notation(dest)} (captura)"
                st.session_state.moves_without_capture = 0
            else:
                move_text = f"{to_notation(source)} → {to_notation(dest)}"
                st.session_state.moves_without_capture += 1

            st.session_state.last_move_ai = move_text

            result = check_game_over(st.session_state.state)
            if result:
                st.session_state.game_over = result

    st.session_state.selected = None
    st.session_state.action = ((), ())

    st.rerun()

if st.button("🔄 Reiniciar Partida"):
    st.session_state.state = {
        "board": [
            [".", "b", ".", "b", ".", "b", ".", "b"],
            ["b", ".", "b", ".", "b", ".", "b", "."],
            [".", "b", ".", "b", ".", "b", ".", "b"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["w", ".", "w", ".", "w", ".", "w", "."],
            [".", "w", ".", "w", ".", "w", ".", "w"],
            ["w", ".", "w", ".", "w", ".", "w", "."]
        ],
        "player": "b"
    }
    st.session_state.action = ((), ())
    st.session_state.selected = None
    st.session_state.game_over = None
    st.session_state.last_move_ai = "Nenhuma jogada ainda"
    st.session_state.last_move_player = "Nenhuma jogada ainda"
    st.rerun()
