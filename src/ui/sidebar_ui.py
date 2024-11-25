from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView
from src.utils.constants import ICON_PATH, FONT_PATH
from resources.styles.sidebar_styles import SidebarStyles
from src.services.map_service import MapService


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Configuración inicial de la ventana
        self.setup_window(MainWindow)

        # Configuración de la interfaz principal
        self.setup_main_interface(MainWindow)

        # Configuración de las páginas
        self.setup_pages()

        # Configuración de los menús
        self.setup_full_menu()
        self.setup_icon_menu()

        # Configuración final
        self.setup_final_configurations(MainWindow)

        # Aplicar estilos y efectos
        self.apply_styles_and_effects()

    def setup_window(self, MainWindow):
        font_path = FONT_PATH / "MADE TOMMY Bold_PERSONAL USE.otf"
        self.font_id = QtGui.QFontDatabase.addApplicationFont(str(font_path))

        MainWindow.setObjectName("GeoGrapy")
        MainWindow.setWindowTitle("GeoGrapy")
        MainWindow.resize(1500, 900)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(SidebarStyles.CENTRAL_WIDGET_STYLE)

    def setup_main_interface(self, MainWindow):
        # Grid Layout principal
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        # Widget central
        self.widget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_3.setStyleSheet(SidebarStyles.CENTRAL_WIDGET_STYLE)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)

        # Header
        self.setup_header()

        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)

    def setup_header(self):
        self.header_widget = QtWidgets.QWidget(parent=self.widget_3)
        self.header_widget.setMinimumSize(QtCore.QSize(0, 55))
        self.header_widget.setStyleSheet(SidebarStyles.HEADER_STYLE)

        # Header layout
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.header_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)

        # Botón de cambiar menú
        self.setup_change_button()

        # Espaciador
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.verticalLayout_5.addWidget(self.header_widget)

    def setup_change_button(self):
        self.change_btn = QtWidgets.QPushButton(parent=self.header_widget)
        self.change_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(ICON_PATH / "menu-4-32.ico")))
        self.change_btn.setIcon(icon)
        self.change_btn.setIconSize(QtCore.QSize(14, 14))
        self.change_btn.setCheckable(True)
        self.change_btn.setStyleSheet(SidebarStyles.CHANGE_BTN_STYLE)
        self.horizontalLayout_4.addWidget(self.change_btn)

    def setup_pages(self):
        # StackedWidget para las páginas
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.widget_3)

        # Home con WebView
        self.setup_home_page()

        # Otras páginas
        self.setup_statistics_page()
        self.setup_questions_page()
        self.setup_chat_page()
        self.setup_notes_page()

        self.verticalLayout_5.addWidget(self.stackedWidget)

    def setup_home_page(self):
        self.page = QtWidgets.QWidget()
        self.page_layout = QtWidgets.QVBoxLayout(self.page)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setHtml(MapService.get_map_html())
        self.page_layout.addWidget(self.web_view)

        self.stackedWidget.addWidget(self.page)

    def setup_statistics_page(self):
        self.page_2 = QtWidgets.QWidget()
        self.page_2_layout = QtWidgets.QVBoxLayout(self.page_2)  # Cambiar a QVBoxLayout
        self.page_2_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        self.page_2_layout.setSpacing(0)  # Eliminar espacio entre widgets
        self.stackedWidget.addWidget(self.page_2)

    def setup_questions_page(self):
        self.page_3 = QtWidgets.QWidget()
        self.page_3_layout = QtWidgets.QVBoxLayout(self.page_3)
        self.stackedWidget.addWidget(self.page_3)

    def setup_chat_page(self):
        self.page_4 = QtWidgets.QWidget()
        self.page_4_layout = QtWidgets.QVBoxLayout(self.page_4)
        self.stackedWidget.addWidget(self.page_4)

    def setup_notes_page(self):
        self.page_5 = QtWidgets.QWidget()
        self.page_5_layout = QtWidgets.QVBoxLayout(self.page_5)
        self.stackedWidget.addWidget(self.page_5)

    def setup_full_menu(self):
        # Configuración del menú completo
        self.full_menu_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.full_menu_widget.setMinimumWidth(215)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setContentsMargins(9, 6, 10, 9)

        # Logo y título
        self.setup_full_menu_logo()

        # Botones
        self.setup_full_menu_buttons()

        # Espaciador y botón de salida
        self.setup_full_menu_footer()

        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)

    def setup_full_menu_logo(self):
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        # Logo
        self.logo_label_2 = QtWidgets.QLabel(parent=self.full_menu_widget)
        self.logo_label_2.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label_2.setMaximumSize(QtCore.QSize(50, 50))
        self.logo_label_2.setPixmap(QtGui.QPixmap(str(ICON_PATH / "logo2_preview.png")))
        self.logo_label_2.setScaledContents(True)
        self.horizontalLayout_2.addWidget(self.logo_label_2)

        # Título
        if self.font_id != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(self.font_id)[0]
            self.logo_label_3 = QtWidgets.QLabel("GeoGrapy", parent=self.full_menu_widget)
            self.logo_label_3.setFont(QtGui.QFont(font_family, 20))
            self.logo_label_3.setStyleSheet("color: white;")#Gracias por tant
        else:
            self.logo_label_3 = QtWidgets.QLabel("GeoGrapy", parent=self.full_menu_widget)
            self.logo_label_3.setFont(QtGui.QFont("Arial", 20))
            self.logo_label_3.setStyleSheet("color: white;")#y perdon por tan poco

        self.logo_label_3.setStyleSheet("color: white;")
        self.horizontalLayout_2.addWidget(self.logo_label_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

    def setup_full_menu_buttons(self):
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)

        # Configuración de botones
        buttons_config = [
            ("Inicio", "home-4-32.ico", "home-4-48.ico"),
            ("Estadísticas", "dashboard-5-32.ico", "dashboard-5-48.ico"),
            ("Preguntas", "activity-feed-32.ico", "activity-feed-48.ico"),
            ("ChatGrapy", "product-32.ico", "product-48.ico"),
            ("Apuntes", "group-32.ico", "group-48.ico")
        ]

        self.menu_buttons = []
        for i, (text, icon_off, icon_on) in enumerate(buttons_config):
            button = self.create_menu_button(text, icon_off, icon_on)
            self.menu_buttons.append(button)
            self.verticalLayout_2.addWidget(button)

            # Asignar el primer botón a home_btn_2
            if i == 0:
                self.home_btn_2 = button

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

    def create_menu_button(self, text, icon_off, icon_on):
        button = QtWidgets.QPushButton(text, parent=self.full_menu_widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(ICON_PATH / icon_off)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap(str(ICON_PATH / icon_on)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(20, 20))
        button.setCheckable(True)
        button.setAutoExclusive(True)
        button.setFixedHeight(50)
        button.setStyleSheet(SidebarStyles.BUTTON_STYLE)
        return button

    def setup_full_menu_footer(self):
        spacerItem2 = QtWidgets.QSpacerItem(20, 358,
                                            QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)

        # Botón de salir
        self.exit_btn_2 = QtWidgets.QPushButton("Salir", parent=self.full_menu_widget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(str(ICON_PATH / "close-window-64.ico")))
        self.exit_btn_2.setIcon(icon8)
        self.exit_btn_2.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn_2.setStyleSheet(SidebarStyles.BUTTON_STYLE)
        self.verticalLayout_4.addWidget(self.exit_btn_2)

    def setup_icon_menu(self):
        # Menú completo pero con solo iconos
        self.icon_only_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)

        # Logo
        self.setup_icon_menu_logo()

        # Botones
        self.setup_icon_menu_buttons()

        # Footer
        self.setup_icon_menu_footer()

        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

    def setup_icon_menu_logo(self):
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.logo_label_1 = QtWidgets.QLabel(parent=self.icon_only_widget)
        self.logo_label_1.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setMaximumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setPixmap(QtGui.QPixmap(str(ICON_PATH / "logo2_preview.png")))
        self.logo_label_1.setScaledContents(True)
        self.horizontalLayout_3.addWidget(self.logo_label_1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

    def setup_icon_menu_buttons(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)

        # Crear botones de icono usando los mismos iconos que el menú completo
        self.icon_buttons = []
        for button in self.menu_buttons:
            icon_button = QtWidgets.QPushButton(parent=self.icon_only_widget)
            icon_button.setIcon(button.icon())
            icon_button.setIconSize(QtCore.QSize(20, 20))
            icon_button.setCheckable(True)
            icon_button.setAutoExclusive(True)
            icon_button.setFixedHeight(50)
            icon_button.setStyleSheet(SidebarStyles.ICON_BUTTON_STYLE)
            self.icon_buttons.append(icon_button)
            self.verticalLayout.addWidget(icon_button)

        self.verticalLayout_3.addLayout(self.verticalLayout)

    def setup_icon_menu_footer(self):
        spacerItem3 = QtWidgets.QSpacerItem(20, 360,
                                            QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)

        # Botón de salir
        self.exit_btn_1 = QtWidgets.QPushButton(parent=self.icon_only_widget)
        self.exit_btn_1.setIcon(self.exit_btn_2.icon())
        self.exit_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn_1.setStyleSheet(SidebarStyles.EXIT_BUTTON_STYLE)
        self.verticalLayout_3.addWidget(self.exit_btn_1)

    def setup_final_configurations(self, MainWindow):
        MainWindow.setCentralWidget(self.centralwidget)
        self.setup_connections(MainWindow)
        self.stackedWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def apply_styles_and_effects(self):
        # Aplicar estilos a los widgets principales
        self.full_menu_widget.setStyleSheet(SidebarStyles.FULL_MENU_STYLE)
        self.icon_only_widget.setStyleSheet(SidebarStyles.ICON_ONLY_STYLE)

        # Aplicar efectos de sombra
        self.full_menu_widget.setGraphicsEffect(SidebarStyles.get_shadow_effect())
        self.icon_only_widget.setGraphicsEffect(SidebarStyles.get_shadow_effect())
        self.header_widget.setGraphicsEffect(SidebarStyles.get_bottom_shadow_effect())

    def setup_connections(self, MainWindow):
        # Conexiones para el cambio de visibilidad de menús
        self.change_btn.toggled['bool'].connect(self.icon_only_widget.setVisible)
        self.change_btn.toggled['bool'].connect(self.full_menu_widget.setHidden)

        # Conexiones entre botones de ambos menús
        for icon_btn, full_btn in zip(self.icon_buttons, self.menu_buttons):
            icon_btn.toggled['bool'].connect(full_btn.setChecked)
            full_btn.toggled['bool'].connect(icon_btn.setChecked)

        # Conexiones para cambiar entre páginas
        # Índices de páginas: 0=Home, 1=EstadIsticas, 2=Preguntas, 3=Chat, 4=Creditos
        for i, (icon_btn, menu_btn) in enumerate(zip(self.icon_buttons, self.menu_buttons)):
            page_index = i  # El índice corresponde al orden de las páginas
            icon_btn.clicked.connect(lambda checked, idx=page_index: self.stackedWidget.setCurrentIndex(idx))
            menu_btn.clicked.connect(lambda checked, idx=page_index: self.stackedWidget.setCurrentIndex(idx))

        # Conexiones de los botones de salir
        self.exit_btn_1.clicked.connect(MainWindow.close)
        self.exit_btn_2.clicked.connect(MainWindow.close)
