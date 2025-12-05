# Assistente-Financeiro 💳

Uma API backend para gerenciamento de finanças pessoais: controle de compras no cartão de débito e crédito, pagamentos, saldo, faturas mensais e consultas automatizadas.  
Permite inserir, editar, deletar e consultar transações de forma integrada, com automações via webhooks e integração com agentes de IA.

---

## 🚀 Funcionalidades principais

- CRUD completo para compras/transações (cartão de débito e crédito).  
- Gestão de saldo e fatura atual.  
- Suporte a diferentes métodos de pagamento e cartões.  
- Integração com automação (webhooks, bots ou ferramentas externas).  
- Estrutura preparada para orquestração de chamadas e fluxos financeiros.  

   ```

## 🛠️ Tecnologias & Dependências

- Python  
- Web framework: FastAPI  
- Banco de dados: PostgreSQL  
- Containerização / deploy: Docker + docker-compose  
- Estrutura de rotas, models e schemas organizados (padrão MVC / modular)  
- Outras dependências: conforme `requirements.txt`  

   ```

## ⚙️ Como rodar localmente / Instalação

1. Clone o repositório  
   ```bash
   git clone https://github.com/Joao-Pontes22/Assistente-Financeiro.git
   ```
2. Acesse a pasta do projeto
   ```bash
   cd Assistente-Financeiro
   ```

3. Crie e ative um ambiente virtual (opcional, mas recomendado)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / Mac  
   .venv\Scripts\activate      # Windows  
   ```

4. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```
5. Inicie o serviço
   ```bash
   uvicorn main:app --reload
   ```

6. (Opcional) Usando Docker / docker-compose
   ```bash
   docker-compose up --build
   ```
📚 Estrutura do Projeto
   ```bash
   Assistente-Financeiro/
   ├── Routes/         # Rotas da API  
   ├── Models/         # Modelos de dados / ORM  
   ├── Schemes/        # Schemas (Pydantic)  
   ├── Response/       # Classes/respostas da API  
   ├── Dockerfile  
   ├── docker-compose.yml  
   ├── main.py         # Ponto de entrada  
   └── requirements.txt
   ```
## Endpoints

# Expenses
   ```bash
   POST /Expenses/add_expense
   {
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05",
     "Category": "string"
   }
   ```
   ```bash
   DELETE /Expenses/delete_expense
   ?id=123
   ```

   ```bash
   DELETE /Expenses/delete_all_expense
   # Não requer body
   ```
   ```bash
   PUT /Expenses/update_expense
   {
     "Id": 1,
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05",
     "Category": "string"
   }
    ```
   ```bash
   GET /Expenses/View_Expenses
   # Retorna lista das despesas
   ```


# Credit Card
   ```bash
   POST /Credit_card/add_expense_CC
   {
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05",
     "Category": "string"
   }
   ```

   ```bash
   PUT /Credit_card/Update_expense_cc
   {
     "Id": 1,
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05",
     "Category": "string"
   }
   ```
   ```bash
   DELETE /Credit_card/Delete_Expense_cc
   ?id=123
   ```
   ```bash
   DELETE /Credit_card/Delete_All_Expense_cc
   # Não requer body
   ```
   
   ```bash
   GET /Credit_card/View_all_expenses_cc
   # Retorna todas as despesas do cartão
   ```
   ```bash
   GET /Credit_card/View_expenses_cc
   ?filter=value
   ```
   ```bash
   POST /Credit_card/Pay_invoice
   {
     "Value": 0
   }
   ```
   
   # Payment
   ```bash
   POST /Payment/add_Payment
   {
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05"
   }
   ```
   ```bash
   PUT /Payment/Update_Payment
   {
     "Id": 1,
     "Description": "string",
     "Value": 0,
     "Date": "2025-12-05"
   }
   ```
   ```bash
   GET /Payment/Get_all_Payment
   # Lista todos os pagamentos
   ```
   ```bash
   GET /Payment/Get_payment
   ?id=1
   ```
   ```bash
   DELETE /Payment/Delete_Payment
   ?id=1
   ```
   ```bash
   DELETE /Payment/Delete_ALL_Payment
   # Não requer body
   ```
   
   # Management
   ```bash
   GET /Management/Get_in_moment_Management
   # Retorna gerenciamento atual
   ```
   ```bash
   GET /Management/Get_defined_Management
   # Retorna gerenciamento salvo
   ```
   ```bash
   POST /Management/Update_balance_and_invoices
   {
     "Balance": 0,
     "Invoice": 0,
     "Date": "2025-12-05"
   }
   ```
   ```bash
   DELETE /Management/delete_all
   # Remove todos os registros
   ```
   ```bash
   PUT /Management/Update_Management
   {
     "Id": 1,
     "Balance": 0,
     "Invoice": 0,
     "Date": "2025-12-05"
   }
   ```
   
   # Monthly Fee
   ```bash
   GET /Monthly_Fee/Get_Monthly_Fee
   # Retorna mensalidades
   ```
   ```bash
   PUT /Monthly_Fee/Update_status
   {
     "Id": 1,
     "Status": "string"
   }
   ```
   ```bash
   PUT /Monthly_Fee/Update_infos_greater_than
   {
     "Value": 0
   }
   ```
   ```bash
   PUT /Monthly_Fee/Update_infos
   {
     "Id": 1,
     "Description": "string",
     "Value": 0
   }
   ```


