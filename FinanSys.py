import email
import os.path
import stat
from turtle import title
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox, 
                               QVBoxLayout, QHBoxLayout, QWidget, QFrame, QStackedWidget, QListWidget, 
                               QListWidgetItem, QScrollArea)
from PySide6.QtGui import QPixmap, QPainterPath, QRegion, QFont, QIcon
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QTimer
import sys
import sqlite3

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border-right: 1px solid #34495e;
            }
        """)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header da sidebar
        header = QLabel("FinanSys")
        header.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                border-bottom: 1px solid #2c3e50;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Lista de navegação
        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: #000000;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: #ecf0f1;
                padding: 15px 20px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:hover {
                background-color: #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # Adicionando itens do menu
        menu_items = [
            "🏠 Dashboard",
            "💰 Transações", 
            "📊 Relatórios",
            "👤 Perfil",
            
        ]
        
        for item_text in menu_items:
            item = QListWidgetItem(item_text)
            item.setFont(QFont("Arial", 12))
            self.nav_list.addItem(item)
        
        layout.addWidget(self.nav_list)
        
        # Botão de logout na parte inferior
        logout_btn = QPushButton("🚪 Sair")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.parent().close)
        layout.addWidget(logout_btn)
        
        self.setLayout(layout)

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título do Dashboard
        title = QLabel("🏠 Dashboard")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        # Cards de estatísticas
        stats_layout = QHBoxLayout()
        
        # Card 1 - Saldo Total
        self.saldo_card = self.create_card("💰 Saldo Total", "R$ 15.450,00", "#27ae60")
        stats_layout.addWidget(self.saldo_card)
        
        # Card 2 - Receitas do Mês
        self.receitas_card = self.create_card("📈 Receitas", "R$ 8.200,00", "#3498db")
        stats_layout.addWidget(self.receitas_card)
        
        # Card 3 - Despesas do Mês
        self.despesas_card = self.create_card("📉 Despesas", "R$ 3.750,00", "#e74c3c")
        stats_layout.addWidget(self.despesas_card)
        
        # Card 4 - Economia
        self.economia_card = self.create_card("💎 Economia", "R$ 4.450,00", "#f39c12")
        stats_layout.addWidget(self.economia_card)
        
        layout.addLayout(stats_layout)
        
        # Área de gráficos e tabelas
        content_layout = QHBoxLayout()
        
        # Gráfico simulado
        self.grafico_area = QLabel("📊 Gráfico de Gastos\n\nAqui você pode colocar:\n• Gráficos de pizza\n• Gráficos de barras\n• Gráficos de linha\n• Qualquer widget de visualização")
        self.grafico_area.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 20px;
                color: #2c3e50;
                font-size: 14px;
            }
        """)
        self.grafico_area.setAlignment(Qt.AlignCenter)
        self.grafico_area.setMinimumHeight(300)
        content_layout.addWidget(self.grafico_area, 2)
        
        # Lista de transações recentes
        self.transacoes_widget = QWidget()
        self.transacoes_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
            }
        """)
        transacoes_layout = QVBoxLayout()
        transacoes_layout.setContentsMargins(15, 15, 15, 15)
        
        transacoes_title = QLabel("📋 Transações Recentes")
        transacoes_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        transacoes_layout.addWidget(transacoes_title)
        
        # Lista de transações
        self.transacoes_list = QListWidget()
        self.transacoes_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
        """)
        
        # Adicionando transações de exemplo
        transacoes_exemplo = [
            "🍕 Uber Eats - R$ 45,00",
            "⛽ Posto Shell - R$ 120,00", 
            "💰 Salário - R$ 3.500,00",
            "🛒 Supermercado - R$ 180,00",
            "📱 Netflix - R$ 32,90"
        ]
        
        for transacao in transacoes_exemplo:
            item = QListWidgetItem(transacao)
            self.transacoes_list.addItem(item)
        
        transacoes_layout.addWidget(self.transacoes_list)
        self.transacoes_widget.setLayout(transacoes_layout)
        content_layout.addWidget(self.transacoes_widget, 1)
        
        layout.addLayout(content_layout)
        
        # Botões de ação rápida
        acoes_layout = QHBoxLayout()
        
        btn_nova_transacao = QPushButton("➕ Nova Transação")
        btn_nova_transacao.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        btn_relatorio = QPushButton("📊 Ver Relatório")
        btn_relatorio.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        btn_configurar = QPushButton("⚙️ Configurações")
        btn_configurar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        acoes_layout.addWidget(btn_nova_transacao)
        acoes_layout.addWidget(btn_relatorio)
        acoes_layout.addWidget(btn_configurar)
        acoes_layout.addStretch()
        
        layout.addLayout(acoes_layout)
        self.setLayout(layout)

    def create_card(self, title, value, color):
        """Cria um card de estatística"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                font-weight: normal;
            }
        """)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 24px;
                font-weight: bold;
                margin-top: 5px;
            }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        
        return card

class MainContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
        """)
        self.setup_ui()
    
    def setup_ui(self):
        
        
        # Layout principal com StackedWidget para trocar páginas
        self.stacked_widget = QStackedWidget()
        
        # Página inicial
        self.welcome_page = QLabel("Bem-vindo ao FinanSys!\n\nSelecione uma opção no menu lateral.")
        self.welcome_page.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                padding: 50px;
                background-color: white;
                border-radius: 8px;
                margin: 20px;
            }
        """)
        self.welcome_page.setAlignment(Qt.AlignCenter)
        
        # Dashboard
        self.dashboard = DashboardWidget()
        
        # Adicionando páginas ao stacked widget
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.dashboard)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        
        self.setLayout(layout)











    def create_card(self, title, value, color):
        """Cria um card de estatística (usado nas páginas internas)"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #86868b;
                font-family: 'SF Pro Display';
                font-size: 15px;
                font-weight: 500;
            }
        """)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-family: 'SF Pro Display';
                font-size: 26px;
                font-weight: 700;
                margin-top: 4px;
            }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        return card














class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(1200, 700)
        self.setWindowTitle("FinanSys")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criando a sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.nav_list.itemClicked.connect(self.on_nav_item_clicked)
        
        # Criando a área de conteúdo principal
        self.main_content = MainContentArea(self)
        
        # Adicionando à layout principal
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content)
        
        central_widget.setLayout(main_layout)
        
        # Botões da barra de título (sobrepostos)
        self.btn_mini = QPushButton(self)
        self.btn_mini.setGeometry(20, 8, 23, 23)
        self.btn_mini.setText("-")
        self.btn_mini.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.btn_mini.clicked.connect(self.showMinimized)

        self.btn_fch = QPushButton(self)
        self.btn_fch.setGeometry(50, 8, 23, 23)
        self.btn_fch.setText("X")
        self.btn_fch.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_fch.clicked.connect(self.close)
        
        # Barra de título personalizada
        self.title_bar = QLabel("ㅤ", self)
        self.title_bar.setGeometry(100, 8, 300, 23)
        self.title_bar.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.title_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    
    def on_nav_item_clicked(self, item):
        """Função chamada quando um item do menu é clicado"""
        item_text = item.text()
        print(f"Item clicado: {item_text}")
        
        # Troca de páginas baseado no item selecionado
        if "Dashboard" in item_text:
            self.main_content.stacked_widget.setCurrentWidget(self.main_content.dashboard)
        elif "Transações" in item_text:
            self.create_transacoes_page()
            self.main_content.stacked_widget.setCurrentWidget(self.main_content.transacoes_page)
        elif "Relatórios" in item_text:
            self.create_relatorios_page()
            self.main_content.stacked_widget.setCurrentWidget(self.main_content.relatorios_page)
        elif "Perfil" in item_text:
            self.create_perfil_page()
            self.main_content.stacked_widget.setCurrentWidget(self.main_content.perfil_page)
        


    
    def create_transacoes_page(self):
        """Cria a página de transações"""
        if not hasattr(self.main_content, 'transacoes_page'):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(40,40,40,40)
            layout.setSpacing(20)

            title = QLabel("💰 Transações")
            title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        
            layout.addWidget(title, alignment=Qt.AlignLeft)

            cards_layout = QHBoxLayout()
            cards_layout.setSpacing(15)

            cards_layout.addWidget(self.main_content.create_card("🛒 Compras", "R$ 1.280,00", "#e74c3c"))
            cards_layout.addWidget(self.main_content.create_card("💳 Cartão de Crédito", "R$ 3.420,00", "#3498db"))
            cards_layout.addWidget(self.main_content.create_card("💵 Dinheiro", "R$ 840,00", "#27ae60"))
            cards_layout.addWidget(self.main_content.create_card("📦 Outras Despesas", "R$ 450,00", "#f39c12"))

            layout.addLayout(cards_layout)

            info_label = QLabel("""
            Aqui você pode:
            • Adicionar novas transações  
            • Editar transações existentes  
            • Filtrar por categoria  
            • Exportar dados
            """)

            info_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 16px;
                    font-weight: 500;
                    margin-top: 20px;
                }
            """)

            layout.addWidget(info_label, alignment=Qt.AlignLeft)

            self.main_content.transacoes_page = page 
            self.main_content.stacked_widget.addWidget(self.main_content.transacoes_page)

        

        
    
    def create_relatorios_page(self):
        """Cria a página de relatórios"""
        if not hasattr(self.main_content, 'relatorios_page'):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(40, 40, 40, 40)
            layout.setSpacing(20)

            # Título da página
            title = QLabel("📊 Relatórios")
            title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 15px;
                }
            """)
            layout.addWidget(title, alignment=Qt.AlignLeft)

            # Cards de estatísticas financeiras
            cards_layout = QHBoxLayout()
            cards_layout.setSpacing(15)
            
            # Card 1 - Receita Bruta
            cards_layout.addWidget(self.main_content.create_card("💵 Receita Bruta", "R$ 12.300,00", "#27ae60"))
            
            # Card 2 - Despesas Totais
            cards_layout.addWidget(self.main_content.create_card("💸 Despesas", "R$ 5.800,00", "#e74c3c"))
            
            # Card 3 - Lucro Líquido
            cards_layout.addWidget(self.main_content.create_card("📈 Lucro Líquido", "R$ 6.500,00", "#3498db"))
            
            # Card 4 - Margem de Lucro
            cards_layout.addWidget(self.main_content.create_card("📊 Margem de Lucro", "52.8%", "#9b59b6"))
            
            layout.addLayout(cards_layout)

            # Área de gráficos e análises
            content_layout = QHBoxLayout()
            content_layout.setSpacing(20)
            
            # Gráfico de receitas vs despesas
            grafico_widget = QWidget()
            grafico_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
            grafico_layout = QVBoxLayout(grafico_widget)
            
            grafico_title = QLabel("📈 Receitas vs Despesas")
            grafico_title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 15px;
                    font-weight: bold;
                    margin-bottom: 0px;
                }
            """)
            grafico_layout.addWidget(grafico_title)
            
            # Simulação de gráfico
            grafico_content = QLabel("""
            📊 Gráfico de Barras
            
            Receitas: ████████████ 12.300
            Despesas: ██████ 5.800
            Lucro:    ████████ 6.500
            
            📈 Tendência: +15% este mês
            """)
            grafico_content.setStyleSheet("""
                QLabel {
                    color: #7f8c8d;
                    font-size: 14px;
                    font-family: 'Courier New', monospace;
                    line-height: 1.5;
                }
            """)
            grafico_content.setAlignment(Qt.AlignLeft)
            grafico_layout.addWidget(grafico_content)
            
            content_layout.addWidget(grafico_widget, 2)
            
            # Lista de categorias de gastos
            categorias_widget = QWidget()
            categorias_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
            categorias_layout = QVBoxLayout(categorias_widget)
            
            categorias_title = QLabel("🏷️ Gastos por Categoria")
            categorias_title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 15px;
                    font-weight: bold;
                    margin-bottom: 1px;
                }
            """)
            categorias_layout.addWidget(categorias_title)
            
            # Lista de categorias
            categorias_list = QListWidget()
            categorias_list.setStyleSheet("""
                QListWidget {
                    border: none;
                    background-color: transparent;
                }
                QListWidget::item {
                    padding: 0px;
                    border-bottom: 5px solid #f0f0f0;
                }
            """)
            
            categorias_data = [
                "🛒 Alimentação - R$ 1.200,00 (20.7%)",
                "⛽ Transporte - R$ 800,00 (13.8%)",
                "🏠 Moradia - R$ 1.500,00 (25.9%)",
                "🎮 Lazer - R$ 600,00 (10.3%)",
                "💊 Saúde - R$ 400,00 (6.9%)",
                "📱 Serviços - R$ 300,00 (5.2%)",
                "👕 Roupas - R$ 500,00 (8.6%)",
                "📚 Educação - R$ 500,00 (8.6%)"
            ]
            
            for categoria in categorias_data:
                item = QListWidgetItem(categoria)
                categorias_list.addItem(item)
            
            categorias_layout.addWidget(categorias_list)
            content_layout.addWidget(categorias_widget, 1)
            
            layout.addLayout(content_layout)

            # Informações sobre relatórios
            info_label = QLabel("""
            📋 Funcionalidades dos Relatórios:
            • Gráficos interativos de receitas e despesas
            • Análise de tendências mensais e anuais  
            • Relatórios por categoria de gastos
            • Exportação em PDF e Excel
            • Comparativos entre períodos
            • Metas financeiras e acompanhamento
            """)

            info_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                    font-weight: 650;
                    margin-top: 1px;
                    background-color: #f8f9fa;
                    padding: 0px;
                    border-radius: 8px;
                    border-left: 4px solid #3498db;
                }
            """)

            layout.addWidget(info_label, alignment=Qt.AlignLeft)
            
            # Botões de ação
            botoes_layout = QHBoxLayout()
            
            btn_exportar_pdf = QPushButton("📄 Exportar PDF")
            btn_exportar_pdf.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            
            btn_exportar_excel = QPushButton("📊 Exportar Excel")
            btn_exportar_excel.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """)
            
            btn_atualizar = QPushButton("🔄 Atualizar Dados")
            btn_atualizar.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            
            botoes_layout.addWidget(btn_exportar_pdf)
            botoes_layout.addWidget(btn_exportar_excel)
            botoes_layout.addWidget(btn_atualizar)
            botoes_layout.addStretch()
            
            layout.addLayout(botoes_layout)
            
            self.main_content.relatorios_page = page
            self.main_content.stacked_widget.addWidget(self.main_content.relatorios_page)





    
    def create_perfil_page(self):
        """Cria a página de perfil"""
        if not hasattr(self.main_content, 'perfil_page'):
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.setContentsMargins(40,40,40,40)
                layout.setSpacing(20)

                title = QLabel("👤Perfil")
                title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 15px;
                }
            """)
        
                layout.addWidget(title, alignment=Qt.AlignLeft)

                cards_layout = QHBoxLayout()
                cards_layout.setSpacing(5)

                cards_layout.addWidget(self.main_content.create_card("Nome", "Matheus Provasi", "#e74c3c"))
                cards_layout.addWidget(self.main_content.create_card("Idade", "15", "#3498db"))
                cards_layout.addWidget(self.main_content.create_card("gmail", "provasi123@gmail.com", "#27ae60"))
                cards_layout.addWidget(self.main_content.create_card("genero", "masculino", "#f39c12"))
                
                layout.addLayout(cards_layout)

            

                info_label = QLabel("""
                Aqui você pode:
                • Adicionar novas transações  
                • Editar transações existentes  
                • Filtrar por categoria  
                • Exportar dados
                """)

                info_label.setStyleSheet("""
                    QLabel {
                        color: #2c3e50;
                        font-size: 10px;
                        font-weight: 500;
                        margin-top: 200px;
                    }
                """)

                layout.addWidget(info_label, alignment=Qt.AlignLeft)
                
                


                self.main_content.perfil_page = page
                self.main_content.stacked_widget.addWidget(self.main_content.perfil_page)
    
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mouse_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event): 
        if event.buttons() == Qt.LeftButton and self._mouse_pos is not None:
            self.move(event.globalPosition().toPoint() - self._mouse_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._mouse_pos = None
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())