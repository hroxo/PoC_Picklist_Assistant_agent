# Balança Inteligente (Smart Scale) - Documentação Técnica

## 📋 Visão Geral do Sistema

Este repositório contém o código-fonte para a "Balança Inteligente", uma aplicação que simula um sistema de pesagem e faturação automática para retalho alimentar. O sistema utiliza **Visão Computacional** e **Inteligência Artificial Generativa** para identificar frutas e vegetais a partir de imagens, cruzando essa identificação com uma base de dados local de produtos.

A solução está dividida em duas componentes arquiteturais principais:
1.  **Core (Backend Lógico):** Serviços Python puros responsáveis pela lógica de negócio, integração com IA e gestão de dados.
2.  **Interface (Frontend/Web):** Uma aplicação Web desenvolvida em **Django** que fornece a interface de utilizador (UI) para interação com o operador/cliente.

---

## 🏗️ Arquitetura do Sistema

O sistema segue uma arquitetura modular, promovendo a separação de responsabilidades. O diagrama abaixo ilustra o fluxo de dados:

```
[ Interface Web (Django) ]  <--->  [ Camada de Serviços (Core) ]  <--->  [ API Externa (Google Gemini) ]
        ^                                       ^
        |                                       |
  [ Upload de Imagem ]                   [ Base de Dados JSON ]
```

### Estrutura de Diretorias

A organização do projeto reflete esta separação arquitetural:

```
/ (Raiz do Projeto)
├── app/                        # NÚCLEO LÓGICO (CORE)
│   ├── data/                   # Armazenamento de dados estáticos
│   │   └── picklist.json       # Base de dados de produtos (Inventário)
│   ├── src/                    # Código fonte dos serviços de backend
│   │   ├── services/           # Lógica de negócio (IA, Matching, Ficheiros)
│   │   ├── repositories/       # Acesso a dados (Leitura do JSON)
│   │   └── models/             # Definições de objetos de dados
│   └── prompts/                # Instruções de sistema para o modelo de IA
│
├── smart_scale/                # CONFIGURAÇÃO DJANGO
│   ├── settings.py             # Definições globais (Apps, Templates, BD)
│   └── urls.py                 # Rotas principais (URL Dispatcher)
│
├── scale_ui/                   # APLICAÇÃO WEB (UI)
│   ├── views.py                # Controladores: Ligação entre HTML e Core
│   └── urls.py                 # Rotas específicas da interface
│
├── templates/                  # CAMADA DE APRESENTAÇÃO (HTML)
│   ├── base.html               # Layout mestre (Estilos e Estrutura)
│   ├── home.html               # Ecrã de Repouso / Upload
│   └── result.html             # Ecrã de Resultado / Erro
│
├── requirements.txt            # Dependências do projeto
└── manage.py                   # Utilitário de gestão Django
```

## 🛠️ Detalhes Técnicos dos Componentes

### 1. Camada de Apresentação (`scale_ui`)
Desenvolvida em **Django**, esta camada gere o ciclo de vida HTTP.
*   **`views.py`**: Interceta o upload da imagem, converte-a em *bytes* e orquestra as chamadas aos serviços do Core. Implementa lógica de repetição (*retry logic*) para garantir robustez na comunicação com a IA.

### 2. Serviço de Inteligência Artificial (`AIService`)
*Localização: `app/src/services/ai_service.py`*
*   Utiliza a API **Google Gemini** para análise visual.
*   Envia a imagem binária e um *prompt* de sistema (`instruction_heavy.txt`) que instrui o modelo a retornar dados estruturados (JSON).

### 3. Serviço de Correspondência (`MatchingService`)
*Localização: `app/src/services/matching_service.py`*
*   Recebe a saída "bruta" da IA e normaliza os dados.
*   Executa algoritmos de pesquisa textual para encontrar o produto correspondente no ficheiro `picklist.json`.
*   Possui capacidade de **Refinamento**: Se existirem múltiplos candidatos (ex: várias qualidades de maçã), pode solicitar à IA uma segunda análise para desambiguação.

### 4. Repositório de Dados (`PicklistRepository`)
*Localização: `app/src/repositories/picklist_repository.py`*
*   Abstrai o acesso ao ficheiro `picklist.json`. Garante que a aplicação trabalha com objetos Python tipados (`Product`) em vez de dicionários genéricos.

---

## 🚀 Instalação e Execução

### Pré-requisitos
*   Sistema Operativo: Linux, macOS ou Windows.
*   Python 3.10 ou superior.
*   Chave de API Google Gemini válida.

### Passo a Passo

1.  **Configurar Variáveis de Ambiente:**
    Crie um ficheiro `.env` na raiz do projeto:
    ```env
    GEMINI_API_KEY=a_sua_chave_secreta_aqui
    ```

2.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Executar o Servidor Web:**
    Inicie o servidor de desenvolvimento do Django:
    ```bash
    python3 manage.py runserver
    ```

4.  **Aceder à Aplicação:**
    Abra o navegador e visite: `http://127.0.0.1:8000/`

---

## 📝 Notas de Desenvolvimento
*   O sistema não utiliza base de dados SQL tradicional; a persistência é feita via ficheiro JSON para simplicidade de demonstração.
*   O *styling* utiliza CSS nativo com variáveis (`:root`) para facilitar a alteração do esquema de cores (atualmente configurado com o vermelho institucional).