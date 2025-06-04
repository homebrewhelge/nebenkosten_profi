**Übersicht:**
Diese Anleitung führt dich Schritt für Schritt durch den gesamten Ablauf – von der Erfassung deiner Daten bis zum fertigen PDF. Dabei gehen wir auf jeden Tab ein, erklären, welche Felder du ausfüllen musst, wie die Berechnung abläuft und wie du am Ende deine Abrechnung exportierst.

---

## 1. Programmstart & Grundkonfiguration

1. **Starten**

   * Öffne ein Terminal, wechsle in den Ordner mit `nebengui.py` und führe aus:

     ```bash
     python nebengui.py
     ```
   * Das Hauptfenster „Nebenkosten Profi (v1.4)“ öffnet sich.

2. **Oberfläche**

   * Ganz oben siehst du ein **Reiter-Widget (Tabs)** mit folgenden Registerkarten:

     1. Zählerstände
     2. Fixkosten/Umlage
     3. Heizkosten
     4. Ergebnisse
     5. Zählerhistorie
     6. Abrechnung
   * Darunter zwei Checkboxen:

     * **„Heizkosten: 70/30-Regel anwenden“**
     * **„CO₂-Abgabe global einrechnen“**
   * Unten findest du drei Buttons:

     * **Neu berechnen**
     * **Speichern Historie**
     * **Laden Historie**

3. **Automatisches Laden vorhandener Daten**

   * Beim Start versucht das Programm automatisch, folgende CSV-Dateien einzulesen (falls sie bereits existieren):

     * `zaehlerstaende.csv` → lädt Zählerstände in Tab 1
     * `fixkosten.csv` → lädt Fixkosten in Tab 2
     * `ergebnisse.csv` → lädt Mieter-Daten in Tab 4
   * Falls keine CSV vorhanden ist, bleiben die Tabellen zunächst leer und du kannst sie neu befüllen.

---

## 2. Tab 1: Zählerstände

Hier erfasst du alle Zählerdaten (Heizung, Wasser, Strom etc.) sowie optional Wohnfläche und bei Mieterwechsel Ein-/Auszugsdaten.

1. **Zeile hinzufügen**

   * Klicke auf **„Zeile hinzufügen“** am unteren Rand des Tab, um eine neue Zeile zu erzeugen.
   * Du kannst beliebig viele Zeilen einfügen – für jede Partei (z. B. EG, OG, DG) und jede Verbrauchsart.

2. **Spalten in der Reihenfolge (0–7)**
   0\. **Partei**: Eindeutige Bezeichnung der Wohneinheit, z. B. „EG“, „OG“, „DG“.

   1. **Verbrauchsart**: Text, z. B. „Heizung“, „Wasser“, „Strom“, „Wohnfläche“ (für Flächen-Verteilung).
   2. **Altstand**: Zählerstand zu Jahresbeginn oder zum Einzugsdatum.
   3. **Neuwert**: Zählerstand zu Jahresende oder zum Auszugsdatum.
   4. **Menge**: Wird automatisch berechnet (Neuwert – Altstand), angepasst bei Mieterwechsel.
   5. **Kosten/Einheit (€)**: Preis pro Einheit, z. B. 0,070 €/kWh (Heizung), 0,085 €/m³ (Wasser), 1 €/m² (Wohnfläche). Muss als Zahl eingetragen werden.
   6. **Einzug (JJJJ-MM-TT)**: Nur bei unterjährigem Mieterwechsel – Datum, ab dem der neue Mieter in der Partei wohnt.
   7. **Auszug (JJJJ-MM-TT)**: Nur bei unterjährigem Mieterwechsel – Datum, bis zu dem der alte Mieter wohnt.

