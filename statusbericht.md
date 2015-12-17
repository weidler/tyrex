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
Klassifizierung von Texten anhand ihrer Textart  

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

**Deadlines**
- ??.01.16 Präsentation des Projekts  
- ??.??.16 Abgabe des Projekts (in den Semesterferien)  

Ansätze:
------
**Programm-Struktur**  
Die Texte (*raw_data*) werden im Rohformat nach Dateitypen/Formatierung sortiert und dementsprechend an den geeigneten **Parser** übergeben.
Die vom **Parser** erstellte *normierte* Version des Textes wird im Datensatz (*data*) des Programms hinterlegt.

Der **Feature Extractor Algorithm** (FEA) enthält verschiedene Methoden, mit denen er die Features aus den normierten Texten extrahiert und in einem JSON File
hinterlegt. Aus diesem kann wahlweise vom **FEA** auch gelesen werden um je nach Bedarf die Daten neu zu berechnen oder nur zu erweitern.

Zuletzt liest ein **ARFF-Builder** dieses *dataset* und wandelt es in ARFF um, um von WEKA verarbeitet werden zu können.

**Mögliche Ressourcen**  
- ella-Ressourcen: "Projekt Guttenberg", dt
- Brown-Korpus, engl (Zugriff von nltk auf verschiedene Genres, schon vorsortiert; z.B. reportage, reviews, science, governmental documents, fiction)
- Textklassen: Zeitungsartikel; Poesie/Gedichte; literarische Prosatexte; wissenschaftliche Artikel; ...  
- darauf achten: Sprache(Deutsch), Länge(Auschnitte?), Format(normieren?), Anzahl(ausgeglichen)  

**Mögliche Algorithmen**  
- k-means

**Mögliche Features**  
- Textlänge: einfach zu messen anhand der Anzahl der Wörter eines Textes; Ermittlung einer üblichen Spanne 
- Textstruktur: Anzahl der Paragraphen/Absätze/Strophen
- Satzbau: Verbstellung, Satzlänge, Komplexität/Verschachtelung (Anzahl Verben; Kommata; Dependenzen -> Parsing), Reim (der Einfachheit halber: die letzten 2-3 Buchstaben eines Wortes am Ende eines Verses)
- Terminologien (Vergleich mit Fachlexika oder Trainingskorpora: Sammlung typischer/häufiger (hoher count) Begriffe, Inhalts-/Schlüsselwörter; wordnet?)
- Erzählperspektive: auktorial, neutral, ich, (personal); direkte Rede: 'du', 'ihr', 'sie' (mit Deklinationen)
- tbc...

**TO DECIDE**
- Sprache des Korpus (dt/engl)

Literaturverzeichnis:
------

-
