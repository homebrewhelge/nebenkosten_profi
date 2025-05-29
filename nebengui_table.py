import sys
from PyQt5 import QtWidgets, QtCore

class TabellenGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebenkosten Profi – Tabellenansicht")
        self.resize(1000, 700)

        tabs = QtWidgets.QTabWidget()

        # Tab 1 – Zählerstände
        self.tab_zaehler = QtWidgets.QWidget()
        self.zaehler_table = QtWidgets.QTableWidget(5, 6)  # Beispiel: 5 Zeilen, 6 Spalten
        self.zaehler_table.setHorizontalHeaderLabels(
            ["Partei", "Verbrauchsart", "Altstand", "Neuwert", "Menge", "Kosten"]
        )
        zaehler_layout = QtWidgets.QVBoxLayout()
        zaehler_layout.addWidget(self.zaehler_table)
        self.tab_zaehler.setLayout(zaehler_layout)
        tabs.addTab(self.tab_zaehler, "Zählerstände")

        # Tab 2 – Fixkosten/Umlageschlüssel
        self.tab_kosten = QtWidgets.QWidget()
        self.kosten_table = QtWidgets.QTableWidget(5, 5)
        self.kosten_table.setHorizontalHeaderLabels(
            ["Kostenart", "Umlageschlüssel", "Faktor", "Gesamtkosten", "Verteilte Kosten"]
        )
        kosten_layout = QtWidgets.QVBoxLayout()
        kosten_layout.addWidget(self.kosten_table)
        self.tab_kosten.setLayout(kosten_layout)
        tabs.addTab(self.tab_kosten, "Fixkosten/Umlage")

        # Tab 3 – Ergebnisse
        self.tab_ergebnisse = QtWidgets.QWidget()
        self.ergebnisse_table = QtWidgets.QTableWidget(5, 7)
        self.ergebnisse_table.setHorizontalHeaderLabels(
            ["Mieter", "Partei", "Gesamtbetrag", "Gezahlt", "Nachzahlung", "Guthaben", "Neuer Abschlag"]
        )
        ergebnisse_layout = QtWidgets.QVBoxLayout()
        ergebnisse_layout.addWidget(self.ergebnisse_table)
        self.tab_ergebnisse.setLayout(ergebnisse_layout)
        tabs.addTab(self.tab_ergebnisse, "Ergebnisse")

        # Hauptlayout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(tabs)

        # Buttons
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