3. **Menger-Berechnung**

   * **Ohne Mieterwechsel:** Nach Klick auf **„Neu berechnen“** wird in Spalte 4 automatisch:

     ```
     Menge = Neuwert – Altstand
     ```
   * **Mit Mieterwechsel (Einzug/Auszug befüllt):**

     * Programm berechnet anteiligen Verbrauch tageweise:

       1. `(Auszugsdatum – Einzugsdatum).days + 1 = Anzahl Tage`
       2. `Menge = (Neuwert – Altstand) × (Tage / 365)`
     * So wird exakt der anteilige Verbrauch für den jeweiligen Zeitraum ermittelt.

4. **Tipps zur Eingabe**

   * Achte auf das korrekte Datumsformat `JJJJ-MM-TT` (z. B. „2024-04-30“). Bei falschem Format wird der Mieterwechsel-Mechanismus übersprungen.
   * Wenn du Kosten nach „Fläche“ verteilen möchtest, lege in Tab 1 eine Zeile mit Verbrauchsart „Wohnfläche“ an und trage in Spalte 4 (Menge) die Quadratmeter (z. B. „85“) ein. In „Kosten/Einheit (€)“ kannst du 1 eintragen – die reine qm-Zahl ist hier wichtiger.
   * Jede Zeile muss denselben Parteinamen verwenden (z. B. „OG“), damit die Zuordnung korrekt erfolgt.

---

## 3. Tab 2: Fixkosten/Umlage

Hier erfass(st) du alle einmaligen fixe Kostenarten (z. B. Grundsteuer, Müll, Heizkosten, Wasser, Allgemeinstrom).

1. **Zeile hinzufügen**

   * Klicke auf **„Zeile hinzufügen“**, um eine neue Kostenposition anzulegen.

2. **Spalten (0–5)**
   0\. **Kostenart**: Freier Text, z. B. „Grundsteuer“, „Müllabfuhr“, „Heizkosten Gesamt“, „Heizung Grundkosten“, „Wasser“, „Strom Allgemein“.

   1. **Umlageschlüssel** (Dropdown): Wähle aus:

      * **„Fläche“** → verteilt nach Quadratmeter (aus Tab 1: Verbrauchsart „Wohnfläche“).
      * **„Parteien“** → gleichmäßig auf alle Parteien (jede Zeile in Tab 1 mit einem Parteinamen zählt als 1).
      * **„Verbrauch“** → verteilt nach Verbrauchsmengen derselben Kostenart (z. B. „Wasser“).
      * **„Faktor“** → verteilt nach numerischen Werten, die du in Spalte 2 (Faktor) einträgst (Format: „Partei\:Zahl,Partei2\:Zahl,…“).
      * **„Manuell“** → du trägst später in Spalte 4 („Verteilte Kosten“) direkt den geldwerten Anteil ein (kein automatisches Mapping).
   2. **Faktor**: Nur bei Umlageschlüssel = „Faktor“ erforderlich. Trage dort eine Liste ein wie `EG:100,OG:50,DG:25`. Damit weiß das Programm, in welchem Verhältnis die Grundkosten (bzw. Kostenarten mit Schlüssel „Faktor“) verteilt werden.
   3. **Gesamtkosten (€)**: Bruttobetrag dieser Kostenposition (als Zahl). Z. B. 3 500 (€/Jahr) für Müll, 10 000 (€) für Heizkosten Gesamt.
   4. **Verteilte Kosten (€)**: Nur erforderlich, wenn Umlageschlüssel = „Manuell“; du gibst hier für jeden Mieter (Partei) manuelle Beträge ein. In v1.4 wird diese Spalte lediglich ignoriert, wenn „Manuell“ gewählt ist (zu komplexes Mapping entfällt).
   5. **CO₂ (ja/nein)**: Kleines Kästchen. Wenn du es aktivierst **und** oben die Checkbox „CO₂-Abgabe global einrechnen“ angehakt ist, rechnet das Programm **+ 5 %** auf „Gesamtkosten (€)“.

