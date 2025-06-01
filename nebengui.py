import sys
import csv
import os
from datetime import datetime, date
from PyQt5 import QtWidgets, QtCore
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class TabellenGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebenkosten Profi – Tabellenansicht (v1.1, erweitert)")
        self.resize(1600, 950)

        tabs = QtWidgets.QTabWidget()

        # ── Tab 1: Zählerstände ───────────────────────────────────────────
        self.zaehler_table = self.create_table(
            ["Partei", "Verbrauchsart", "Altstand", "Neuwert", "Menge",
             "Kosten/Einheit (€)", "Einzug (JJJJ-MM-TT)", "Auszug (JJJJ-MM-TT)"],
            10
        )
        tab_zaehler = QtWidgets.QWidget()
        layout_zaehler = QtWidgets.QVBoxLayout()
        layout_zaehler.addWidget(QtWidgets.QLabel(
            "Hier erfasst du die aktuellen Zählerstände und ggf. Einzugs-/Auszugsdaten."))
        layout_zaehler.addWidget(self.zaehler_table)
        tab_zaehler.setLayout(layout_zaehler)
        tabs.addTab(tab_zaehler, "Zählerstände")

        # ── Tab 2: Fixkosten/Umlage ───────────────────────────────────────
        self.kosten_table = QtWidgets.QTableWidget()
        self.kosten_table.setColumnCount(6)
        self.kosten_table.setRowCount(10)
        self.kosten_table.setHorizontalHeaderLabels(
            ["Kostenart", "Umlageschlüssel", "Faktor", "Gesamtkosten (€)",
             "Verteilte Kosten (€)", "CO₂ (ja/nein)"]
        )
        for row in range(10):
            combo = QtWidgets.QComboBox()
            combo.addItems(["", "Fläche", "Parteien", "Verbrauch", "Faktor", "Manuell"])
            self.kosten_table.setCellWidget(row, 1, combo)
            co2_checkbox = QtWidgets.QCheckBox()
            self.kosten_table.setCellWidget(row, 5, co2_checkbox)

        tab_kosten = QtWidgets.QWidget()
        layout_kosten = QtWidgets.QVBoxLayout()
        layout_kosten.addWidget(QtWidgets.QLabel(
            "Hier legst du die fixen Kostenarten fest. 'Heizung' wird ggf. 70/30 aufgeteilt."))
        layout_kosten.addWidget(self.kosten_table)
        tab_kosten.setLayout(layout_kosten)
        tabs.addTab(tab_kosten, "Fixkosten/Umlage")

        # ── Neuer Tab: Heizkosten-Detail ─────────────────────────────────
        self.heiz_table = QtWidgets.QTableWidget()
        self.heiz_table.setColumnCount(4)
        self.heiz_table.setHorizontalHeaderLabels([
            "Partei", "Heizverbrauch (Einheiten)",
            "Heizkosten 70 % (€)", "Heizgrundkosten 30 % (€)"
        ])
        self.heiz_table.setRowCount(0)

        tab_heizung = QtWidgets.QWidget()
        layout_heizung = QtWidgets.QVBoxLayout()
        layout_heizung.addWidget(QtWidgets.QLabel(
            "Hier siehst du die detaillierte Heizkosten‐Aufteilung pro Partei."))
        layout_heizung.addWidget(self.heiz_table)
        tab_heizung.setLayout(layout_heizung)
        tabs.insertTab(2, tab_heizung, "Heizkosten")

        # ── Tab 3: Ergebnisse ─────────────────────────────────────────────
        self.ergebnisse_table = QtWidgets.QTableWidget()
        self.ergebnisse_table.setColumnCount(6)
        self.ergebnisse_table.setRowCount(2)
        self.ergebnisse_table.setHorizontalHeaderLabels(
            ["Mieter", "Partei", "Gesamt (€)", "Gezahlt (€)",
             "Nachzahlung/Gutschrift (€)", "Neuer Abschlag (€/Monat)"]
        )
        tab_ergebnisse = QtWidgets.QWidget()
        layout_ergebnisse = QtWidgets.QVBoxLayout()
        layout_ergebnisse.addWidget(QtWidgets.QLabel(
            "Hier siehst du die Endergebnisse pro Mieter."))
        layout_ergebnisse.addWidget(self.ergebnisse_table)
        tab_ergebnisse.setLayout(layout_ergebnisse)
        tabs.addTab(tab_ergebnisse, "Ergebnisse")

        # ── Tab 4: Zählerhistorie ────────────────────────────────────────
        self.historie_table = QtWidgets.QTableWidget()
        self.historie_table.setColumnCount(6)
        self.historie_table.setRowCount(20)
        self.historie_table.setHorizontalHeaderLabels(
            ["Jahr", "Partei", "Verbrauchsart", "Altstand", "Neuwert", "Verbrauch"]
        )
        tab_historie = QtWidgets.QWidget()
        layout_historie = QtWidgets.QVBoxLayout()
        layout_historie.addWidget(QtWidgets.QLabel(
            "Hier speicherst du alle historischen Zählerdaten."))
        layout_historie.addWidget(self.historie_table)

        btn_add_row = QtWidgets.QPushButton("Zeile hinzufügen")
        btn_add_row.clicked.connect(
            lambda: self.historie_table.setRowCount(self.historie_table.rowCount() + 1))
        btn_copy_zaehler = QtWidgets.QPushButton("Zähler in Historie übernehmen")
        btn_copy_zaehler.clicked.connect(self.copy_zaehler_to_historie)
        btn_new_year = QtWidgets.QPushButton("Neues Jahr anlegen")
        btn_new_year.clicked.connect(self.prepare_new_year)

        layout_historie.addWidget(btn_add_row)
        layout_historie.addWidget(btn_copy_zaehler)
        layout_historie.addWidget(btn_new_year)
        tab_historie.setLayout(layout_historie)
        tabs.addTab(tab_historie, "Zählerhistorie")

        # ── Tab 5: Abrechnung ────────────────────────────────────────────
        self.abrechnung_area = QtWidgets.QTextEdit()
        tab_abrechnung = QtWidgets.QWidget()
        layout_abrechnung = QtWidgets.QVBoxLayout()
        layout_abrechnung.addWidget(QtWidgets.QLabel(
            "Hier werden die fertigen Abrechnungstexte pro Mieter angezeigt."))
        layout_abrechnung.addWidget(self.abrechnung_area)
        btn_export_pdf = QtWidgets.QPushButton("Abrechnung als PDF speichern")
        btn_export_pdf.clicked.connect(self.export_abrechnung_pdf)
        layout_abrechnung.addWidget(btn_export_pdf)
        tab_abrechnung.setLayout(layout_abrechnung)
        tabs.addTab(tab_abrechnung, "Abrechnung")

        # ───────────────────────────────────────────────────────────────────
        options_layout = QtWidgets.QHBoxLayout()
        self.check_7030 = QtWidgets.QCheckBox("Heizkosten: 70/30-Regel anwenden")
        self.check_co2_global = QtWidgets.QCheckBox("CO₂-Abgabe global einrechnen")
        options_layout.addWidget(self.check_7030)
        options_layout.addWidget(self.check_co2_global)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(tabs)
        main_layout.addLayout(options_layout)

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
        """Generiert eine editierbare QTableWidget mit den gegebenen Spaltenüberschriften."""
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(rows)
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        return table

    def copy_zaehler_to_historie(self):
        """Kopiert die aktuellen Zählerstände in die Historie und berechnet den Verbrauch."""
        year = datetime.now().year
        for row in range(self.zaehler_table.rowCount()):
            partei_item = self.zaehler_table.item(row, 0)
            art_item    = self.zaehler_table.item(row, 1)
            alt_item    = self.zaehler_table.item(row, 2)
            neu_item    = self.zaehler_table.item(row, 3)

            if partei_item and art_item and alt_item and neu_item:
                try:
                    alt_wert = float(alt_item.text())
                    neu_wert = float(neu_item.text())
                except ValueError:
                    continue

                row_index = self.historie_table.rowCount()
                self.historie_table.insertRow(row_index)
                self.historie_table.setItem(row_index, 0,
                    QtWidgets.QTableWidgetItem(str(year)))
                self.historie_table.setItem(row_index, 1,
                    QtWidgets.QTableWidgetItem(partei_item.text()))
                self.historie_table.setItem(row_index, 2,
                    QtWidgets.QTableWidgetItem(art_item.text()))
                self.historie_table.setItem(row_index, 3,
                    QtWidgets.QTableWidgetItem(f"{alt_wert:.2f}"))
                self.historie_table.setItem(row_index, 4,
                    QtWidgets.QTableWidgetItem(f"{neu_wert:.2f}"))
                verbrauch = neu_wert - alt_wert
                self.historie_table.setItem(row_index, 5,
                    QtWidgets.QTableWidgetItem(f"{verbrauch:.2f}"))

    def prepare_new_year(self):
        """Übernimmt bei Jahreswechsel den Neuwert als neuen Altstand und leert das Neuwert-Feld."""
        next_year = datetime.now().year + 1
        for row in range(self.zaehler_table.rowCount()):
            neu_item = self.zaehler_table.item(row, 3)
            if neu_item:
                self.zaehler_table.setItem(row, 2,
                    QtWidgets.QTableWidgetItem(neu_item.text()))
                self.zaehler_table.setItem(row, 3,
                    QtWidgets.QTableWidgetItem(""))
        QtWidgets.QMessageBox.information(
            self, "Neues Jahr", f"Vorbereitung für {next_year} abgeschlossen.")

    def speichere_historie(self):
        """Speichert die Historie in eine CSV-Datei pro Jahr und erstellt ein Backup."""
        year = datetime.now().year
        filename = f"zaehlerhistorie_{year}.csv"
        os.makedirs("backups", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backups/{filename.replace('.csv', f'_{timestamp}.csv')}"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            headers = [
                self.historie_table.horizontalHeaderItem(i).text()
                for i in range(self.historie_table.columnCount())
            ]
            writer.writerow(headers)
            for row in range(self.historie_table.rowCount()):
                row_data = []
                for col in range(self.historie_table.columnCount()):
                    item = self.historie_table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

        import shutil
        shutil.copyfile(filename, backup_filename)
        QtWidgets.QMessageBox.information(
            self, "Speichern",
            f"Historie gespeichert in {filename} und Backup erstellt als\n{backup_filename}"
        )

    def lade_historie(self):
        """Lädt die CSV-Historie des aktuellen Jahres in die Historie-Tabelle."""
        year = datetime.now().year
        filename = f"zaehlerhistorie_{year}.csv"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Kopfzeile überspringen
                self.historie_table.setRowCount(0)
                for row_data in reader:
                    row_index = self.historie_table.rowCount()
                    self.historie_table.insertRow(row_index)
                    for col, data in enumerate(row_data):
                        self.historie_table.setItem(row_index, col,
                            QtWidgets.QTableWidgetItem(data))
            QtWidgets.QMessageBox.information(
                self, "Laden", f"Historie aus {filename} geladen")
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, "Fehler", f"Datei {filename} nicht gefunden")

    def berechne(self):
        """Haupt-Berechnungslogik inklusive Heizkosten-Tab."""
        # 1) Zählerstände → Menge (inkl. Mieterwechsel)
        par_consumption = {}
        total_heiz_consumption = 0.0

        for row in range(self.zaehler_table.rowCount()):
            partei_item = self.zaehler_table.item(row, 0)
            art_item    = self.zaehler_table.item(row, 1)
            alt_item    = self.zaehler_table.item(row, 2)
            neu_item    = self.zaehler_table.item(row, 3)
            kosten_item = self.zaehler_table.item(row, 5)
            einzug_item = self.zaehler_table.item(row, 6)
            auszug_item = self.zaehler_table.item(row, 7)

            if not (partei_item and art_item and alt_item and neu_item and kosten_item):
                continue

            partei_text = partei_item.text().strip()
            art_text    = art_item.text().strip()

            try:
                alt_wert = float(alt_item.text())
                neu_wert = float(neu_item.text())
                _ = float(kosten_item.text())
            except ValueError:
                continue

            menge = neu_wert - alt_wert
            if einzug_item and auszug_item:
                einzug_text = einzug_item.text().strip()
                auszug_text = auszug_item.text().strip()
                if einzug_text and auszug_text:
                    try:
                        einzug_date = datetime.strptime(einzug_text, "%Y-%m-%d").date()
                        auszug_date = datetime.strptime(auszug_text, "%Y-%m-%d").date()
                        tage = (auszug_date - einzug_date).days + 1
                        menge = (neu_wert - alt_wert) * (tage / 365)
                    except ValueError:
                        pass

            self.zaehler_table.setItem(row, 4,
                QtWidgets.QTableWidgetItem(f"{menge:.2f}"))
            key = (partei_text, art_text)
            par_consumption[key] = par_consumption.get(key, 0.0) + menge

            if self.check_7030.isChecked() and "Heizung" in art_text:
                total_heiz_consumption += menge

        # 2) Heizkosten 70/30 & CO₂-Aufschlag
        heizkosten_gesamt       = 0.0
        heizgrundkosten_gesamt   = 0.0
        heiz_faktoren_pro_partei = {}

        for row in range(self.kosten_table.rowCount()):
            kostenart_item = self.kosten_table.item(row, 0)
            schl_widget    = self.kosten_table.cellWidget(row, 1)
            schl_text      = schl_widget.currentText() if schl_widget else ""
            gesamt_item    = self.kosten_table.item(row, 3)
            faktor_item    = self.kosten_table.item(row, 2)
            co2_widget     = self.kosten_table.cellWidget(row, 5)

            if not (kostenart_item and gesamt_item):
                continue

            text_kostenart = kostenart_item.text().strip()
            try:
                gesamt_kost = float(gesamt_item.text())
            except ValueError:
                continue

            if self.check_co2_global.isChecked() and co2_widget and co2_widget.isChecked():
                gesamt_kost *= 1.05

            if self.check_7030.isChecked() and "Heizung" in text_kostenart:
                verbrauchsteil = gesamt_kost * 0.70
                grundteil      = gesamt_kost * 0.30
                heizkosten_gesamt     += verbrauchsteil
                heizgrundkosten_gesamt += grundteil

                if schl_text == "Faktor" and faktor_item:
                    faktor_text = faktor_item.text().strip()
                    for pair in faktor_text.split(","):
                        if ":" in pair:
                            partei_name, wert_str = pair.split(":", 1)
                            partei_name = partei_name.strip()
                            try:
                                wert = float(wert_str.strip())
                            except ValueError:
                                wert = 0.0
                            heiz_faktoren_pro_partei[partei_name] = (
                                heiz_faktoren_pro_partei.get(partei_name, 0.0) + wert
                            )

        summe_heizfaktoren = sum(heiz_faktoren_pro_partei.values())

        verbrauch_heiz_verteilung = {}
        for (partei, art), menge in par_consumption.items():
            if self.check_7030.isChecked() and "Heizung" in art:
                if total_heiz_consumption > 0:
                    verbrauch_heiz_verteilung[partei] = (
                        verbrauch_heiz_verteilung.get(partei, 0.0)
                        + (menge / total_heiz_consumption) * heizkosten_gesamt
                    )
                else:
                    verbrauch_heiz_verteilung[partei] = (
                        verbrauch_heiz_verteilung.get(partei, 0.0) + 0.0
                    )

        grund_heiz_verteilung = {}
        if summe_heizfaktoren > 0:
            for partei_name, faktor in heiz_faktoren_pro_partei.items():
                grund_heiz_verteilung[partei_name] = (
                    faktor / summe_heizfaktoren
                ) * heizgrundkosten_gesamt
        else:
            parteien_mit_heiz = list(verbrauch_heiz_verteilung.keys())
            if parteien_mit_heiz:
                gleichanteil = heizgrundkosten_gesamt / len(parteien_mit_heiz)
                for partei_name in parteien_mit_heiz:
                    grund_heiz_verteilung[partei_name] = gleichanteil

        # ── Heizkosten-Tab befüllen ───────────────────────────────────────
        self.heiz_table.setRowCount(0)
        alle_parteien = set()
        for (partei, art), menge in par_consumption.items():
            if "Heizung" in art:
                alle_parteien.add(partei)
        alle_parteien.update(heiz_faktoren_pro_partei.keys())

        for partei_name in sorted(alle_parteien):
            zeile = self.heiz_table.rowCount()
            self.heiz_table.insertRow(zeile)

            self.heiz_table.setItem(zeile, 0,
                QtWidgets.QTableWidgetItem(partei_name))

            heiz_verbrauch = 0.0
            for (p, art), menge in par_consumption.items():
                if p == partei_name and "Heizung" in art:
                    heiz_verbrauch += menge
            self.heiz_table.setItem(zeile, 1,
                QtWidgets.QTableWidgetItem(f"{heiz_verbrauch:.2f}"))

            heizkosten70 = verbrauch_heiz_verteilung.get(partei_name, 0.0)
            self.heiz_table.setItem(zeile, 2,
                QtWidgets.QTableWidgetItem(f"{heizkosten70:.2f}"))

            heizgrund30 = grund_heiz_verteilung.get(partei_name, 0.0)
            self.heiz_table.setItem(zeile, 3,
                QtWidgets.QTableWidgetItem(f"{heizgrund30:.2f}"))

        # ── Fixkosten-Umlage & andere Verteilungen ───────────────────────
        anteile_pro_partei = {}
        gesamt_flaeche     = 0.0
        gesamt_parteien    = 0

        for row in range(self.kosten_table.rowCount()):
            schl_widget = self.kosten_table.cellWidget(row, 1)
            schl_text   = schl_widget.currentText() if schl_widget else ""
            if schl_text == "Fläche":
                for z_row in range(self.zaehler_table.rowCount()):
                    partei = self.zaehler_table.item(z_row, 0)
                    art    = self.zaehler_table.item(z_row, 1)
                    if partei and art and art.text().strip().lower() == "wohnfläche":
                        try:
                            qm = float(self.zaehler_table.item(z_row, 4).text())
                        except:
                            qm = 0.0
                        gesamt_flaeche += qm

            elif schl_text == "Parteien":
                for z_row in range(self.zaehler_table.rowCount()):
                    partei = self.zaehler_table.item(z_row, 0)
                    if partei and partei.text().strip():
                        gesamt_parteien += 1

        for row in range(self.kosten_table.rowCount()):
            kostenart_item = self.kosten_table.item(row, 0)
            schl_widget    = self.kosten_table.cellWidget(row, 1)
            schl_text      = schl_widget.currentText() if schl_widget else ""
            gesamt_item    = self.kosten_table.item(row, 3)
            co2_widget     = self.kosten_table.cellWidget(row, 5)

            if not (kostenart_item and gesamt_item):
                continue

            text_kostenart = kostenart_item.text().strip()
            try:
                gesamt_kost = float(gesamt_item.text())
            except ValueError:
                gesamt_kost = 0.0

            if self.check_co2_global.isChecked() and co2_widget and co2_widget.isChecked():
                gesamt_kost *= 1.05

            if self.check_7030.isChecked() and "Heizung" in text_kostenart:
                continue

            if schl_text == "Manuell":
                try:
                    man_kost = float(self.kosten_table.item(row, 4).text())
                except:
                    man_kost = 0.0
                continue

            elif schl_text == "Faktor":
                faktor_item = self.kosten_table.item(row, 2)
                if not faktor_item:
                    continue
                faktor_text = faktor_item.text().strip()
                faktor_dict = {}
                for pair in faktor_text.split(","):
                    if ":" in pair:
                        partei_name, wert_str = pair.split(":", 1)
                        partei_name = partei_name.strip()
                        try:
                            wert = float(wert_str.strip())
                        except ValueError:
                            wert = 0.0
                        faktor_dict[partei_name] = (
                            faktor_dict.get(partei_name, 0.0) + wert
                        )
                summe_faktoren_fix = sum(faktor_dict.values())
                if summe_faktoren_fix > 0:
                    for partei_name, wert in faktor_dict.items():
                        anteil = (wert / summe_faktoren_fix) * gesamt_kost
                        anteile_pro_partei[partei_name] = (
                            anteile_pro_partei.get(partei_name, 0.0) + anteil
                        )
                continue

            elif schl_text == "Fläche":
                if gesamt_flaeche > 0:
                    for z_row in range(self.zaehler_table.rowCount()):
                        partei = self.zaehler_table.item(z_row, 0)
                        art    = self.zaehler_table.item(z_row, 1)
                        if partei and art and art.text().strip().lower() == "wohnfläche":
                            try:
                                qm = float(self.zaehler_table.item(z_row, 4).text())
                            except:
                                qm = 0.0
                            anteil = (qm / gesamt_flaeche) * gesamt_kost
                            anteile_pro_partei[partei.text()] = (
                                anteile_pro_partei.get(partei.text(), 0.0) + anteil
                            )
                continue

            elif schl_text == "Parteien":
                if gesamt_parteien > 0:
                    anteil = gesamt_kost / gesamt_parteien
                else:
                    anteil = 0.0
                for z_row in range(self.zaehler_table.rowCount()):
                    partei = self.zaehler_table.item(z_row, 0)
                    if partei and partei.text().strip():
                        anteile_pro_partei[partei.text()] = (
                            anteile_pro_partei.get(partei.text(), 0.0) + anteil
                        )
                continue

            elif schl_text == "Verbrauch":
                total_verbrauch = 0.0
                kosten_art = text_kostenart
                for z_row in range(self.zaehler_table.rowCount()):
                    art = self.zaehler_table.item(z_row, 1)
                    if art and art.text().strip() == kosten_art:
                        try:
                            verbrauch = float(self.zaehler_table.item(z_row, 4).text())
                        except:
                            verbrauch = 0.0
                        total_verbrauch += verbrauch
                for z_row in range(self.zaehler_table.rowCount()):
                    partei = self.zaehler_table.item(z_row, 0)
                    art    = self.zaehler_table.item(z_row, 1)
                    if partei and art and art.text().strip() == kosten_art:
                        try:
                            verbrauch = float(self.zaehler_table.item(z_row, 4).text())
                        except:
                            verbrauch = 0.0
                        if total_verbrauch > 0:
                            anteil = (verbrauch / total_verbrauch) * gesamt_kost
                        else:
                            anteil = 0.0
                        anteile_pro_partei[partei.text()] = (
                            anteile_pro_partei.get(partei.text(), 0.0) + anteil
                        )
                continue

        # ── Tab 3: Ergebnisse mit Summen ─────────────────────────────────
        ergebnis_texte = []
        for row in range(self.ergebnisse_table.rowCount()):
            name_item    = self.ergebnisse_table.item(row, 0)
            partei_item  = self.ergebnisse_table.item(row, 1)
            gezahlt_item = self.ergebnisse_table.item(row, 3)
            if not (name_item and partei_item and gezahlt_item):
                continue

            name_text   = name_item.text().strip()
            partei_text = partei_item.text().strip()
            try:
                gezahlt_betrag = float(gezahlt_item.text())
            except ValueError:
                gezahlt_betrag = 0.0

            anteil_summe = anteile_pro_partei.get(partei_text, 0.0)
            heiz_v       = verbrauch_heiz_verteilung.get(partei_text, 0.0)
            grund_v      = grund_heiz_verteilung.get(partei_text, 0.0)

            gesamt_kosten_partei = anteil_summe + heiz_v + grund_v
            differenz = gesamt_kosten_partei - gezahlt_betrag
            try:
                neuer_abschlag = (gesamt_kosten_partei / 12) * 1.05
            except:
                neuer_abschlag = 0.0

            if differenz > 0:
                self.ergebnisse_table.setItem(row, 4,
                    QtWidgets.QTableWidgetItem(f"{differenz:.2f}"))
                self.ergebnisse_table.setItem(row, 5,
                    QtWidgets.QTableWidgetItem("0.00"))
            else:
                self.ergebnisse_table.setItem(row, 4,
                    QtWidgets.QTableWidgetItem("0.00"))
                self.ergebnisse_table.setItem(row, 5,
                    QtWidgets.QTableWidgetItem(f"{-differenz:.2f}"))

            self.ergebnisse_table.setItem(row, 2,
                QtWidgets.QTableWidgetItem(f"{gesamt_kosten_partei:.2f}"))
            self.ergebnisse_table.setItem(row, 5,
                QtWidgets.QTableWidgetItem(f"{neuer_abschlag:.2f}"))

            if differenz > 0:
                text = (
                    f"Sehr geehrte/r {name_text}, Ihre Nebenkostenabrechnung ergibt eine "
                    f"Nachzahlung von {differenz:.2f} €. Ihr neuer Abschlag beträgt "
                    f"{neuer_abschlag:.2f} € pro Monat."
                )
            else:
                text = (
                    f"Sehr geehrte/r {name_text}, Sie erhalten eine Gutschrift von "
                    f"{-differenz:.2f} €. Ihr neuer Abschlag beträgt "
                    f"{neuer_abschlag:.2f} € pro Monat."
                )
            ergebnis_texte.append(text)

        self.abrechnung_area.setText("\n\n".join(ergebnis_texte))

    def export_abrechnung_pdf(self):
        """Exportiert den Inhalt des Abrechnungstab als PDF."""
        year = datetime.now().year
        filename = f"abrechnung_{year}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        textobject = c.beginText(40, height - 50)
        textobject.setFont("Helvetica", 12)

        content = self.abrechnung_area.toPlainText().split("\n")
        for line in content:
            textobject.textLine(line)

        c.drawText(textobject)
        c.save()
        QtWidgets.QMessageBox.information(
            self, "PDF Export", f"Abrechnung als {filename} gespeichert")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TabellenGUI()
    gui.show()
    sys.exit(app.exec_())
