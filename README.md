FinanSys — Sistema de Controle Financeiro Pessoal

FinanSys é um sistema de controle financeiro pessoal desenvolvido em Python com PySide6 (Qt for Python).
Ele foi criado para ajudar usuários a gerenciar receitas, despesas e relatórios financeiros de forma visual e intuitiva.

Aviso: O backend (banco de dados e persistência de dados) ainda não está funcional nesta versão.
A aplicação atual demonstra apenas a interface gráfica (frontend).

Funcionalidades Atuais

Interface moderna com navegação lateral (sidebar) e design inspirado em dashboards profissionais

Dashboard financeiro com:

Cards de resumo (saldo total, receitas, despesas, economia)

Lista de transações recentes

Área para exibição de gráficos (ainda simulada)

Páginas adicionais:

Transações — visão geral e cards de categorias de gastos

Relatórios — visão de receitas vs. despesas e resumo por categoria

Perfil — exibição de informações do usuário

Design responsivo com layout limpo e uso de ícones emoji para facilitar a leitura

Sistema de navegação com QStackedWidget, permitindo transição entre páginas sem recarregar a janela

Tecnologias Utilizadas
Categoria	Tecnologia
Linguagem	Python 3.10+
Framework GUI	PySide6
Banco de Dados (planejado)	SQLite3
Interface	QMainWindow, QFrame, QListWidget, QStackedWidget, QPushButton, QLabel
Estilo	CSS aplicado via Qt StyleSheets
Estrutura do Projeto
```
FinanSys/
│
├── FinanSys.py          # Código principal da interface gráfica
├── assets/              
└── README.md            
```

Como Executar

Clone ou baixe o repositório:
```
git clone https://github.com/seuusuario/FinanSys.git
cd FinanSys
```


Instale as dependências:

```
pip install PySide6
```

Execute o programa:

python FinanSys.py

Próximos Passos (Planejados)

 Implementar conexão real com banco de dados SQLite

 Criar CRUD completo (Adicionar, Editar, Excluir Transações)

 Adicionar sistema de login com usuários e autenticação

 Gerar relatórios em PDF e Excel

 Inserir gráficos interativos (matplotlib ou Plotly)

 Melhorar design responsivo e animações de interface

Conceito do Projeto

O FinanSys foi idealizado como uma ferramenta prática e elegante para controle financeiro pessoal, permitindo ao usuário visualizar rapidamente sua situação financeira através de painéis e relatórios visuais.
