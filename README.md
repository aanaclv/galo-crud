# 🌱 GALO - Guia do Agricultor Local

Projeto acadêmico desenvolvido para a disciplina de **Fundamentos de Programação** em Python.

## 📖 Sobre o Projeto

O **GALO (Guia do Agricultor Local)** é um sistema CLI em Python desenvolvido para auxiliar agricultores familiares no cadastro de suas propriedades e na interpretação de laudos de análise de solo.

O sistema transforma dados técnicos em orientações simples e práticas, permitindo que agricultores organizem seus terrenos e tomem decisões mais assertivas sobre o manejo da lavoura.

---

## 🎯 Problema

Muitos agricultores familiares recebem relatórios de análise de solo contendo dados técnicos como pH, fósforo (P) e potássio (K), mas encontram dificuldades para interpretar essas informações e convertê-las em ações concretas.

O GALO foi criado para simplificar esse processo, separando o cadastro das propriedades/solos da geração de diagnósticos químicos e traduzindo os resultados do laudo em recomendações acessíveis e organizadas por prioridade.

---

## 🚀 Funcionalidades

### Gerenciamento de Usuários (CRUD e Autenticação)

- ✅ Cadastrar usuário com validação de e-mail e senha (mínimo de 4 caracteres)
- ✅ Login com autenticação via hash (`PBKDF2-HMAC-SHA256`)
- ✅ Consultar perfil formatado no terminal
- ✅ Atualizar dados cadastrais e senha
- ✅ Excluir conta com verificação de vínculos (solos e análises)

### Gerenciamento de Solos (CRUD)

- ✅ Cadastrar solo/propriedade (`propriedade`, `cidade`, `área`, `cultura`)
- ✅ Listar solos cadastrados com formatação visual
- ✅ Consultar solo por ID
- ✅ Atualizar dados do solo
- ✅ Excluir solo (com bloqueio caso existam análises vinculadas)

### Análises e Diagnósticos Agrícolas (CRUD)

- ✅ Selecionar um solo previamente cadastrado pelo usuário para análise
- ✅ Gerar e salvar diagnóstico a partir de pH, fósforo (P) e potássio (K)
- ✅ Classificar pH e definir prioridades para fósforo e potássio
- ✅ Gerar recomendações práticas para o agricultor
- ✅ Listar, consultar, atualizar e excluir análises por ID
- ✅ Persistência local em arquivos JSON (`database/`)
- ✅ Tratamento de erros e normalização de entradas (aceita vírgula ou ponto)

---

## 👨‍🌾 Dados Coletados

### Dados do Usuário

- Nome
- E-mail
- Senha

### Dados do Solo / Propriedade

- Propriedade
- Cidade
- Área (em hectares)
- Cultura plantada

### Dados do Laudo (Análise)

- Solo vinculado (ID da propriedade)
- pH
- Fósforo (P)
- Potássio (K)

---

## 📚 Regras de Negócio

### Avaliação do pH

| Faixa | Diagnóstico |
|---------|---------|
| Menor que 5,5 | Solo Ácido |
| Entre 5,5 e 7,0 | Solo Adequado |
| Acima de 7,0 | Solo Alcalino |

### Avaliação do Fósforo

| Valor | Prioridade |
|---------|---------|
| Menor que 10 | Alta |
| Entre 10 e 20 | Média |
| Acima de 20 | Baixa |

### Avaliação do Potássio

| Valor | Prioridade |
|---------|---------|
| Menor que 50 | Alta |
| Entre 50 e 100 | Média |
| Acima de 100 | Baixa |

---

## 🧠 Conceitos de Python Aplicados

O projeto foi desenvolvido utilizando os conceitos trabalhados em sala:

- Estruturas de decisão (`if`, `elif`, `else`)
- Estruturas de repetição (`for`, `while`)
- Listas e Compreensão de Listas
- Tuplas
- Dicionários
- Modularização (pacotes `entidades/` e `services/`)
- Manipulação de arquivos JSON
- Tratamento de exceções (`try`, `except`, `raise ValueError`)
- Funções e CRUD completo

---

## 🗂️ Estrutura do Projeto

```text
galo-crud/
│
├── database/
│   ├── db_usuario.json
│   ├── db_solo.json
│   └── db_analise.json
│
├── entidades/
│   ├── usuario.py
│   └── solo.py
│
├── services/
│   ├── analise.py
│   └── regras_diagnostico.py
├── ui/
│   ├── formatadores.py
│   └── menus.py
├── db.py
├── main.py
└── README.md
```

---

## ▶️ Como Rodar o Projeto

### 1. Pré-requisitos

- **Python 3.10+** instalado na máquina
- **Git** instalado (opcional, para clonar o repositório)

### 2. Clonar o repositório e acessar a pasta raiz

```bash
git clone https://github.com/aanaclv/galo-crud.git
cd galo-crud
```

*(Caso já tenha o projeto localmente, navegue até a pasta `galo-crud` pelo terminal.)*

### 3. Executar o sistema

Execute o arquivo `main.py` **a partir da raiz `galo-crud`** para garantir que os módulos internos e a pasta `database/` sejam criados e carregados corretamente:

```bash
python main.py
```

*(Em sistemas Linux ou macOS, caso necessário, utilize `python3 main.py`.)*

### 4. Passo a passo de uso no terminal

1. **Criar conta ou entrar:** No menu inicial (`=== G.A.L.O. ===`), escolha `2 - Cadastrar usuário` (senha com no mínimo 4 caracteres) e depois `1 - Login`.
2. **Cadastrar um solo:** Acesse `1 - Solos` -> `1 - Cadastrar solo` e preencha propriedade, cidade, área e cultura.
3. **Gerar uma análise:** Acesse `2 - Análise` -> `1 - Gerar e salvar`, escolha o **ID** do solo desejado na lista exibida e informe `pH`, `Fósforo` e `Potássio`.
4. **Consultar e gerenciar:** Utilize as opções de listagem, consulta por ID, atualização e exclusão nos menus de **Solos**, **Análise** e **Perfil**.

---

## 💾 Persistência de Dados

Os registros de usuários, solos e análises são armazenados em arquivos JSON dentro da pasta `database/` (`db_usuario.json`, `db_solo.json` e `db_analise.json`), permitindo que os dados permaneçam salvos mesmo após o encerramento do programa.

---

## ✅ Requisitos Acadêmicos Atendidos

| Requisito | Implementação |
|------------|------------|
| Estruturas de decisão | Classificação do solo, validações e navegação nos menus |
| Estruturas de repetição | Loops de menus interativos, listagens e buscas |
| Listas | Armazenamento e filtragem de usuários, solos e análises |
| Tuplas | Faixas de classificação e chaves permitidas |
| Dicionários | Representação estruturada de usuários, solos e diagnósticos |
| Manipulação de arquivos | Leitura e escrita persistente em arquivos JSON via `db.py` |
| Tratamento de exceções | Validação de entradas numéricas/textuais e controle de erros |
| CRUD | Cadastro, consulta, atualização e exclusão em múltiplas entidades |

---

## 👥 Equipe

- Ana Beatriz Mergulhão
- Ana Clara Alves
- Cauã Williams Machado
- Isabelly Carneiro Sales
- Rafael Tavares de Melo

---

## 🎓 Disciplina

Fundamentos de Programação

Projeto desenvolvido para fins acadêmicos.
