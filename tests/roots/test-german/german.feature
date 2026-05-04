# language: de

Funktionalität: Test für Verwendung Deutscher Keywords


Voraussetzungen:

    Angenommen die App ist gestartet
    Und der lokale Rechner ist läuft


Szenarien: Editieren der Dateien

    Angenommen die Datei "<Datei>" ist selektiert
    Wenn die Datei "<Datei>" per Drag und Drop auf "<Position>" gezogen wird
    Dann ist die Datei an Position <Position>

    Beispiele:
    | Datei          | Position |
    | test_versch_2  | (30,30)  |
    | test_versch_1  | (31,31)  |

Szenario: Datei hilfe selektieren

    Wenn die Datei "hilfe" selektiert wird
    Dann ist der Status der App "Datei hilfe"
    * ist der Status der App "Datei hilfe"


Regel: Auswahl mehrerer Dateien

    Szenario: die Datei hilfe2 wird selektiert

        Wenn die Datei "hilfe2" selektiert wird
        Dann ist der Status der App "Datei hilfe2"
        Und ist der Status der App "Datei hilfe2"