3. **Heizkosten-Sonderfall (70/30-Regel)**

   * Wenn du bei obenstehender globalen Checkbox **„Heizkosten: 70/30-Regel anwenden“** aktivierst und in einer Kostenart das Wort **„Heizung“** enthalten ist, passiert Folgendes:

     1. **70 % Verbrauchsteil**: Aus den Zeilen in Tab 1, Verbrauchsart „Heizung“, wird der gesamte Verbrauch aller Parteien zusammengerechnet. Davon erhält jede Partei anteilig den Verbrauchskosten-Anteil:

        $$
          \text{Verbrauchskosten‐Betrag} = \; (\text{Partei‐Heizverbrauch} / \text{Gesamt‐Heizverbrauch}) \;\times\; (0{,}70 \times \text{Gesamtkosten})
        $$
     2. **30 % Grundteil**: Aus den Zeilen in Tab 2, bei denen „Heizung“ in „Kostenart“ steht **und** Umlageschlüssel = „Faktor“, wird der Wert in Spalte 2 ausgewertet (z. B. `EG:100,OG:50`). Die Summe aller Faktoren ergibt $F_{\text{Summe}}$. Dann erhält jede Partei:

        $$
          \text{Grundkostenanteil} = \bigl(\text{Faktor}_\text{Partei} / F_{\text{Summe}}\bigr) \;\times\; (0{,}30 \times \text{Gesamtkosten})
        $$
     3. **Beispiel**:

        * Kostenart „Heizung Gesamt“, Gesamtkosten = 10 000 € →

          * 70 % Verbrauchsteil = 7 000 € (verteilt nach tatsächlichem Zählerverbrauch).
          * 30 % Grundteil = 3 000 € (verteilt nach Faktoren).
        * Faktoren-Liste in Tab 2: `EG:100,OG:50,DG:25` → $100 + 50 + 25 = 175$.

          * EG bekommt $3 000 \times (100/175) ≈ 1 714,29\,€$
          * OG bekommt $3 000 \times (50/175) ≈ 857,14\,€$
          * DG bekommt $3 000 \times (25/175) ≈ 428,57\,€$

4. **CO₂-Abgabe global**

   * Aktiviere oben die Checkbox **„CO₂-Abgabe global einrechnen“**, wenn du willst, dass alle Kostenpositionen mit gesetztem Unter-Kästchen in Tab 2 um 5 % erhöht werden.
   * Pro Zeile in Tab 2 musst du dann in Spalte 5 (CO₂) den Haken setzen, damit **nur diese Position** den 5 %-Aufschlag erhält.

5. **Speichern & Laden in Tab 2**

   * Beim Schließen des Programms wird Tab 2 automatisch in `fixkosten.csv` gespeichert.
   * Beim nächsten Start wird der gespeicherte Inhalt wieder in Tab 2 geladen (Umlageschlüssel, Faktor-Texte und CO₂-Checkboxen bleiben erhalten).

---

## 4. Tab 3: Heizkosten (Detail)

In diesem Tab siehst du, wie sich die Heizkosten aufsplitten (Verbrauchsteil 70 % und Grundkosten Teil 30 %) – **automatisch** nach Klick auf **„Neu berechnen“**.

1. **Zeilen werden automatisch befüllt**

   * Nach dem Klick auf „Neu berechnen“ (in Tab 6) durchsucht das Programm alle Zähler-Daten (Tab 1) und Fixkosten-Daten (Tab 2) nach Einträgen mit „Heizung“.
   * Für jede Partei, die Heizverbrauch in Tab 1 hat, wird eine Zeile erzeugt mit:

     * Spalte 0: Parteiname
     * Spalte 1: Heizverbrauch (Menge aller Zeilen aus Tab 1 mit „Heizung“, anteilig bei Mieterwechsel)
     * Spalte 2: Heizkosten 70 % in € (Verbrauchsteil)
     * Spalte 3: Heizgrundkosten 30 % in €

2. **Kontrolle**

   * Überprüfe hier, ob die Verteilung logisch aussieht und den Faktoren entspricht, die du in Tab 2 eingetragen hast.

---

## 5. Tab 4: Ergebnisse

Hier legst du fest, welche Mieter existieren, wie viel sie bereits gezahlt haben, und nach Klick auf „Neu berechnen“ siehst du ihre jährlichen Gesamtkosten, Nachzahlung/Gutschrift und den neuen Abschlag.

