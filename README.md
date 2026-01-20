# Agente de Reconhecimento Visual de Produtos Frescos

## 📋 Visão Geral do Projeto

Este projeto consiste num agente inteligente desenvolvido em Python, concebido para automatizar a identificação e inventariação de produtos frescos (frutas e vegetais). O sistema monitoriza uma diretoria específica em tempo real, deteta a entrada de novas imagens, processa-as utilizando um Modelo de Linguagem Multimodal (Google Gemini) e cruza a previsão obtida com uma base de dados local (`picklist.json`).

O objetivo principal é demonstrar a capacidade de modelos de IA generativa na classificação visual de artigos perecíveis e na sua correta correspondência com um inventário fictício.

## 🚀 Arquitetura e Tecnologias

O projeto segue uma arquitetura modular, separando a lógica de monitorização de ficheiros, a interação com a IA e o processamento de dados.

**Stack Tecnológica:**
*   **Linguagem:** Python 3.12+
*   **IA Generativa:** Google Gemini API (Modelo `gemini-3-flash-preview` ou `gemini-2.0-flash` para baixa latência).
*   **Gestão de Ambiente:** `python-dotenv` para segurança de chaves de API.
*   **Estrutura de Dados:** JSON para persistência de dados do inventário.

---

## 🛠️ Documentação Técnica dos Módulos

Abaixo descreve-se a funcionalidade técnica de cada componente do sistema.

### 1. `main.py` - O Orquestrador
Este é o ponto de entrada da aplicação. Gere o fluxo de execução síncrono.
*   **Inicialização:** Carrega o ficheiro de inventário (`processor/picklist.json`) para memória.
*   **Monitorização:** Instancia a classe `FileHandler` para vigiar a diretoria fornecida via argumento de linha de comandos (CLI).
*   **Fluxo de Processamento:**
    1.  Aguarda detetar uma nova imagem na diretoria alvo.
    2.  Lê os *bytes* da imagem.
    3.  Envia os dados para o módulo `brain.py` para inferência.
    4.  Recebe a classificação e invoca `cross_w_picklist` para validar a existência do produto.
    5.  Calcula e apresenta a latência total do processo (`time.perf_counter`).

### 2. `agent/brain.py` - O Cérebro (Integração LLM)
Responsável pela comunicação com a API da Google GenAI.

*   **Método `agent(image_bytes, agent_model, prompt)`:**
    *   **Entrada:** Recebe a imagem em bytes brutos e define o modelo (padrão: `gemini-3-flash-preview`).
    *   **Prompting:** Carrega um prompt "Few-Shot" (`few_shot.txt`) que instrui o modelo a responder estritamente em formato JSON, fornecendo exemplos de classificação correta.
    *   **Execução:** Utiliza a biblioteca `google.genai` para enviar um pedido multimodal (Imagem + Texto).
    *   **Saída:** Retorna uma *string* contendo a resposta do modelo (idealmente um JSON com campos como `fruit`, `PLU`, `Price`).
    *   **Tratamento de Erros:** Inclui sanitização básica da resposta (substituição de plicas por aspas duplas) para garantir um *parsing* JSON válido.

### 3. `processor/FileHandler.py` - Gestor de Ficheiros
Implementa a lógica de observação do sistema de ficheiros (File System Watcher).

*   **Classe `FileHandler`:**
    *   **`__init__(dir)`:** Verifica se a diretoria alvo existe; se não, cria-a automaticamente (`os.makedirs`), garantindo a robustez do ambiente de execução.
    *   **`watch_dir()`:** Implementa um ciclo de *polling* (verificação contínua) com um intervalo de 1 segundo (`time.sleep(1)`). Utiliza a teoria de conjuntos (`novos_ficheiros = ficheiros_atuais - ficheiros_anteriores`) para identificar de forma eficiente ficheiros recém-adicionados, retornando o caminho absoluto da nova imagem.
    
    > **Nota Técnica:** Optou-se por *polling* simples em vez de bibliotecas baseadas em eventos do kernel (como `inotify` ou `watchdog`) para manter as dependências mínimas e a portabilidade do código, dado o escopo do projeto.

### 4. `processor/searcher.py` - Motor de Busca
Responsável pela lógica de correspondência de dados (Data Matching).

*   **Método `cross_w_picklist(picklist, agent_output)`:**
    *   **Parsing:** Converte as strings de entrada (tanto o inventário como a resposta da IA) em dicionários Python (`json.loads`).
    *   **Algoritmo de Busca:** Itera sobre a lista de inventário e verifica se o nome da fruta detetada pela IA está contido no nome do artigo do inventário (`in` operator), ignorando diferenças de maiúsculas/minúsculas (`.lower()`).
    *   **Justificação:** Esta abordagem de "string containment" permite lidar com variações linguísticas (ex: IA deteta "Maçã Gala" e o inventário tem "Maçã Gala Importada").

---

## 📦 Instalação e Utilização

### Pré-requisitos
1.  Python 3.12 ou superior instalado.
2.  Uma chave de API válida para o Google Gemini AI.

### Configuração
1.  Clone o repositório.
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crie um ficheiro `.env` na raiz do projeto:
    ```env
    GEMINI_API_KEY=a_sua_chave_aqui
    ```

### Execução
Execute o ficheiro principal indicando a diretoria onde as imagens serão colocadas:

```bash
python main.py samples/
```

Ao colocar uma imagem (ex: `test.png`) na pasta `samples/`, o agente processará automaticamente o ficheiro e apresentará o resultado no terminal.

---

## 📚 Referências e Decisões Técnicas

1.  **Modelo Gemini Flash:** A escolha de modelos da família "Flash" (ex: `gemini-1.5-flash` ou `gemini-3-flash-preview`) deve-se à sua otimização para tarefas de alta frequência e baixa latência, essenciais para sistemas de reconhecimento em tempo real. [Fonte: Google DeepMind Technical Reports].
2.  **Multimodalidade:** A utilização de um modelo nativamente multimodal dispensa a necessidade de sistemas complexos de OCR ou segmentação de imagem prévia (como YOLO ou Tesseract), permitindo que um único modelo compreenda o contexto visual e semântico.
3.  **JSON para Intercâmbio de Dados:** A utilização de JSON como formato padrão de saída do LLM facilita a integração programática com sistemas de *backend* tradicionais (como o ficheiro `picklist.json`).
