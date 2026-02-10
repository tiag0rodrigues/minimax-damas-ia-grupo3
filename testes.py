import streamlit as st
import MinimaxAlfaBeta
from CheckersGame import CheckersGame
import streamlit.components.v1 as components
import json

def main():
    st.set_page_config(page_title="Tabuleiro de Damas", layout="centered")

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

    if "start_ai" not in st.session_state:
        st.session_state.start_ai = False

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

    # Usa minimax para saber qual o melhor movimento
    if st.session_state.start_ai and st.session_state.state['player'] in ['b', 'B']:
        move = MinimaxAlfaBeta.ALPHA_BETA_SEARCH(game, st.session_state.state, depth=depth)
        if move is not None:
            st.session_state.state = game.RESULT(st.session_state.state, move)
            st.rerun()
    
        

    css_style = """
        <style>
        /* Container principal do tabuleiro */
        .board-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
        }

        .board {
            display: grid;
            grid-template-columns: repeat(8, 60px);
            grid-template-rows: repeat(8, 60px);
            border: 10px solid #5d2906; /* Moldura de madeira escura */
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        /* Estilo das casas */
        .square {
            width: 60px;
            height: 60px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .light-square {
            background-color: #e9c48c; /* Cor de madeira clara */
            background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 2px, transparent 2px, transparent 4px);
        }

        .dark-square {
            background-color: #7b3f00; /* Cor de madeira escura */
            background-image: repeating-linear-gradient(-45deg, rgba(0,0,0,0.1) 0px, rgba(0,0,0,0.1) 2px, transparent 2px, transparent 4px);
        }

        /* Estilo das peças */
        .piece {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.4), inset -2px -2px 4px rgba(0,0,0,0.3);
            position: relative;
        }

        /* Efeito de ranhuras concêntricas nas peças */
        .piece::after {
            content: '';
            position: absolute;
            top: 10%; left: 10%; right: 10%; bottom: 10%;
            border-radius: 50%;
            border: 1px solid rgba(0,0,0,0.1);
            box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
        }

        .black-piece {
            background: radial-gradient(circle at 30% 30%, #444, #111);
            border: 1px solid #000;
        }

        .white-piece {
            background: radial-gradient(circle at 30% 30%, #fff, #d2b48c);
            border: 1px solid #bda078;
        }

        /* Responsividade para telas menores */
        @media (max-width: 600px) {
            .board {
                grid-template-columns: repeat(8, 40px);
                grid-template-rows: repeat(8, 40px);
            }
            .square { width: 40px; height: 40px; }
            .piece { width: 30px; height: 30px; }
        }
        </style>
    """

    st.markdown("""
    <style>
    [class*="dark-square-1"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button){
        width: 68px;
        height: 68px;
        display: flex;
        border-radius: 0%;
        background-color: #7b3f00; /* Cor de madeira escura */
        background-image: repeating-linear-gradient(-45deg, rgba(0,0,0,0.1) 0px, rgba(0,0,0,0.1) 2px, transparent 2px, transparent 4px);
    }        

    [class*="light-square-1"] > .stButton > button[data-testid="stBaseButton-secondary"]:not(.st-key-start_ai_key button){                    
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

    st.title("⚪ Tabuleiro de Damas")
    if st.button("Iniciar jogada da IA", key="start_ai_key"):
        st.session_state.start_ai = True

    cols = st.columns(4, gap="small")
    cols[0].button(" ", key="black-piece-dark-square-1")
    cols[1].button(" ", key="white-piece-dark-square-1")
    cols[2].button(" ", key="dark-square-1")
    cols[3].button(" ", key="light-square-1")
    # Lógica para renderizar o tabuleiro
    def render_board():
        board_html = f'{css_style}<div class="board-container"><div class="board">'
        for i in range(size):
            for j in range(size):
                # 1. Define a cor da casa
                is_dark = (i + j) % 2 != 0
                square_class = "dark-square" if is_dark else "light-square"

                piece_html = ""
                piece_type = st.session_state.state['board'][i][j]

                if piece_type in ['b', 'B']:
                    piece_html = '<div class="piece black-piece"></div>'
                elif piece_type in ['w', 'W']:
                    piece_html = '<div class="piece white-piece"></div>'
                
                board_html += f'<div class="square {square_class}" onclick="sendClick({i}, {j})">{piece_html}</div>'
        
        board_html += '</div></div>'

        # Script JavaScript para comunicar com o Python
        js_script = """
        <script>
        const streamlit = window.Streamlit;

        function sendClick(r, c) {
            streamlit.setComponentValue({
                row: r,
                col: c
            });
        }
        </script>
        """
        return board_html + js_script

    click_data = components.html(render_board(), height=700,)
    st.sidebar.header("Informações")
    st.sidebar.info("Este é um protótipo visual.")
    if click_data is not None and isinstance(click_data, dict):
        if 'row' in click_data and 'col' in click_data:
            st.sidebar.success(" aqui")
            row = click_data['row']
            col = click_data['col']

if __name__ == "__main__":
    main()