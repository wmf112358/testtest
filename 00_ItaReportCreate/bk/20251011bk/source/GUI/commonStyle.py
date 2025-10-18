class CommonStyle:
    BUTTON = """
        QPushButton {
            background: #e3f0fa;
            color: #222;
            border: 1px solid #b5d1e8;
            border-radius: 0px;
            min-width: 80px;
            min-height: 32px;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """
    PATTERN_SELECT_CARD ="""
        background: #f7f8fa;
        border: 1px solid #ccc;
        border-radius: 0px;
        margin-left: 40px;
        margin-right: 320px;
    """
    PATTERN_SELECT_BUTTON = """
        QPushButton {
            background: #e3f0fa;
            color: #222;
            border: 1px solid #b5d1e8;
            border-radius: 0px;
            min-width: 160px;
            min-height: 40px;
            margin: 0 28px;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """

    FILE_PATH_SELECT_BUTTON = """
        QPushButton {
            border: 1px solid #888;
            background: #e3f0fa;
            padding: 0 8px;
            border-left: none;
        }
        QPushButton:hover {
            background: #A7D5F7;
        }
    """

    SECTION_SELECT_TABLE = """
        QTableWidget {
            gridline-color: #b5d1e8;
            border: none;
        }
        QHeaderView::section {
            background: #e3f0fa;
            border-top: 1px solid #b5d1e8;
            border-bottom: 1px solid #b5d1e8;
            border-right: 1px solid #b5d1e8;
            color: #222;
            font-weight: bold;
        }
        QHeaderView::section:first {
            border-left: 1px solid #b5d1e8;
        }
    """

    TEXT_BOX = """
        QLineEdit {
            border: 1px solid #888;
            background: #fff;
        }
        QLineEdit:focus {
            border: 1px solid #00B0F0;
            background: #e3f0fa;
        }
    """

    COMBO_BOX = """
        QComboBox {
            border: 1px solid #888;
            background: #fff;
        }
        QComboBox::drop-down {
            border-left: 1px solid #888;
            width: 24px;
        }
        QComboBox::down-arrow {
            image: url(../images/icon3.jpg);
            width: 12px;
            height: 12px;
        }
    """
    SKELETON_COMBO_QLINE_EDIT = """
        QLineEdit:focus {
            border: 1px solid #00B0F0;
            background: #e3f0fa;
        }
    """

    NAV_BAR = """
        background: #d6e7f4;
        color: #222;
        padding: 12px 0 12px 24px;
        border-bottom: 1px solid #ccc;
    """

    TITLE = """
        color: white;
        background-color: #111;
        min-height: 44px;
        max-height: 44px;
        padding-left: 0px;
        padding-right: 0px;
    """

    TITLE_BUTTON = """
        QPushButton {
            background: #111;
            color: #fff;
            border: none;
            min-height: 44px;
            max-height: 44px;
            margin: 0;
            padding: 0;
        }
    """
    BACK_BUTTON = """
        QPushButton {
            background: transparent;
            color: #222;
            border: none; 
            padding: 0 16px 0 0;
        }
        QPushButton:hover {
            color: #00B0F0; 
            text-decoration: underline;
        }
    """
    GRAY_BUTTON = """
        QPushButton {
            background: transparent;
            color: #BFBFBF;
            border: none; 
            padding: 0 16px 0 0;
        }
    """

    CASE_LIST_TABLE_HEADER = """
        QHeaderView { background: #F2F2F2; color: #222; font-weight: bold; }
    """

    CASE_LIST_TABLE = """
        QTableWidget {
            border: none;
            gridline-color: #BFBFBF;
            font-family: Meiryo;
            font-size: 10pt;
        }
        QHeaderView::section {
            background: #F2F2F2;
            color: #222;
            border-width: 0px 1px 1px 0px;  /* 上右下左 */
            border-style: solid;
            border-color: transparent #BFBFBF #BFBFBF transparent;
            font-size: 11pt;
            height: 44px;
        }
        QHeaderView::section:hover, QHeaderView::section:pressed, QHeaderView::section:focus {
            background: #F2F2F2 !important;
        }
        QHeaderView::section:checked {
            background: #F2F2F2 !important;
        }
        QHeaderView {
            background: #F2F2F2;
        }
    """
