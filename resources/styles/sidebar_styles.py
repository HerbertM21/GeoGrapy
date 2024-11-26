class SidebarStyles:
    BUTTON_STYLE = """
        QPushButton {
            border: none;
            border-radius: 3px;
            text-align: left;
            padding: 8px 0 8px 15px;
            color: #788596;
        }
        QPushButton:hover {
            /*background-color: rgba(86, 101, 115, 0.5);*/
            background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #232c38,
                    stop:0.3 #233836,
                    stop:1 #566573
                );
        }
        QPushButton:checked {
            background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #233836,
                    stop:0.25 #313e4f,
                    stop:1 #039668
                );
            color: #fff;
        }
    """

    EXIT_BUTTON_STYLE = """
        QPushButton {
            border: none;
            border-radius: 3px;
            text-align: center;
            padding: 8px 0;
            color: #fff;
        }
        
        QPushButton:hover {
            background-color: rgba(86, 101, 115, 0.5); /* Hover igual que los demás */
        }
    """

    ICON_BUTTON_STYLE = """
        QPushButton {
            border: none;
            border-radius: 3px;
            text-align: center;
            padding: 8px 0;
            color: #788596;
        }
        QPushButton:hover {
            background-color: rgba(86, 101, 115, 0.5);
        }
        QPushButton:checked {
            background-color: rgba(86, 101, 115, 0.5); /* Igual al hover */
            color: #fff;
        }
    """

    CHANGE_BTN_STYLE = """
        QPushButton {
            border: none;
            border-radius: 3px;
            text-align: center;
            padding: 8px;
            margin-left: 15px;
            width: 30px;
            height: 30px;
            color: #788596;
        }
        QPushButton:hover {
            background-color: rgba(86, 101, 115, 0.5);
        }
        QPushButton:checked {
            color: #fff;
        }
    """

    FULL_MENU_STYLE = """
        background-color: #232c38;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px; 
    """

    ICON_ONLY_STYLE = """
        background-color: #232c38;
        width: 50px;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
    """

    HEADER_STYLE = "background-color: #f5f6fa; "
    CENTRAL_WIDGET_STYLE = "background-color: #f5f6fa;"

    SCROLL_AREA_STYLE = """
        QScrollArea {
            border: none;
            background-color: #F5F6FA;
        }
        QScrollBar:vertical {
            border: none;
            width: 8px;
            background: #F5F6FA;
        }
        QScrollBar::handle:vertical {
            background-color: #B3B3B3;
            border-radius: 4px;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
    """

    @staticmethod
    def get_shadow_effect(blur_radius=15, x_offset=5, y_offset=0, opacity=50):
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setXOffset(x_offset)
        shadow.setYOffset(y_offset)
        shadow.setColor(QColor(0, 0, 0, opacity))
        return shadow

    @staticmethod
    def get_bottom_shadow_effect(blur_radius=8, x_offset=0, y_offset=2, opacity=40):
        return SidebarStyles.get_shadow_effect(blur_radius, x_offset, y_offset, opacity)