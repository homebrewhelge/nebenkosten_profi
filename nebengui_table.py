import sys
import csv
import os
from datetime import datetime
from PyQt5 import QtWidgets
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class TabellenGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebenkosten Profi – Tabellenansicht")
        self.resize(1600, 900)

        tabs = QtWidgets.QTabWidget()

        # Tab 1 – Zählerstände
        self.zaehler_table = self.create_table(["Partei", "Verbrauchsart", "Altstand", "Neuwert", "Menge", "Kosten"], 10)
        tab_zaehler = QtWidgets.QWidget()
        layout_zaehler = QtWidgets.QVBoxLayout()
        layout_zaehler.addWidget(QtWidgets.QLabel("Hier erfasst du die aktuellen Zählerstände der Parteien."))
        layout_zaehler.addWidget(self.zaehler_table)
        tab_zaehler.setLayout(layout_zaehler)
        tabs.addTab(tab_zaehler, "Zählerstände")

        # Tab 2 – Fixkosten/Umlage
        self.kosten_table = self.create_table(["Kostenart", "Umlageschlüssel", "Faktor", "Gesamtkosten", "Verteilte Kosten", "CO₂ (ja/nein)"], 10)
        tab_kosten = QtWidgets.QWidget()
        layout_kosten = QtWidgets.QVBoxLayout()
        layout_kosten.addWidget(QtWidgets.QLabel("Hier legst du die fixen Kostenarten und Umlageschlüssel fest."))
        layout_kosten.addWidget(self.kosten_table)
        tab_kosten.setLayout(layout_kosten)
        tabs.addTab(tab_kosten, "Fixkosten/Umlage")

        # Tab 3 – Ergebnisse
        self.ergebnisse_table = self.create_table(["Mieter", "Partei", "Gesamtbetrag", "Gezahlt", "Nachzahlung", "Gutschrift", "Neuer Abschlag"], 2)
        tab_ergebnisse = QtWidgets.QWidget()
        layout_ergebnisse = QtWidgets.QVBoxLayout()
        layout_ergebnisse.addWidget(QtWidgets.QLabel("Hier siehst du die Ergebnisse pro Mieter – inkl. Nachzahlung, Gutschrift, neuem Abschlag."))
        layout_ergebnisse.addWidget(self.ergebnisse_table)
        tab_ergebnisse.setLayout(layout_ergebnisse)
        tabs.addTab(tab_ergebnisse, "Ergebnisse")

        # Tab 4 – Zählerhistorie
        self.historie_table = self.create_table(["Jahr", "Partei", "Verbrauchsart", "Altstand", "Neuwert", "Verbrauch"], 20)
        tab_historie = QtWidgets.QWidget()
        layout_historie = QtWidgets.QVBoxLayout()
        layout_historie.addWidget(QtWidgets.QLabel("Hier speicherst du alle historischen Zählerdaten über die Jahre."))
        layout_historie.addWidget(self.historie_table)

        btn_add_row = QtWidgets.QPushButton("Zeile hinzufügen")
        btn_add_row.clicked.connect(lambda: self.historie_table.setRowCount(self.historie_table.rowCount() + 1))
        btn_copy_zaehler = QtWidgets.QPushButton("Zähler in Historie übernehmen")
        btn_copy_zaehler.clicked.connect(self.copy_zaehler_to_historie)
        btn_new_year = QtWidgets.QPushButton("Neues Jahr anlegen")
        btn_new_year.clicked.connect(self.prepare_new_year)

        layout_historie.addWidget(btn_add_row)
        layout_historie.addWidget(btn_copy_zaehler)
        layout_historie.addWidget(btn_new_year)
        tab_historie.setLayout(layout_historie)
        tabs.addTab(tab_historie, "Zählerhistorie")

        # Tab 5 – Abrechnung
        self.abrechnung_area = QtWidgets.QTextEdit()
        tab_abrechnung = QtWidgets.QWidget()
        layout_abrechnung = QtWidgets.QVBoxLayout()
        layout_abrechnung.addWidget(QtWidgets.QLabel("Hier werden die fertigen Abrechnungstexte pro Mieter angezeigt."))
        layout_abrechnung.addWidget(self.abrechnung_area)
        btn_export_pdf = QtWidgets.QPushButton("Abrechnung als PDF speichern")
        btn_export_pdf.clicked.connect(self.export_abrechnung_pdf)
        layout_abrechnung.addWidget(btn_export_pdf)
        tab_abrechnung.setLayout(layout_abrechnung)
        tabs.addTab(tab_abrechnung, "Abrechnung")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(tabs)

        button_layout = QtWidgets.QHBoxLayout()
        self.btn_neuberechnen = QtWidgets.QPushButton("Neu berechnen")
        self.btn_neuberechnen.clicked.connect(self.berechne)
        self.btn_speichern = QtWidgets.QPushButton("Speichern Historie")
        self.btn_speichern.clicked.connect(self.speichere_historie)
        self.btn_laden = QtWidgets.QPushButton("Laden Historie")
        self.btn_laden.clicked.connect(self.lade_historie)
        button_layout.addWidget(self.btn_neuberechnen)
        button_layout.addWidget(self.btn_speichern)
        button_layout.addWidget(self.btn_laden)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_table(self, headers, rows):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(rows)
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        return table

    def copy_zaehler_to_historie(self):
        year = datetime.now().year
        for row in range(self.zaehler_table.rowCount()):
            partei_item = self.zaehler_table.item(row, 0)
            art_item = self.zaehler_table.item(row, 1)
            alt_item = self.zaehler_table.item(row, 2)
            neu_item = self.zaehler_table.item(row, 3)
            if partei_item and art_item and alt_item and neu_item:
                row_index = self.historie_table.rowCount()
                self.historie_table.insertRow(row_index)
                self.historie_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(year)))
                self.historie_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(partei_item.text()))
                self.historie_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(art_item.text()))
                self.historie_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(alt_item.text()))
                self.historie_table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(neu_item.text()))
                verbrauch = float(neu_item.text()) - float(alt_item.text())
                self.historie_table.setItem(row_index, 5, QtWidgets.QTableWidgetItem(f"{verbrauch:.2f}"))

    def prepare_new_year(self):
        next_year = datetime.now().year + 1
        for row in range(self.zaehler_table.rowCount()):
            partei_item = self.zaehler_table.item(row, 0)
            art_item = self.zaehler_table.item(row, 1)
            neu_item = self.zaehler_table.item(row, 3)
            if partei_item and art_item and neu_item:
                self.zaehler_table.setItem(row, 2, QtWidgets.QTableWidgetItem(neu_item.text()))
                self.zaehler_table.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
        QtWidgets.QMessageBox.information(self, "Neues Jahr", f"Vorbereitung für {next_year} abgeschlossen.")

    def speichere_historie(self):
        year = datetime.now().year
        filename = f"zaehlerhistorie_{year}.csv"
        os.makedirs("backups", exist_ok=True)
        backup_filename = f"backups/{filename.replace('.csv', f'_{datetime.now().strftime('%Y%m%d_%H%M')}.csv')}"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            headers = [self.historie_table.horizontalHeaderItem(i).text() for i in range(self.historie_table.columnCount())]
            writer.writerow(headers)
            for row in range(self.historie_table.rowCount()):
                writer.writerow([self.historie_table.item(row, col).text() if self.historie_table.item(row, col) else "" for col in range(self.historie_table.columnCount())])
        import shutil
        shutil.copyfile(filename, backup_filename)
        QtWidgets.QMessageBox.information(self, "Speichern", f"Historie gespeichert in {filename} und Backup erstellt als {backup_filename}")

    def lade_historie(self):
        year = datetime.now().year
        filename = f"zaehlerhistorie_{year}.csv"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                self.historie_table.setRowCount(0)
                for row_data in reader:
                    row_index = self.historie_table.rowCount()
                    self.historie_table.insertRow(row_index)
                    for col, data in enumerate(row_data):
                        self.historie_table.setItem(row_index, col, QtWidgets.QTableWidgetItem(data))
            QtWidgets.QMessageBox.information(self, "Laden", f"Historie aus {filename} geladen")
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Fehler", f"Datei {filename} nicht gefunden")

    def berechne(self):
        texte = []
        for row in range(self.ergebnisse_table.rowCount()):
            name_item = self.ergebnisse_table.item(row, 0)
            gesamt_item = self.ergebnisse_table.item(row, 2)
            gezahlt_item = self.ergebnisse_table.item(row, 3)
            abschlag_item = self.ergebnisse_table.item(row, 6)
            if name_item and gesamt_item and gezahlt_item and abschlag_item:
                name = name_item.text()
                gesamt = float(gesamt_item.text())
                gezahlt = float(gezahlt_item.text())
                differenz = gesamt - gezahlt
                abschlag = float(abschlag_item.text())
                if differenz > 0:
                    text = f"Sehr geehrte/r {name}, Ihre Nebenkostenabrechnung zeigt eine Nachzahlung von {differenz:.2f} €. Ihr neuer Abschlag beträgt {abschlag:.2f} € pro Monat."
                else:
                    text = f"Sehr geehrte/r {name}, Sie erhalten eine Gutschrift von {-differenz:.2f} €. Ihr neuer Abschlag beträgt {abschlag:.2f} € pro Monat."
                texte.append(text)
        self.abrechnung_area.setText("\n\n".join(texte))

    def export_abrechnung_pdf(self):
        year = datetime.now().year
        filename = f"abrechnung_{year}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        textobject = c.beginText(40, height - 50)
        textobject.setFont("Helvetica", 12)
        content = self.abrechnung_area.toPlainText().split('\\n')
        for line in content:
            textobject.textLine(line)
        c.drawText(textobject)
        c.save()
        QtWidgets.QMessageBox.information(self, "PDF Export", f"Abrechnung als {filename} gespeichert")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TabellenGUI()
    gui.show()
    sys.exit(app.exec_())