1. **Zeile hinzufügen**

   * Klicke auf **„Zeile hinzufügen“**, um pro Mieter eine Zeile anzulegen.

2. **Spalten (0–5)**
   0\. **Mieter**: Name des Mieters, z. B. „Frau Müller“, „Herr Schmidt“.

   1. **Partei**: Muss mit einem Eintrag aus Tab 1 übereinstimmen (z. B. „OG“).
   2. **Gesamt (€)**: Wird nach Klick auf „Neu berechnen“ automatisch befüllt (Summe aller Heizkosten- und Fixkosten-Anteile).
   3. **Gezahlt (€)**: Trage hier manuell ein, was der Mieter bisher als monatliche Abschläge insgesamt für das Jahr gezahlt hat (z. B. 1 200 € = 12×100 €).
   4. **Nachzahlung/Gutschrift (€)**: Wird automatisch berechnet:

      $$
        \text{Nachzahlung/Gutschrift} = \text{Gesamt} - \text{Gezahlt}
      $$

      * Positiv → Nachzahlung
      * Negativ → Gutschrift
   5. **Neuer Abschlag (€/Monat)**: Wird automatisch berechnet als

      $$
        (\text{Gesamt} / 12) \times 1{,}05
      $$

      → 5 % Puffer. Kann bei Bedarf auch manuell überschrieben werden (nach dem Berechnen).

3. **Speichern & Laden**

   * Tab 4 wird beim Schließen automatisch in `ergebnisse.csv` gespeichert.
   * Beim nächsten Start lädt das Programm die gespeicherten Mieter-Daten wieder.

---

## 6. Tab 5: Zählerhistorie (Backup)

Dient zur Kontrolle, Jahr-für-Jahr-Archivierung deiner Zählerstände.

1. **Tab aufrufen**

   * Hier siehst du eine Tabelle mit 6 Spalten: Jahr, Partei, Verbrauchsart, Altstand, Neuwert, Verbrauch.

2. **Zeilen manuell hinzufügen**

   * Klicke auf **„Zeile hinzufügen“**, um eine freie Zeile einzufügen. Du kannst manuell Historien-Daten eintragen.

3. **Zähler in Historie übernehmen**

   * Klicke auf **„Zähler in Historie übernehmen“**, um alle aktuellen Zählerstände (Tab 1) in die Historie zu kopieren. Dabei:

     * Für jede Zeile in Tab 1 wird in Tab 5:

       * Spalte 0: Aktuelles Jahr
       * Spalte 1: Parteiname
       * Spalte 2: Verbrauchsart
       * Spalte 3: Altstand
       * Spalte 4: Neuwert
       * Spalte 5: Verbrauch (Neuwert – Altstand)
   * Das ist praktisch, um Jahresabschlüsse zu archivieren.

4. **Speichern Historie**

   * Klicke auf **„Speichern Historie“**, um Tab 5 in die Datei `zaehlerhistorie_{Jahr}.csv` zu schreiben. Gleichzeitig wird eine Backup-Datei im Ordner `backups/` mit Zeitstempel angelegt.
   * Danach siehst du eine Info-Meldung, in welcher Datei die Historie gespeichert wurde.

5. **Neues Jahr anlegen**

   * Klicke auf **„Neues Jahr anlegen“**, um in Tab 1 bei jedem Eintrag den aktuellen Neuwert als neuen Altstand zu übernehmen und das Neuwert-Feld zu leeren.
   * So bist du automatisch bereit für das nächste Abrechnungsjahr.

---

## 7. Tab 6: Abrechnung

Im letzten Tab werden alle wichtigen Einzelposten und zusammenfassenden Texte angezeigt – und von hier aus speicherst du das finale PDF.

