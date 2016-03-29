TyReX (Text Type Recognition)  
----------------
Projektdokumentation 31.03.2016  
Autoren: Lydia Hofmann, Svenja Lohse, Tonio Weidler  
Betreuer: Éva Mújdricza-Maydt  

Inhaltsverzeichnis  
-------
1. Einführung  
2. Daten  
3. Struktur und Features  
4. Experimente und Evaluation  
5. Aussichten  
6. Literatur

Einführung     
-------
Das Ziel dieses Projektes ist eine automatische Klassifizierung von Texten nach ihrer Textart. 
Suchmaschinen könnten das zur Kategorisierung und damit besseren Suche vorhandener Dokumente verwenden und auch andere Unternehmen würden von einem internen Kategoriensystem (mit Kategorien wie u.a. Rechnungen, Mitarbeitergespräche, Rezensionen, etc.) profitieren.  

Um dieses Ziel zu erreichen, müssen viele Daten gesammelt, aufbereitet und analysiert werden.  
Features, die die Eigenschaften der unterschiedlichen Texte beschreiben, spielen eine wichtige Rolle bei der Genre-Klassifizierung.  
...Satz zu unserem Ergebnis   
Weitere Schritte wären u.a. eine Erweiterung der Feature-Liste, größere Trainingsdatenmenge und z.B. eine einfach zu bedienende Webanwendung.  
  
Daten  
-------
Die Trainingsdaten stammen aus dem "Projekt-Gutenberg"-Korpus, der viele Werke bekannter Autoren bereit stellt, und "Zeit-Online" dient ebenfalls als Quelle.  
Die Texte sind unannotiert und wie folgt auf vier Kategorien aufgeteilt:  
*EPIC*(...)  
*DRAMA*(...)  
*POETRY*(...)  
*REPORT*(...)
  
Die Texte werden durch den "TextNormierer" aufbereitet, d.h. Satzzeichen werden durch <Tags/> ersetzt und unnötige Zeichen entfernt, sodass geordnete Zeilen- und Satzgrenzen entstehen. Durch die Normierung ist die Weiterverarbeitung der Daten einfacher und nützliche Metadaten werden durch die Tag-Setzung eingebunden. Ein Nachteil ist allerdings, dass uns externe Metadaten verloren gehen und der Nomierer viele Datentypen zu verarbeiten hat.  

Zusätzlich lassen wir den TreeTagger die Texte annotieren, um die so entstandenen POS-Tags und die Baumstruktur in Features verwenden zu können. 

...AUSSCHNITT NORM_TEXT  
...AUSSCHNITT TAGGED_TEXT  
  
Struktur
-------
Das einfache Prinzip bisheriger Theorien zu diesem Thema lautet, aus Trainingsdaten Features zu extrahieren und sie an einen Klassifizierungsalgorithmus zu übergeben.  
Z.B. Zelch und Engel (2005) haben Wort-Features aus ihren Texten extrahiert, Lexeme gebildet, lemmatisiert und diese Features dann mit einem 'SVM'-Algorithmus verarbeitet. 2015 beschrieb Ghaffari ebenfalls Vektoren aus extrahierten Worten, die er mit den 'SVM'-, 'Naive Bayes'- und 'Decision Tree'-Algorithmen zur Textklassifikation verwendet hatte. 
Unsere Vorgehensweise ist (weitgehend) ohne Wortvektoren, mit mehr trivialen Features. Mit Weka lassen wir u.a. 'Naive Bayes', 'MultilayerPerceptron' und 'Decision Tree' über die Daten laufen.  
  
  
*ARCHITEKTURÜBERSICHT*  
  
Features
-------
Im Folgenden werden alle bisher verwendeten Features aufgezählt und ihre Funktion grob beschrieben (für einen genauen Einblick kann der Code in "/fea/FeatureExtractionAlgorithms" nachvollzogen werden).  

Auflistung/Beschreibung Features (Sinn, Beispiel, Ausgabe), ARFF Ergebnis  
... calcTextLength  
... calcSentenceLengthAvg  
... calcSentenceLengthMax  
... calcSentenceLengthMin  
... calcRhyme1  
... calcRhyme2  
... calcMostCommonWords  
... calcTerminologicalCongruence  
... calcPhrasesPerParagraph  
... calcDigitFrequency  
... calcPunctuationFrequency  
... calcHashtagFrequency  
... calcWordLengthAvg  
... calcWordVariance  
... calcNEFrequency  
... calcVerbFrequency  
... calcNounFrequency  

Experimente und Evaluation  
-------
(Datenverteilung,) Algorithmen, Bewertung, ...  

Aussichten
-------
Probleme (mehr und besser verteilte Daten; Featureergebnisse nicht immer wie erwartet(z.B.Rhyme bei Poetry); weitere Features benötigt (z.B. Terminologien))  
Überlegungen (Kombination mit anderen Projekten; weitere Experimente; feinere Klassen; )  

Literatur
-------
**Klassifikation:**  
http://www.kdnuggets.com/2015/01/text-analysis-101-document-classification.html - *comparing the number of matching terms in doc vectors*  
http://www.python-kurs.eu/text_klassifikation_python.php - *bag of words/ naive bayes*   
http://wt.hs-augsburg.de/report/2005/Zelch_Christa_Engel_Stephan/Klassifikation.pdf - *automatische Textklassifizierung mit SVM*  
Lewis, David D., Naive (Bayes) at Forty: The independence assumption in informal retrieval, Lecture Notes in Computer Science (1998), 1398, Issue: 1398, Publisher: Springer, Pages: 4-15  
K. Nigam, A. McCallum, S. Thrun and T. Mitchell, Text classification from labeled and unlabeled documents using EM, Machine Learning 39 (2000) (2/3), pp. 103-134.  

**Andere:**  
http://www.falkwolfschneider.de/kurs10/Textgattungen.pdf - *lists different text genres*  
Textsorten : Differenzierungskriterien aus linguistischer Sicht / Elisabeth Gülich, Wolfgang Raible (Hrsg.). 2. Aufl., Wiesbaden : Akademische Verlagsgesellschaft Athenaion, c1975; (http://iucat.iu.edu/iuk/1836130) - *linguistical criteria*  
