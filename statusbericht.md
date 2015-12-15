Designing Experiments for Machine Learning, WiSe 2015/16  
Institute of Computational Linguistics  
Heidelberg University, Germany  

TexErk aka **TyReX** (Text Type Recognition)  
===================

*Statusbericht*  16.12.2015  
Autoren: Lydia Hofmann, Svenja Lohse, Tonio Weidler  
Betreuer: Éva Mújdricza-Maydt  

Ziel
------
Klassifizierung und Erkennung von Texten anhand ihrer Textart  

Hauptaufgabenverteilung:
------
*Lydia*: Dokumentation, Ressourcen  
*Svenja*: Recherche, Features  
*Tonio*: Programmierung  
-> alle helfen gegenseitig   

To Do:
------
- Texte verschiedener Arten finden  
- Vorverarbeitung (Formatierung und Linguistik) zur Feature-Extraktion  
- geeignete Algorithmen finden
- Feature-Extraktion
- Aufbau einer DB mit extrahierten Informationen
- Analyseprogramm

??.01.16 Präsentation des Projekts  
??.??.16 Abgabe des Projekts (in den Semesterferien)  

Weitere Ideen:
------
**Programm-Struktur**  
Text *->* "Parser"/Preprocessing/Normierung *->* niceText *->* 'FeatureExtraktion'Module *<->* Features in JSON *->* ARFF Datei  

**Mögliche Ressourcen**  
- ella-Ressourcen: "Projekt Guttenberg"  
- Textklassen: Zeitungsartikel; Poesie/Gedichte; literarische Prosatexte; wissenschaftliche Artikel; ...  
- darauf achten: Sprache(Deutsch), Länge(Auschnitte?), Format(normieren?), Anzahl(ausgeglichen)  

**Mögliche Algorithmen**  
- k-means

**Mögliche Features**  
- Textlänge  
- Satzbau: Verbstellung, Satzlänge, Verschachtelung (Anzahl Verben; Kommata; Dependenzen), Reim
- Terminologien (Vergleich mit Fachlexika oder Trainingskorpora)
- Worthäufigkeiten
- tbc...
