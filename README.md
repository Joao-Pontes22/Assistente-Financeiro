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

---

## 🛠️ Tecnologias & Dependências

- Python  
- Web framework: FastAPI  
- Banco de dados: PostgreSQL  
- Containerização / deploy: Docker + docker-compose  
- Estrutura de rotas, models e schemas organizados (padrão MVC / modular)  
- Outras dependências: conforme `requirements.txt`  

---

## ⚙️ Como rodar localmente / Instalação

1. Clone o repositório  
   ```bash
   git clone https://github.com/Joao-Pontes22/Assistente-Financeiro.git
   
2. Acesse a pasta do projeto
   ```bash
   cd Assistente-Financeiro


3. Crie e ative um ambiente virtual (opcional, mas recomendado)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / Mac  
   .venv\Scripts\activate      # Windows  


4. Instale as dependências
   ```bash
   pip install -r requirements.txt


5. Inicie o serviço
   ```bash
   uvicorn main:app --reload


6. (Opcional) Usando Docker / docker-compose
   ```bash
   docker-compose up --build

📚 Estrutura do projeto
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

🎯 Caso de uso / Exemplo de uso
   ```bash
   Supondo que a API esteja rodando localmente em http://localhost:8000:
   ```bash
      POST /purchases
      Content-Type: application/json
   
      {
        "card_type": "credit",
        "amount": 150.00,
        "description": "Compra no supermercado",
        "date": "2025-12-04"
      }

Isso criará uma nova transação (compra) no cartão.
Outros endpoints permitem listar transações, editar, deletar, consultar saldo ou fatura, etc.

✅ Boas práticas aplicadas

Código modular e organizado.

Uso de boas práticas na estruturação (models / schemas / rotas separadas).

Possibilidade de deploy via container (Docker).

Fácil manutenção e extensão.

🧩 Possíveis melhorias / Roadmap

Autenticação / Autorização (usuários, tokens).

Integração com sistema de notificação (ex: WhatsApp, e-mail).

Interface front-end / dashboard financeiro.

Histórico de transações pagas / pendentes.

Geração de relatórios / exportação de dados.

📫 Contato / Contribuição

Se quiser contribuir, sugerir melhorias ou reportar problemas, sinta-se à vontade para abrir uma Issue ou Pull Request.
Para dúvidas ou sugestões diretas, entre em contato comigo pelo meu perfil GitHub.
