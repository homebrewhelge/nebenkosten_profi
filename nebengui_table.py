import sys
from PyQt5 import QtWidgets, QtCore

class TabellenGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebenkosten Profi – Tabellenansicht")
        self.resize(1200, 800)

        tabs = QtWidgets.QTabWidget()

        # Tab 1 – Zählerstände
        self.tab_zaehler = QtWidgets.QWidget()
        self.zaehler_table = QtWidgets.QTableWidget()
        self.zaehler_table.setColumnCount(6)
        self.zaehler_table.setRowCount(10)
        self.zaehler_table.setHorizontalHeaderLabels(
            ["Partei", "Verbrauchsart", "Altstand", "Neuwert", "Menge", "Kosten"]
        )
        self.zaehler_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        zaehler_layout = QtWidgets.QVBoxLayout()
        zaehler_layout.addWidget(self.zaehler_table)
        self.tab_zaehler.setLayout(zaehler_layout)
        tabs.addTab(self.tab_zaehler, "Zählerstände")

        # Tab 2 – Fixkosten/Umlage
        self.tab_kosten = QtWidgets.QWidget()
        self.kosten_table = QtWidgets.QTableWidget()
        self.kosten_table.setColumnCount(6)
        self.kosten_table.setRowCount(10)
        self.kosten_table.setHorizontalHeaderLabels(
            ["Kostenart", "Umlageschlüssel", "Faktor", "Gesamtkosten", "Verteilte Kosten", "CO₂ (ja/nein)"]
        )
        kosten_layout = QtWidgets.QVBoxLayout()
        kosten_layout.addWidget(self.kosten_table)

        # Dropdowns in der Umlageschlüssel-Spalte
        for row in range(10):
            combo = QtWidgets.QComboBox()
            combo.addItems(["Fläche", "Parteien", "Verbrauch", "Faktor", "Manuell"])
            self.kosten_table.setCellWidget(row, 1, combo)

            # CO₂-Checkbox
            co2_checkbox = QtWidgets.QCheckBox()
            self.kosten_table.setCellWidget(row, 5, co2_checkbox)

        self.tab_kosten.setLayout(kosten_layout)
        tabs.addTab(self.tab_kosten, "Fixkosten/Umlage")

        # Tab 3 – Ergebnisse
        self.tab_ergebnisse = QtWidgets.QWidget()
        self.ergebnisse_table = QtWidgets.QTableWidget()
        self.ergebnisse_table.setColumnCount(7)
        self.ergebnisse_table.setRowCount(10)
        self.ergebnisse_table.setHorizontalHeaderLabels(
            ["Mieter", "Partei", "Gesamtbetrag", "Gezahlt", "Nachzahlung", "Guthaben", "Neuer Abschlag"]
        )
        self.ergebnisse_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        ergebnisse_layout = QtWidgets.QVBoxLayout()
        ergebnisse_layout.addWidget(self.ergebnisse_table)
        self.tab_ergebnisse.setLayout(ergebnisse_layout)
        tabs.addTab(self.tab_ergebnisse, "Ergebnisse")

        # Hauptlayout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(tabs)

        # Heizkosten-Sonderoptionen
        options_layout = QtWidgets.QHBoxLayout()
        self.check_7030 = QtWidgets.QCheckBox("Heizkosten: 70/30-Regel anwenden")
        self.check_co2 = QtWidgets.QCheckBox("Heizkosten: CO₂-Kosten einrechnen")
        options_layout.addWidget(self.check_7030)
        options_layout.addWidget(self.check_co2)
        main_layout.addLayout(options_layout)

        # Buttons unten
        button_layout = QtWidgets.QHBoxLayout()
        self.btn_neuberechnen = QtWidgets.QPushButton("Neu berechnen")
        self.btn_speichern = QtWidgets.QPushButton("Speichern")
        self.btn_laden = QtWidgets.QPushButton("Laden")
        button_layout.addWidget(self.btn_neuberechnen)
        button_layout.addWidget(self.btn_speichern)
        button_layout.addWidget(self.btn_laden)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TabellenGUI()
    gui.show()
    sys.exit(app.exec_())
