Import Tools für Druckmessungen
=================

# Varianten

- 20L Messungen
- 1m3 Messungen
- 1XXm3 Messungen

# Import der Messdaten
 
Die Daten für die 20L Kugel müssen bisher manuell exportiert in ein Txt-file werden. Für die 1m3-Software 
wird gerade die Konvertierungsumgeschrieben. 1xxm3 ist direkt aus der Messerfassung konvertierbar.

# Auswertung

Es wird ein Export-TXT-File mit den Druckdaten eingelesen und entsprechend konvertiert.
Dann wird eine Logistische Regression durchgeführt und die Ableitung damit berechnet und ausgeben.

Zudem können Diagramme von den Druckverlaufskurven erstellt werden.

## Zielstellung

Einfach Bildung der Ableitung von Druckmessdaten, ohne manuelle Eingriffe.

# Prerequisites

Einmal [Python][2] (I've got 2.7) und pandas, numpy, and matplotlib.
Es kann [pip][3] verwendet werden um die Anhängigkeiten zu installieren:

    pip install -r requirements.txt