1. **Checkboxen „Details anzeigen“**
   Über der Detail-Tabelle findest du drei Checkboxen:

   * **„Heizkosten“**: Zeigt alle Posten ➔ „Heizkosten (Verbrauchsteil 70 %)“ und „Heizgrundkosten (30 %)“ inklusive Menge (Heizverbrauch).
   * **„Fixkosten“**: Zeigt alle fixen Kostenanteile (z. B. Wasser, Müll, Grundsteuer) pro Mieter.
   * **„Verbrauchswerte“**: Zeigt alle Einzel-Verbräuche aus Tab 1 (z. B. „Verbrauch Heizung“, „Verbrauch Wasser“) samt berechnetem Kostenbetrag = (Menge × Kosten/Einheit).

   Setze oder entferne die Haken, um zu steuern, welche Detail-Spalten im PDF später erscheinen.

2. **Detail-Tabelle**

   * Spalten:

     1. **Mieter**
     2. **Position** (z. B. „Heizkosten (Verbrauchsteil 70 %)“, „Grundsteuer“, „Verbrauch Wasser“…)
     3. **Wert (€)**: Geldbetrag dieses Postens
     4. **Verbrauch**: Mengenangabe (nur bei echten Verbrauchsposten, sonst leer)

   * Nach Klick auf **„Neu berechnen“** werden – je nach aktivierter Checkbox – für jeden Mieter einzelne Zeilen in diese Tabelle eingefügt. So siehst du ganz genau, wie sich der Gesamtbetrag aus den Einzelposten zusammensetzt.

3. **Zusammenfassende Texte**

   * Unterhalb der Detail-Tabelle befindet sich ein Textfeld, das automatisch pro Mieter einen Text anlegt, z. B.:

     ```
     Sehr geehrte/r Frau Müller, Ihre Nebenkostenabrechnung ergibt eine Nachzahlung von 1200,00 €. Ihr neuer Abschlag beträgt 110,00 € pro Monat.
     ```
   * Diese Zusammenfassung hilft dir, jedem Mieter den Gesamtbetrag und den neuen Abschlag mitzuteilen.

4. **Neu berechnen**

   * Sobald du alle vorherigen Tabs befüllt (Tab 1–4) und deine gewünschten Checkboxen gesetzt hast, klicke unten im Hauptfenster auf **„Neu berechnen“**.
   * Dann passiert Folgendes:

     1. **Tab 1**: Die Spalte „Menge“ wird gefüllt (je Zeile Verbrauch oder anteiliger Verbrauch).
     2. **Tab 2**: Heizkosten-Einträge (wenn aktiv) werden in 70 / 30 % aufgeteilt, CO₂-Aufschlag wird berücksichtigt.
     3. **Tab 3**: Es wird automatisch die Heizkosten-Detail-Tabelle neu erstellt.
     4. **Tab 4**: Pro Mieter werden „Gesamt (€)“, „Nachzahlung/Gutschrift (€)“ und „Neuer Abschlag“ berechnet und eingetragen.
     5. **Tab 6**:

        * Die **Detail-Tabelle** (Mieter/Position/Wert/Verbrauch) wird entsprechend deiner Checkboxen gefüllt.
        * Die **Textbausteine** im Textfeld werden neu generiert.

5. **Abrechnung als PDF speichern**

   * Wenn Detail-Tabelle und Texte aussehen, wie du sie brauchst, klicke in Tab 6 auf **„Abrechnung als PDF speichern“**.
   * Das Programm erstellt in deinem Arbeitsordner eine Datei `abrechnung_{Jahr}.pdf`, die enthält:

     1. **Kopfzeile** „Nebenkostenabrechnung {Jahr}“.
     2. **Detail-Tabelle** (mit Kopfzeile und allen Zeilen, je nach Checkbox-Auswahl) als echte PDF-Tabelle.
     3. **Zusammenfassende Texte** unterhalb der Tabelle (automatischer Zeilenumbruch, ggf. Seitenwechsel).
   * Nach erfolgreichem Export siehst du eine Info-Meldung: „Abrechnung als abrechnung\_{Jahr}.pdf gespeichert“.

---

## 8. So gehst du in der Praxis vor – Beispielablauf

