from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView
from src.ui.chat_page import ChatPage
from src.utils.constants import ICON_PATH, RESOURCE_PATH, FONT_PATH, DATA_PATH
import json
import os
from PyQt6.QtCore import QUrl

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        font_path = FONT_PATH / "MADE TOMMY Bold_PERSONAL USE.otf"
        font_id = QtGui.QFontDatabase.addApplicationFont(str(font_path))

        MainWindow.setObjectName("GeoGrapy")

        MainWindow.resize(1500, 900)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Grid Layout principal
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        # Widget central y su layout
        self.widget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_3.setStyleSheet("background-color: #f5f6fa;")  # Gris muy claro
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)

        # Header widget
        self.header_widget = QtWidgets.QWidget(parent=self.widget_3)
        self.header_widget.setMinimumSize(QtCore.QSize(0, 55))

        # Header layout
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.header_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)

        # Botón de cambiar menú
        self.change_btn = QtWidgets.QPushButton(parent=self.header_widget)
        self.change_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(ICON_PATH / "menu-4-32.ico")))
        self.change_btn.setIcon(icon)
        self.change_btn.setIconSize(QtCore.QSize(14, 14))
        self.change_btn.setCheckable(True)
        self.horizontalLayout_4.addWidget(self.change_btn)

        self.change_btn.setStyleSheet("""
            QPushButton {
                padding: 2px;
                margin-left: 15px;
                width: 30px;
                height: 30px;
            }
        """)

        # Espaciador
        spacerItem = QtWidgets.QSpacerItem(202, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                         QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        # Búsqueda
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)

        self.search_input = QtWidgets.QLineEdit(parent=self.header_widget)
        self.horizontalLayout.addWidget(self.search_input)

        self.search_btn = QtWidgets.QPushButton(parent=self.header_widget)
        self.search_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(ICON_PATH / "search-13-48.ico")))
        self.search_btn.setIcon(icon1)
        self.horizontalLayout.addWidget(self.search_btn)

        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        # Otro espaciador
        spacerItem1 = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                          QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)

        self.verticalLayout_5.addWidget(self.header_widget)

        # StackedWidget para las páginas
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.widget_3)

        # Página 1 - Home con WebView
        self.page = QtWidgets.QWidget()
        self.page_layout = QtWidgets.QVBoxLayout(self.page)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.get_map_html())
        self.page_layout.addWidget(self.web_view)

        self.stackedWidget.addWidget(self.page)

        # Página 2 - Estadísticas
        self.page_2 = QtWidgets.QWidget()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_2)
        self.label_5 = QtWidgets.QLabel("Estadísticas", parent=self.page_2)
        self.label_5.setFont(QtGui.QFont("Arial", 15))
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)

        # Página 3 - Preguntas
        self.page_3 = QtWidgets.QWidget()
        self.page_3_layout = QtWidgets.QVBoxLayout(self.page_3)
        self.stackedWidget.addWidget(self.page_3)

        # Página 4 - ChatBOT
        self.page_4 = QtWidgets.QWidget()
        self.page_4_layout = QtWidgets.QVBoxLayout(self.page_4)
        self.stackedWidget.addWidget(self.page_4)

        # Página 5 - Créditos
        self.page_5 = QtWidgets.QWidget()
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page_5)
        self.label_8 = QtWidgets.QLabel("Créditos", parent=self.page_5)
        self.label_8.setFont(QtGui.QFont("Arial", 15))
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_5)

        # Página 6 - Búsqueda
        self.page_6 = QtWidgets.QWidget()
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_6)
        self.label_9 = QtWidgets.QLabel("Search Page", parent=self.page_6)
        self.label_9.setFont(QtGui.QFont("Arial", 15))
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_7.addWidget(self.label_9, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_6)

        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)

        # Menú completo
        self.full_menu_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)

        # Logo y título en menú completo
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.logo_label_2 = QtWidgets.QLabel(parent=self.full_menu_widget)
        self.logo_label_2.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label_2.setMaximumSize(QtCore.QSize(50, 50))
        self.logo_label_2.setPixmap(QtGui.QPixmap(str(ICON_PATH / "logo2_preview.png")))
        self.logo_label_2.setScaledContents(True)
        self.horizontalLayout_2.addWidget(self.logo_label_2)

        # APLICAR FUENTE A TITULO SIDEBAR
        if font_id != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            self.logo_label_3 = QtWidgets.QLabel("GeoGrapy", parent=self.full_menu_widget)
            self.logo_label_3.setFont(QtGui.QFont(font_family, 20))
        else:
            self.logo_label_3 = QtWidgets.QLabel("GeoGrapy", parent=self.full_menu_widget)
            self.logo_label_3.setFont(QtGui.QFont("Arial", 20))

        self.horizontalLayout_2.addWidget(self.logo_label_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        # Botones del menú completo
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)

        # Home
        self.home_btn_2 = QtWidgets.QPushButton("Inicio", parent=self.full_menu_widget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(str(ICON_PATH / "home-4-32.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon3.addPixmap(QtGui.QPixmap(str(ICON_PATH / "home-4-48.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.home_btn_2.setIcon(icon3)
        self.home_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setAutoExclusive(True)
        self.verticalLayout_2.addWidget(self.home_btn_2)

        # Dashboard
        self.dashboard_btn_2 = QtWidgets.QPushButton("Estadísticas", parent=self.full_menu_widget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(str(ICON_PATH / "dashboard-5-32.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon4.addPixmap(QtGui.QPixmap(str(ICON_PATH / "dashboard-5-48.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.dashboard_btn_2.setIcon(icon4)
        self.dashboard_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.dashboard_btn_2.setCheckable(True)
        self.dashboard_btn_2.setAutoExclusive(True)
        self.verticalLayout_2.addWidget(self.dashboard_btn_2)

        # Preguntas
        self.questions_btn_2 = QtWidgets.QPushButton("Preguntas", parent=self.full_menu_widget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(str(ICON_PATH / "activity-feed-32.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon5.addPixmap(QtGui.QPixmap(str(ICON_PATH / "activity-feed-48.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.questions_btn_2.setIcon(icon5)
        self.questions_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.questions_btn_2.setCheckable(True)
        self.questions_btn_2.setAutoExclusive(True)
        self.verticalLayout_2.addWidget(self.questions_btn_2)

        # Chat
        self.chat_btn_2 = QtWidgets.QPushButton("ChatGrapy", parent=self.full_menu_widget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(str(ICON_PATH / "product-32.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon6.addPixmap(QtGui.QPixmap(str(ICON_PATH / "product-48.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.chat_btn_2.setIcon(icon6)
        self.chat_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.chat_btn_2.setCheckable(True)
        self.chat_btn_2.setAutoExclusive(True)
        self.verticalLayout_2.addWidget(self.chat_btn_2)

        # Créditos
        self.credits_btn_2 = QtWidgets.QPushButton("Créditos", parent=self.full_menu_widget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(str(ICON_PATH / "group-32.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon7.addPixmap(QtGui.QPixmap(str(ICON_PATH / "group-48.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.credits_btn_2.setIcon(icon7)
        self.credits_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.credits_btn_2.setCheckable(True)
        self.credits_btn_2.setAutoExclusive(True)
        self.verticalLayout_2.addWidget(self.credits_btn_2)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        # Espaciador
        spacerItem2 = QtWidgets.QSpacerItem(20, 358, QtWidgets.QSizePolicy.Policy.Minimum,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)

        # Botón de salir en menú completo
        self.exit_btn_2 = QtWidgets.QPushButton("Salir", parent=self.full_menu_widget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(str(ICON_PATH / "close-window-64.ico")))
        self.exit_btn_2.setIcon(icon8)
        self.exit_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.verticalLayout_4.addWidget(self.exit_btn_2)

        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)

        # Menú de solo iconos
        self.icon_only_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)

        # Logo en menú de iconos
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.logo_label_1 = QtWidgets.QLabel(parent=self.icon_only_widget)
        self.logo_label_1.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setMaximumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setPixmap(QtGui.QPixmap(str(ICON_PATH / "logo2_preview.png")))
        self.logo_label_1.setScaledContents(True)
        self.horizontalLayout_3.addWidget(self.logo_label_1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        # Botones del menú de iconos
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)

        # Home
        self.home_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.home_btn_1.setIcon(icon3)
        self.home_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.home_btn_1.setCheckable(True)
        self.home_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.home_btn_1)

        # Dashboard
        self.dashboard_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.dashboard_btn_1.setIcon(icon4)
        self.dashboard_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.dashboard_btn_1.setCheckable(True)
        self.dashboard_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.dashboard_btn_1)

        # Questions
        self.questions_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.questions_btn_1.setIcon(icon5)
        self.questions_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.questions_btn_1.setCheckable(True)
        self.questions_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.questions_btn_1)

        # Chat
        self.chat_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.chat_btn_1.setIcon(icon6)
        self.chat_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.chat_btn_1.setCheckable(True)
        self.chat_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.chat_btn_1)

        # Credits
        self.credits_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.credits_btn_1.setIcon(icon7)
        self.credits_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.credits_btn_1.setCheckable(True)
        self.credits_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.credits_btn_1)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        # Espaciador
        spacerItem3 = QtWidgets.QSpacerItem(20, 360, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)

        # Botón de salir en menú de iconos
        self.exit_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.exit_btn_1.setIcon(icon8)
        self.exit_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.verticalLayout_3.addWidget(self.exit_btn_1)

        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # Conexiones
        self.setup_connections(MainWindow)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Configuración de altura de botones
        self.home_btn_2.setFixedHeight(50)  # Mayor altura
        self.dashboard_btn_2.setFixedHeight(50)
        self.questions_btn_2.setFixedHeight(50)
        self.chat_btn_2.setFixedHeight(50)
        self.credits_btn_2.setFixedHeight(50)

        self.home_btn_1.setFixedHeight(50)  # Mayor altura
        self.dashboard_btn_1.setFixedHeight(50)
        self.questions_btn_1.setFixedHeight(50)
        self.chat_btn_1.setFixedHeight(50)
        self.credits_btn_1.setFixedHeight(50)

        button_style = """
            QPushButton {
                border: none;
                border-radius: 3px;
                text-align: left;
                padding: 8px 0 8px 15px;
                color: #788596;
            }
            QPushButton:hover {
                background-color: rgba(86, 101, 115, 0.5);
            }
            QPushButton:checked {
                color: #fff;
            }
        """

        self.home_btn_2.setStyleSheet(button_style)
        self.dashboard_btn_2.setStyleSheet(button_style)
        self.questions_btn_2.setStyleSheet(button_style)
        self.chat_btn_2.setStyleSheet(button_style)
        self.credits_btn_2.setStyleSheet(button_style)

        self.home_btn_1.setStyleSheet(button_style)
        self.dashboard_btn_1.setStyleSheet(button_style)
        self.questions_btn_1.setStyleSheet(button_style)
        self.chat_btn_1.setStyleSheet(button_style)
        self.credits_btn_1.setStyleSheet(button_style)

        # En sidebar_ui.py, después de crear full_menu_widget:
        self.full_menu_widget.setStyleSheet("""
            background-color: #313a46;
        """)


        # Estilos para widgets principales
        self.full_menu_widget.setStyleSheet("background-color: #313a46;")
        self.icon_only_widget.setStyleSheet("background-color: #313a46; width: 50px;")
        self.header_widget.setStyleSheet("background-color: #313a46;")

    def setup_connections(self, MainWindow):
        self.change_btn.toggled['bool'].connect(self.icon_only_widget.setVisible)
        self.change_btn.toggled['bool'].connect(self.full_menu_widget.setHidden)
        self.home_btn_1.toggled['bool'].connect(self.home_btn_2.setChecked)
        self.dashboard_btn_1.toggled['bool'].connect(self.dashboard_btn_2.setChecked)
        self.questions_btn_1.toggled['bool'].connect(self.questions_btn_2.setChecked)
        self.chat_btn_1.toggled['bool'].connect(self.chat_btn_2.setChecked)
        self.credits_btn_1.toggled['bool'].connect(self.credits_btn_2.setChecked)
        self.home_btn_2.toggled['bool'].connect(self.home_btn_1.setChecked)
        self.dashboard_btn_2.toggled['bool'].connect(self.dashboard_btn_1.setChecked)
        self.questions_btn_2.toggled['bool'].connect(self.questions_btn_1.setChecked)
        self.chat_btn_2.toggled['bool'].connect(self.chat_btn_1.setChecked)
        self.credits_btn_2.toggled['bool'].connect(self.credits_btn_1.setChecked)
        self.exit_btn_2.clicked.connect(MainWindow.close)
        self.exit_btn_1.clicked.connect(MainWindow.close)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoGrapy"))
        self.search_input.setPlaceholderText(_translate("MainWindow", "Buscar..."))
        self.logo_label_3.setText(_translate("MainWindow", "GeoGrapy"))
        self.home_btn_2.setText(_translate("MainWindow", "Inicio"))
        self.dashboard_btn_2.setText(_translate("MainWindow", "Estadísticas"))
        self.questions_btn_2.setText(_translate("MainWindow", "Preguntas"))
        self.chat_btn_2.setText(_translate("MainWindow", "ChatGrapy"))
        self.credits_btn_2.setText(_translate("MainWindow", "Créditos"))
        self.exit_btn_2.setText(_translate("MainWindow", "Salir"))

    def get_map_html(self):
        try:
            # Cargar los datos JSON
            countries_path = os.path.join(DATA_PATH, 'countries.json')
            coordinates_path = os.path.join(DATA_PATH, 'coordinates.json')

            # Cargar los JSON
            with open(countries_path, 'r', encoding='utf-8') as f:
                countries_data = json.load(f)

            with open(coordinates_path, 'r', encoding='utf-8') as f:
                coordinates_data = json.load(f)

            # Leer la plantilla HTML
            with open(str(RESOURCE_PATH / 'styles' / 'index.html'), 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Modificar el HTML para incluir los datos directamente
            html_content = html_content.replace(
                "// REPLACE",
                f"""
                const countriesData = {json.dumps(countries_data)};
                const coordinatesData = {json.dumps(coordinates_data)};
                """
            )

            return html_content

        except Exception as e:
            print(f"Error cargando el mapa: {e}")
            return f"<html><body>Error cargando el mapa: {e}</body></html>"