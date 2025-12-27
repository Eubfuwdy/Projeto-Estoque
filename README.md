# 📦 Sistema de Controle de Estoque (ERP Modular)

> Um sistema web full-stack para gestão de inventário com suporte a múltiplas categorias e histórico detalhado de auditoria.

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)
![Badge Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Badge Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey?style=for-the-badge&logo=flask)
![Badge SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

---

## 📋 Sobre o Projeto

Este projeto é um sistema de ERP (Enterprise Resource Planning) focado em controle de estoque, desenvolvido como um estudo de caso de uma aplicação web completa usando Python e Flask.

O diferencial do sistema é sua **arquitetura modular**, permitindo gerenciar diferentes tipos de produtos (atualmente "Periféricos" e "Roupas") com campos dinâmicos que se adaptam à categoria selecionada. Além disso, possui um robusto **sistema de log**, registrando o "antes e depois" de cada alteração crítica.

---

## ✨ Funcionalidades Principais

* **CRUD Completo:** Criação, Leitura, Atualização e Exclusão de produtos.
* **Categorização Modular:**
    * Aba para **Periféricos** (campos padrão).
    * Aba para **Roupas** (campo adicional de "Tamanho").
* **Interface Dinâmica:** O formulário se adapta automaticamente dependendo da categoria selecionada (ex: esconde o campo "Tamanho" para eletrônicos).
* **Busca em Tempo Real:** Filtragem instantânea na tabela sem recarregar a página.
* **Alertas Visuais:** Indicador visual (⚠️ e cor vermelha) para produtos com estoque baixo (menos de 5 unidades).
* **Cálculo Financeiro:** Exibição automática do valor total em estoque (Quantidade × Preço Unitário).
* **Edição Inteligente:** Ao editar, o backend compara os dados novos com os antigos e detecta exatamente o que mudou.
* **Histórico de Auditoria Detalhado:** Registra todas as ações. Em edições, mostra o valor antigo e o novo (ex: `Qtd: 10 -> 15`).

---

## 🛠 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

* **Backend:** Python 3, Flask (Framework Web).
* **Database:** SQLite3 (Banco de dados relacional leve).
* **Frontend:** HTML5, CSS3 (Layout Flexbox e Sidebar), JavaScript (ES6+ para interatividade e Fetch API).

---

## 🗄 Estrutura do Banco de Dados

O projeto utiliza duas tabelas principais no SQLite:

**Tabela `produtos`** (Single Table Inheritance):
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador único |
| `codigo` | TEXT | Código do produto (ex: 0001) |
| `nome` | TEXT | Nome do produto |
| `quantidade`| INTEGER | Qtd em estoque |
| `preco` | REAL | Preço unitário |
| `categoria` | TEXT | 'eletronicos' ou 'roupas' |
| `tamanho` | TEXT | Usado apenas para roupas (pode ser NULL) |

> **Nota:** Existe uma constraint `UNIQUE(codigo, categoria)`, permitindo que o mesmo código exista em categorias diferentes.

**Tabela `historico`**:
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador do log |
| `mensagem` | TEXT | Detalhes da ação realizada |
| `data_hora` | TEXT | Timestamp da ação |

---

## 🚀 Como rodar o projeto localmente

Siga os passos abaixo para executar o sistema na sua máquina.

### Pré-requisitos

* Python 3 instalado.
* Git instalado.

### Passo a passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/MarcosDev23/Projeto-Estoque.git](https://github.com/MarcosDev23/Projeto-Estoque.git)
    ```

2.  **Entre na pasta do projeto:**
    ```bash
    cd Projeto-Estoque
    ```

3.  **Crie e ative um ambiente virtual (Recomendado):**
    * *Linux/Mac:*
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * *Windows:*
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

6.  **Acesse:**
    Abra seu navegador e vá para `http://127.0.0.1:5000/`.

---
