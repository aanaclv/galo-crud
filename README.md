# 🌱 GALO - Guia do Agricultor Local

Projeto acadêmico desenvolvido para a disciplina de Programação em Python.

## 📖 Sobre o Projeto

O GALO (Guia do Agricultor Local) é um sistema desenvolvido para auxiliar agricultores familiares na interpretação de laudos de análise de solo.

O sistema transforma informações técnicas em orientações simples e práticas, permitindo que agricultores tomem decisões mais assertivas sobre o manejo da lavoura.

---

## 🎯 Problema

Muitos agricultores familiares recebem relatórios de análise de solo contendo dados técnicos como pH, fósforo (P) e potássio (K), mas encontram dificuldades para interpretar essas informações e convertê-las em ações concretas.

O GALO foi criado para simplificar esse processo, traduzindo os resultados do laudo em recomendações acessíveis e organizadas por prioridade.

---

## 🚀 Funcionalidades

### CRUD de Diagnósticos Agrícolas

- ✅ Cadastrar diagnóstico
- ✅ Consultar diagnósticos
- ✅ Atualizar diagnóstico
- ✅ Excluir diagnóstico

### Funcionalidades Adicionais

- ✅ Análise simplificada do solo
- ✅ Classificação de prioridades
- ✅ Recomendações para o agricultor
- ✅ Armazenamento em arquivo JSON
- ✅ Persistência dos dados após encerrar o sistema
- ✅ Tratamento de erros de entrada

---

## 👨‍🌾 Dados Coletados

### Informações do Agricultor

- Nome
- Nome da propriedade
- Cidade
- Área da propriedade
- Cultura plantada

### Dados do Laudo

- pH
- Fósforo (P)
- Potássio (K)

---

## 📋 Exemplo de Entrada

```text
Nome: José da Silva

Propriedade: Sítio Esperança

Cidade: Caruaru - PE

Área: 5 hectares

Cultura: Milho

pH: 5.2

Fósforo: 8

Potássio: 70
```

---

## 📊 Exemplo de Resultado

```text
============================================================

                 GALO - Guia do Agricultor Local

============================================================

Olá, José da Silva!

Analisamos os dados informados para sua lavoura de milho.

Encontramos 3 oportunidades de melhoria para aumentar sua produtividade.

🔴 PRIORIDADE ALTA
✓ Corrigir a acidez do solo.
✓ Aplicar calcário para melhorar as condições do plantio.

🟡 PRIORIDADE MÉDIA
✓ Reforçar a adubação com fósforo.

🟢 PRIORIDADE BAIXA
✓ Continuar monitorando os níveis de potássio.

============================================================
```

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
- Listas
- Tuplas
- Dicionários
- Manipulação de arquivos
- Tratamento de exceções
- Funções
- CRUD

---

## 🗂️ Estrutura do Projeto

```text
galo/

├── main.py
├── crud.py
├── regras_solo.py
├── arquivo.py
├── utils.py
├── dados.json
└── README.md
```

---

## 🔄 Fluxo do Sistema

```text
Início
   ↓
Menu Principal
   ↓
Cadastrar Diagnóstico
   ↓
Informar Dados do Agricultor
   ↓
Informar Dados do Laudo
   ↓
Analisar Solo
   ↓
Gerar Diagnóstico Simplificado
   ↓
Salvar em JSON
   ↓
Exibir Resultado
   ↓
Consultar / Atualizar / Excluir
   ↓
Fim
```

---

## 💾 Persistência de Dados

Os diagnósticos são armazenados em um arquivo JSON, permitindo que os dados permaneçam disponíveis mesmo após o encerramento do programa.

---

## ✅ Requisitos Acadêmicos Atendidos

| Requisito | Implementação |
|------------|------------|
| Estruturas de decisão | Classificação do solo |
| Estruturas de repetição | Menu principal e consultas |
| Listas | Armazenamento dos diagnósticos |
| Tuplas | Faixas de classificação |
| Dicionários | Representação de diagnósticos |
| Manipulação de arquivos | Arquivo JSON |
| Tratamento de exceções | Validação de entradas |
| CRUD | Cadastro, consulta, atualização e exclusão |

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