Angenommen, du möchtest die Nebenkosten für 2024 berechnen:

1. **Tab 1: Zählerstände befüllen**

   * Füge pro Partei jede Verbrauchsart ein:

     * Zeile 1: Partei = EG, Verbrauchsart = „Heizung“, Altstand = 5 000, Neuwert = 5 500, Kosten/Einheit = 0,070, Einzug/Auszug leer.
     * Zeile 2: Partei = OG, Verbrauchsart = „Heizung“, Altstand = 4 800, Neuwert = 5 300, Kosten/Einheit = 0,070.
     * Zeile 3: Partei = DG, Verbrauchsart = „Heizung“, Altstand = 4 000, Neuwert = 4 600, Kosten/Einheit = 0,070.
     * Zeile 4: Partei = EG, Verbrauchsart = „Wasser“, Altstand = 1 200, Neuwert = 1 500, Kosten/Einheit = 0,085.
     * Zeile 5: Partei = OG, Verbrauchsart = „Wasser“, Altstand = 900, Neuwert = 1 100, Kosten/Einheit = 0,085.
     * … usw.
     * (Optional) Zeile: Partei = EG, Verbrauchsart = „Wohnfläche“, Altstand/Neuwert leer, Menge=85 (qm), Kosten/Einheit = 1.
   * Speichere zwischendurch (Datei `zaehlerstaende.csv`), damit beim Neustart nichts verloren geht.

2. **Tab 2: Fixkosten/Umlage befüllen**

   * Zeile 1: Kostenart = „Heizung Gesamt“, Umlageschlüssel = „Faktor“, Faktor = `EG:100,OG:50,DG:25`, Gesamtkosten = 10 000, CO₂ = angehakt (wenn CO₂-Abgabe gewünscht).
   * Zeile 2: Kostenart = „Wasser“, Umlageschlüssel = „Verbrauch“, Faktor leer, Gesamtkosten = 1 200, CO₂ = nicht angehakt.
   * Zeile 3: Kostenart = „Grundsteuer“, Umlageschlüssel = „Fläche“, Faktor leer, Gesamtkosten = 2 500, CO₂ = nicht angehakt.
   * Zeile 4: Kostenart = „Müllabfuhr“, Umlageschlüssel = „Parteien“, Faktor leer, Gesamtkosten = 900, CO₂ = nicht angehakt.
   * Zeile 5: Kostenart = „Allgemeinstrom“, Umlageschlüssel = „Faktor“, Faktor = `EG:1,OG:1,DG:1` (gleichverteilt), Gesamtkosten = 600, CO₂ = nicht angehakt.
   * (Optional) Andere Kosten nach Bedarf: Gartenpflege (Fläche), Hausmeister (Parteien) …

3. **Oben Checkboxen setzen**

   * Wenn du die 70/30-Regel nutzen willst, aktiviere **oben** „Heizkosten: 70/30-Regel anwenden“.
   * Wenn CO₂-Abgabe gewünscht, aktiviere **oben** „CO₂-Abgabe global einrechnen“.

4. **Tab 4: Mieter & Vorauszahlungen**

   * Zeile 1: Mieter = „Frau Müller“, Partei = „EG“, Gezahlt = 1 200 (12×100).
   * Zeile 2: Mieter = „Herr Schmidt“, Partei = „OG“, Gezahlt = 1 080 (12×90).
   * Zeile 3: Mieter = „Frau Meier“, Partei = „DG“, Gezahlt = 1 320 (12×110).

5. **Tab 5 (optional)**

   * Wenn du bereits ein Archiv hast, lade „Zählerhistorie 2023“ und vergleich die Werte. Sonst kannst du jetzt „Zähler in Historie übernehmen“ klicken, um die aktuellen Zählerstände in Tab 5 zu kopieren, und dann „Speichern Historie“, um `zaehlerhistorie_2024.csv` anzulegen.

