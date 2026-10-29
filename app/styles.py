"""
QUANTIX Professional Desktop Design System
Refactored with tabbed sidebars, scroll areas, and responsive desktop distribution.
"""

DARK_THEME_QSS = """
/* ==========================================================================
   GLOBAL DESKTOP FOUNDATION
   ========================================================================== */
QWidget {
    background-color: #131722;
    color: #d1d4dc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
    selection-background-color: #2962ff;
    selection-color: #ffffff;
}

QMainWindow {
    background-color: #0c0e15;
}

/* Tooltips */
QToolTip {
    background-color: #1e222d;
    color: #ffffff;
    border: 1px solid #363a45;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 12px;
}

/* ==========================================================================
   DESKTOP APP HEADER BAR
   ========================================================================== */
#headerBar {
    background-color: #131722;
    border-bottom: 1px solid #2a2e39;
    padding: 6px 14px;
}

#appLogo {
    font-size: 15px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 1px;
}

#appBadge {
    background-color: #1e222d;
    color: #2962ff;
    border: 1px solid #2962ff;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

#tickerBadge {
    background-color: #13241b;
    color: #089981;
    border: 1px solid #089981;
    border-radius: 5px;
    padding: 5px 12px;
    font-weight: 700;
    font-size: 12px;
    font-family: "Consolas", "Cascadia Code", monospace;
}

/* Header Action Buttons */
QPushButton[headerBtn="true"] {
    background-color: #1e222d;
    color: #d1d4dc;
    border: 1px solid #363a45;
    border-radius: 5px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton[headerBtn="true"]:hover {
    background-color: #2a2e39;
    color: #ffffff;
    border-color: #50535e;
}
QPushButton[headerBtn="true"]:pressed {
    background-color: #131722;
}

/* Sidebar Toggle Pills */
QPushButton[toggleBtn="true"] {
    background-color: #181c27;
    color: #9598a1;
    border: 1px solid #2a2e39;
    border-radius: 5px;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 600;
}
QPushButton[toggleBtn="true"]:hover {
    background-color: #222735;
    color: #ffffff;
    border-color: #388bfd;
}

/* ==========================================================================
   METRIC KPI SUMMARY BAR
   ========================================================================== */
#metricsContainer {
    background-color: #131722;
    border-bottom: 1px solid #2a2e39;
    padding: 8px 14px;
}

QFrame[metricCard="true"] {
    background-color: #1e222d;
    border: 1px solid #2a2e39;
    border-radius: 7px;
    padding: 8px 12px;
}
QFrame[metricCard="true"]:hover {
    border-color: #2962ff;
    background-color: #222735;
}

QLabel[metricLabel="true"] {
    color: #787b86;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

QLabel[metricValue="true"] {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    font-family: "Consolas", "Cascadia Code", monospace;
}

QLabel[metricSub="positive"] {
    color: #089981;
    font-size: 11px;
    font-weight: 600;
    font-family: "Consolas", "Cascadia Code", monospace;
}

QLabel[metricSub="negative"] {
    color: #f23645;
    font-size: 11px;
    font-weight: 600;
    font-family: "Consolas", "Cascadia Code", monospace;
}

/* ==========================================================================
   SIDEBAR TABS & SCROLL AREAS
   ========================================================================== */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}

/* Sidebar Tab Widget */
QTabWidget[sidebarTabs="true"]::pane {
    border: 1px solid #2a2e39;
    background-color: #181c27;
    border-radius: 7px;
    top: -1px;
    padding: 10px;
}

QTabWidget[sidebarTabs="true"] QTabBar::tab {
    background-color: #131722;
    color: #787b86;
    border: 1px solid #2a2e39;
    border-bottom: none;
    padding: 6px 12px;
    margin-right: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    font-weight: 600;
    font-size: 11px;
}
QTabWidget[sidebarTabs="true"] QTabBar::tab:selected {
    background-color: #181c27;
    color: #2962ff;
    border-bottom: 2px solid #2962ff;
}
QTabWidget[sidebarTabs="true"] QTabBar::tab:hover:!selected {
    color: #d1d4dc;
    background-color: #1c212e;
}

/* Section Cards inside tabs */
QFrame[sectionCard="true"] {
    background-color: #1e222d;
    border: 1px solid #2a2e39;
    border-radius: 7px;
    padding: 10px;
}

QLabel[sectionTitle="true"] {
    color: #9598a1;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 2px;
}

QLabel[fieldLabel="true"] {
    color: #b2b5be;
    font-size: 12px;
    font-weight: 500;
}

/* ==========================================================================
   FORM CONTROLS (Crisp, High Contrast, Perfectly Padded)
   ========================================================================== */
QComboBox {
    background-color: #131722;
    color: #ffffff;
    border: 1px solid #363a45;
    border-radius: 5px;
    min-height: 32px;
    height: 32px;
    padding-left: 10px;
    padding-right: 28px;
    font-size: 12px;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #50535e;
    background-color: #171b26;
}
QComboBox:focus {
    border-color: #2962ff;
    background-color: #171b26;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #2a2e39;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #181c27;
}
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #9598a1;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #1e222d;
    color: #ffffff;
    border: 1px solid #363a45;
    border-radius: 5px;
    selection-background-color: #2962ff;
    selection-color: #ffffff;
    padding: 4px;
    outline: none;
    font-size: 12px;
}

/* SpinBoxes */
QSpinBox, QDoubleSpinBox, QLineEdit {
    background-color: #131722;
    color: #ffffff;
    border: 1px solid #363a45;
    border-radius: 5px;
    min-height: 32px;
    height: 32px;
    padding-left: 10px;
    padding-right: 26px;
    font-size: 12px;
    font-weight: 600;
    font-family: "Consolas", "Cascadia Code", monospace;
}
QSpinBox:hover, QDoubleSpinBox:hover, QLineEdit:hover {
    border-color: #50535e;
    background-color: #171b26;
}
QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
    border-color: #2962ff;
    background-color: #171b26;
}
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    height: 15px;
    border-left: 1px solid #2a2e39;
    border-bottom: 1px solid #2a2e39;
    border-top-right-radius: 4px;
    background-color: #181c27;
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {
    background-color: #2962ff;
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-bottom: 4px solid #d1d4dc;
    width: 0;
    height: 0;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    height: 15px;
    border-left: 1px solid #2a2e39;
    border-bottom-right-radius: 4px;
    background-color: #181c27;
}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #2962ff;
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-top: 4px solid #d1d4dc;
    width: 0;
    height: 0;
}

/* ==========================================================================
   SEGMENTED TIMEFRAME CONTROL
   ========================================================================== */
#timeframeBar {
    background-color: #131722;
    border: 1px solid #363a45;
    border-radius: 5px;
    padding: 2px;
}

QPushButton[tfSegment="true"] {
    background-color: transparent;
    color: #9598a1;
    border: none;
    border-radius: 4px;
    height: 26px;
    font-size: 11px;
    font-weight: 600;
}
QPushButton[tfSegment="true"]:hover {
    color: #ffffff;
    background-color: #1e222d;
}
QPushButton[tfSegment="true"]:checked {
    background-color: #2962ff;
    color: #ffffff;
    font-weight: 700;
}

/* ==========================================================================
   PRIMARY ACTION CTA
   ========================================================================== */
QPushButton[runCTA="true"] {
    background-color: #089981;
    color: #ffffff;
    border: 1px solid #0bb397;
    border-radius: 6px;
    min-height: 40px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.8px;
}
QPushButton[runCTA="true"]:hover {
    background-color: #0bb397;
}
QPushButton[runCTA="true"]:pressed {
    background-color: #067a67;
}

/* AI Action Chips */
QPushButton[aiChip="true"] {
    background-color: #1e222d;
    color: #93c5fd;
    border: 1px solid #2a2e39;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 11px;
    font-weight: 500;
    text-align: left;
}
QPushButton[aiChip="true"]:hover {
    background-color: #222a3a;
    border-color: #2962ff;
    color: #ffffff;
}

/* ==========================================================================
   CENTRAL TAB WORKSPACE
   ========================================================================== */
QTabWidget[mainTabs="true"]::pane {
    border: 1px solid #2a2e39;
    background-color: #131722;
    border-radius: 7px;
    top: -1px;
}

QTabWidget[mainTabs="true"] QTabBar::tab {
    background-color: #131722;
    color: #787b86;
    border: 1px solid #2a2e39;
    border-bottom: none;
    padding: 8px 16px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    font-size: 12px;
}
QTabWidget[mainTabs="true"] QTabBar::tab:selected {
    background-color: #1e222d;
    color: #2962ff;
    border-bottom: 2px solid #2962ff;
}
QTabWidget[mainTabs="true"] QTabBar::tab:hover:!selected {
    color: #d1d4dc;
    background-color: #181c27;
}

/* ==========================================================================
   DATA TABLES
   ========================================================================== */
QTableWidget {
    background-color: #131722;
    gridline-color: #1e222d;
    border: 1px solid #2a2e39;
    border-radius: 6px;
    color: #d1d4dc;
    font-size: 12px;
    font-family: "Consolas", "Cascadia Code", monospace;
}
QHeaderView::section {
    background-color: #1e222d;
    color: #787b86;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid #2a2e39;
    font-weight: 700;
    font-size: 11px;
    font-family: -apple-system, "Segoe UI", sans-serif;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #1a1e29;
}
QTableWidget::item:selected {
    background-color: #222938;
    color: #ffffff;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #131722;
    width: 6px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #2a2e39;
    min-height: 24px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #2962ff;
}

/* Splitter */
QSplitter::handle {
    background-color: #1a1e29;
}
QSplitter::handle:hover {
    background-color: #2962ff;
}

/* Status Bar */
QStatusBar {
    background-color: #131722;
    border-top: 1px solid #2a2e39;
    color: #787b86;
    font-size: 11px;
    padding: 3px 8px;
}
"""
