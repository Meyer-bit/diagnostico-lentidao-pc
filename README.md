# 🖥️ Diagnóstico de Lentidão do Sistema (Python)

Projeto em Python que **monitora CPU e RAM em tempo real**, detecta períodos reais de lentidão, identifica **processos suspeitos**, gera um **diagnóstico em linguagem humana** e salva **relatórios automáticos**.

Este projeto foi desenvolvido com foco em **aprendizado prático**, **depuração real** e **boas práticas**, indo além de scripts simples de monitoramento.

---

## 🎯 Objetivo do Projeto

Criar uma ferramenta que responda, de forma clara, à pergunta:

> **“Por que meu computador ficou lento?”**

O sistema não apenas coleta dados, mas:
- Detecta lentidão real (não picos isolados)
- Analisa causas prováveis (CPU vs RAM)
- Identifica processos recorrentes
- Gera relatórios compreensíveis para humanos

---

## 🧠 Conceitos Aplicados

- Monitoramento de recursos com `psutil`
- Detecção por estado (normal → lento → normal)
- Análise estatística simples (médias)
- Tratamento de erros reais (Unicode, fluxo lógico)
- Escrita de arquivos e logs
- Organização de projeto para GitHub

---

## 📁 Estrutura do Projeto

```text
diagnostico-lentidao/
├── monitor.py
├── data/
│   └── logs.csv
├── reports/
│   └── relatorio.txt
└── README.md


## ⚙️ Requisitos

Para executar o projeto, é necessário:

- **Python 3.9 ou superior**
- Biblioteca externa obrigatória:
  - `psutil`

### 📦 Instalação da dependência

Comando:
pip install psutil

---

## ▶️ Como Executar o Projeto

No diretório raiz do projeto, execute o comando abaixo:

Comando:
python monitor.py

Após a execução, o programa permanecerá rodando continuamente, monitorando o uso de CPU e memória RAM do sistema em tempo real.

---

## 🚨 Como o Sistema Detecta Lentidão

A detecção de lentidão **não ocorre com base em picos isolados** de uso de recursos.

Uma lentidão só é considerada quando:

- O uso de **CPU** é maior ou igual ao limite configurado  
OU  
- O uso de **RAM** é maior ou igual ao limite configurado  

E essas condições ocorrem por um número mínimo de leituras consecutivas.

Esse critério evita falsos positivos causados por variações rápidas e momentâneas no uso do sistema.

---

## 🧠 Lógica de Estados do Sistema

O funcionamento do sistema é baseado em uma **máquina de estados**, composta por três estados principais:

### 🟢 Estado Normal
- CPU e RAM estão abaixo dos limites configurados
- O sistema apenas registra os dados de uso
- Nenhum alerta ou relatório é gerado

### 🟡 Estado de Lentidão
- CPU ou RAM permanecem acima do limite por várias leituras
- O sistema entra em modo de análise
- Processos que mais consomem recursos são monitorados
- Estatísticas de uso são acumuladas durante o evento

### 🔵 Retorno ao Normal
- CPU e RAM retornam a níveis aceitáveis
- O evento de lentidão é encerrado
- Um relatório detalhado é gerado automaticamente

---

## 📊 Relatórios Gerados

Sempre que um evento de lentidão termina, o sistema gera um relatório no seguinte caminho:

reports/relatorio.txt

Características dos relatórios:

- O arquivo **não é sobrescrito**
- Cada evento de lentidão gera uma nova entrada
- Contém dados técnicos e uma explicação textual do problema

---

## 🧾 Exemplo de Relatório

==== RELATÓRIO DE LENTIDÃO ====
Início: 2026-01-03 16:43:10  
Fim: 2026-01-03 16:43:38  
Duração: 0:00:28  
CPU média: 87.42%  
RAM média: 71.33%  
Processos: chrome.exe, code.exe  
Diagnóstico: A lentidão foi causada principalmente pelo alto uso da CPU.

---

## 📈 Logs Contínuos

Além dos relatórios de lentidão, o sistema registra logs contínuos de uso de recursos em:

data/logs.csv

Formato do arquivo de log:

timestamp,cpu_percent,ram_percent

Esses registros permitem:

- Análise histórica do desempenho do sistema
- Criação de gráficos
- Exportação para ferramentas externas (como Excel)
- Auditoria do comportamento do computador ao longo do tempo


