<h1>Jogo de damas contra IA usando Minimax com poda alfa-beta</h1>

<dl>
<dt>Alunos:</dt>
<dd>Tiago Rodrigues dos Santos</dd
</dl>

<h2>Link do app no Hugging Face Spaces</h2>
https://huggingface.co/spaces/tiagorodriguesdev/English-Checkers-AI-Minimax-with-Alpha-Beta-Pruning

<h2>Descrição</h2>

Este projeto tem como objetivo desenvolver uma aplicação de jogo de damas inglesas na qual o jogador enfrenta uma inteligência artificial. A IA será implementada utilizando o algoritmo Minimax com poda alfa-beta, permitindo a tomada de decisões estratégicas e a otimização do desempenho ao reduzir a quantidade de estados analisados na árvore de busca.

A proposta envolve também a criação da interface do jogo usando <strong>Streamlit</strong>.

<h2>Regras de Damas Inglesas</h2>

<ol>
  <li>Movimentação</li>
  <ul>
    <li>Peças comuns só andam na diagonal para frente uma casa por vez</li>
    <li>Damas andam na diagonal para frente e para trás uma casa por vez</li>
  </ul>
  <li>Captura</li>
  <ul>
    <li>Uma peça adversária está em uma casa diagonal adjacente. A casa imediatamente após ela está vazia</li>
    <li>Peças comuns só capturam peças na diagonal para frente</li>
    <li>Damas capturam peças na diagonal para frente e para trás</li>
    <li>A captura é obrigatória</li>
    <li>Se, após uma captura, houver mais uma captura disponível para a mesma peça, é obrigatório realizar a captura até não haver mais capturas disponíveis</li>
  </ul>
  <li>Quando o jogo termina?</li>
  <ul>
    <li>O jogo termina quando todas as peças do adversário são capturadas ou quando há um empate (repetição)</li>
  </ul>
</ol>

<h2>Instalação</h2>

<ol>
  <li>Clonar repositório</li>
  <ul>
    <li>Abra o terminal com diretório dentro da pasta de sua escolha</li>
    <li>Execute o comando: git clone https://github.com/tiag0rodrigues/minimax-damas-ia-grupo3.git</li>
    <li>No terminal, navegue até a pasta do repositório clonado "minimax-damas-ia-grupo3"</li>
  </ul>
  <li>Criar ambiente virtual do Python (venv)</li>
  <ul>
    <li>Para criar, execute o comando: python -m venv venv</li>
    <li>Para ativar, execute o comando: venv\Scripts\activate</li>
  </ul>
  <li>Instalar dependências</li>
  <ul>
    <li>Execute o comando: pip install -r requirements.txt</li>
  </ul>
</ol>

<h3>Para executar a aplicação, use o seguinte comando:</h3>

- streamlit run app_streamlit.py