6. **Tab 6: Checkboxen für Detailanzeige**

   * Standardmäßig sind alle drei Checkboxen („Heizkosten“, „Fixkosten“, „Verbrauchswerte“) aktiviert – so siehst du später alles im fertigen PDF.
   * Wenn du nur eine kurze Übersicht willst, kannst du z. B. „Verbrauchswerte“ deaktivieren, sodass im PDF nur die reinen Geldbeträge stehen, ohne Mengen.

7. **Neu berechnen (Endgültige Berechnung)**

   * Klicke **„Neu berechnen“**.
   * Kontrolle:

     1. **Tab 1**: Spalte „Menge“ füllt sich automatisch (z. B. Heiz-Menge, Wasser-Menge).
     2. **Tab 3** („Heizkosten“) zeigt pro Partei Heizverbrauch, Heizkosten (70 %) und Heizgrundkosten (30 %).
     3. **Tab 4** („Ergebnisse“) zeigt pro Mieter:

        * Gesamt (€) (Summe Heizkosten + sonstige Fixkosten)
        * Nachzahlung/Gutschrift (= Gesamt – Gezahlt)
        * Neuer Abschlag (€/Monat) = (Gesamt/12)×1,05.
     4. **Tab 6**:

        * **Detail-Tabelle**: je nach Haken siehst du alle einzelnen Posten (Heizkosten, Fixkosten, Verbrauchswerte) pro Mieter.
        * **Textfeld**: Die standardisierten Textbausteine erscheinen unten.

8. **Detail-Tabelle prüfen**

   * Scrolle in Tab 6 hoch, um die Detail-Tabelle zu sehen. Achte auf folgende Spalten:

     1. Mieter (immer gleich)
     2. Position (z. B. „Heizkosten (Verbrauchsteil 70 %)“, „Heizgrundkosten (30 %)“, „Wasser“, „Grundsteuer“, „Verbrauch Heizung“, „Verbrauch Wasser“ …)
     3. Wert (€) (Betrag dieses Postens)
     4. Verbrauch (Menge bei echten Verbrauchsposten)

   * Kontrolliere stichprobenartig:

     * Heizkosten 70 % + 30 % passen zu den Summen aus Tab 3.
     * Fixkosten-Beträge entsprechen deinen Eingaben in Tab 2 und den gewählten Umlageschlüsseln.
     * Verbrauchswerte: `Menge × Kosten/Einheit (€)` passt zu Tab 1-Daten.

9. **PDF speichern**

   * Wenn alles passt, klicke in Tab 6 auf **„Abrechnung als PDF speichern“**.
   * Das Programm öffnet einen PDF-Canvas und schreibt:

     1. Eine Überschrift „Nebenkostenabrechnung 2024“.
     2. Die **Detail-Tabelle** (alle ausgewählten Zeilen) als PDF-Tabelle (mit grauem Kopf).
     3. Unterhalb die **Zusammenfassenden Texte** (mit automatischem Zeilenumbruch und Seitenumbruch, falls nötig).
   * Danach siehst du eine Info-Meldung:

     ```
     Abrechnung als abrechnung_2024.pdf gespeichert
     ```
   * Öffne diese PDF (mit deinem PDF-Betrachter), um zu prüfen, dass alle Detail-Spalten und Texte enthalten sind.

---

## 9. Schließen & Neustart

1. **Automatisches Speichern**

   * Wenn du das Programm schließt (Fenster-X), werden automatisch alle Tabellen in CSV-Dateien geschrieben:

     * `zaehlerstaende.csv` (Tab 1)
     * `fixkosten.csv` (Tab 2)
     * `ergebnisse.csv` (Tab 4)
   * Die Zählerhistorie (`zaehlerhistorie_2024.csv`) bleibt unverändert – die speicherst du manuell über den Button in Tab 5.

2. **Neustart**

   * Starte `python nebengui.py` erneut – die Daten aus den CSV-Dateien werden in Tabs 1, 2 und 4 automatisch geladen.
   * Du kannst sofort mit „Neu berechnen“ fortfahren oder weitere Änderungen vornehmen.

3. **Historie-Daten**

   * Wenn du später Zählerdaten aus Vorjahren vergleichen willst, lade in Tab 5 über **„Laden Historie“** z. B. `zaehlerhistorie_2023.csv`. Dann siehst du die alten Jahres-Zähler in der Historie-Tabelle.

---

## 10. Zusammenfassung & Tipps

* **Reihenfolge der Befüllung**

  1. **Tab 1** („Zählerstände“) komplett befüllen: alle Parteien + Verbrauchsarten + Alt-/Neustände + Kosten/Einheit (+ Einzug/Auszug falls Mieterwechsel).
  2. **Tab 2** („Fixkosten/Umlage“) befüllen: alle Kostenarten mit Umlageschlüssel, Betrag + Faktor-Texte oder sonstige Verteilung.

     * Für Heizkosten beide Zeilen:

       * „Heizung Gesamt“ mit Umlageschlüssel = „Faktor“ und Faktoren-Liste.
       * („Heizung Grundkosten“ muss in der v1.4 nicht mehr getrennt als eigene Zeile stehen – die 30 %-Logik wird automatisch basierend auf Faktoren berechnet.)
  3. **Oben** die Checkbox **„Heizkosten: 70/30-Regel anwenden“** und ggf. **„CO₂-Abgabe global einrechnen“** setzen.
  4. **Tab 4** („Ergebnisse“) befüllen: pro Mieter Name + Partei + Zahlungsbetrag.
  5. **Tab 6** („Abrechnung“) – Checkboxen wählen,
  6. **„Neu berechnen“** klicken und **anschließend** **„Abrechnung als PDF speichern“**.

* **Kontrolle & Quellen**

  * In **Tab 3** („Heizkosten“) prüfst du, ob Verbrauch und Kosten-Split plausibel ist.
  * In **Tab 4** („Ergebnisse“) schaust du:

    * Ist „Gesamt (€)“ korrekt?
    * Stimmen „Nachzahlung/Gutschrift (€)“ und „Neuer Abschlag“?
  * In **Tab 6** kannst du per Checkbox-Auswahl exakt steuern, welche Posten in der PDF-Detail-Tabelle auftauchen.

* **Persistenz**

  * Einmal eingetragene Werte bleiben erhalten, weil sie beim Schließen in CSV-Dateien geschrieben werden.
  * Beim Neustart lädt das Programm alles automatisch. Nur die Zählerhistorie speicherst du manuell, um ältere Jahre zu archivieren.

* **Fehlersuche**

  * Wenn „Menge“ in Tab 1 nach „Neu berechnen“ nicht gefüllt wird, überprüfe:

    * Sind Altstand/Neuwert numerisch?
    * Ist „Kosten/Einheit (€)“ eine gültige Zahl?
    * Liegt ein Tippfehler im Datumsformat (Einzug/Auszug) vor?
  * Wenn in Tab 6 bestimmte Zeilen fehlen, prüfe zuerst die Checkboxen („Heizkosten“, „Fixkosten“, „Verbrauchswerte“).

* **PDF-Layout**

  * Die erzeugte PDF hat oben die Detail-Tabelle (bis zu etwa 100 Zeilen).
  * Darunter folgen die Textbausteine.
  * Für sehr umfangreiche Detail-Tabellen kann der Platz knapp werden – im Sinne einer Seite-für-Detail-Spalte ist v1.4 so getrimmt, dass mindestens 18 px Zeilenhöhe und definierte Spaltenbreiten (100 px, 200 px, 80 px, 80 px) verwendet werden. Sollte deine Tabelle mehr als einsehbare Zeilen fassen, kannst du per Handy-Zoom oder A4-Druck vergrößern, oder die Detail-Checkboxen einschränken.

---

Mit dieser Schritt-für-Schritt-Anleitung solltest du das Programm **korrekt benutzen** und **vollständig befüllen** können, um am Ende eine **komplette, detaillierte PDF-Nebenkostenabrechnung** zu erstellen. Viel Erfolg bei der tatsächlichen Abrechnung!
