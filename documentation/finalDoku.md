TyReX (Text Type Recognition)  
===============================
Projektdokumentation 31.03.2016  
Autoren: Lydia Hofmann, Svenja Lohse, Tonio Weidler  
Betreuer: Éva Mújdricza-Maydt  

Inhaltsverzeichnis  
-------
1. Einführung  
2. Daten  
3. Struktur
4. Features  
5. Experimente und Evaluation
6. Auswertung
7. Aussichten  
8. Literatur

1 Einführung     
-------
Das Ziel dieses Projektes ist eine automatische Klassifizierung von Texten nach ihrer Textart.
Suchmaschinen könnten das zur Kategorisierung und damit besseren Suche vorhandener Dokumente verwenden und auch andere Unternehmen würden von einem internen Kategoriensystem (mit Kategorien wie u.a. Rechnungen, Mitarbeitergespräche, Rezensionen, etc.) profitieren.  

Um dieses Ziel zu erreichen, müssen viele Daten gesammelt, aufbereitet und analysiert werden.  
Features, die die Eigenschaften der unterschiedlichen Texte beschreiben, spielen eine wichtige Rolle bei der Genre-Klassifizierung.  
...Satz zu unserem Ergebnis   
Weitere Schritte wären u.a. eine Erweiterung der Feature-Liste, größere Trainingsdatenmenge und z.B. eine einfach zu bedienende Webanwendung.  

2 Daten  
-------
Die Trainingsdaten stammen aus dem "Projekt-Gutenberg"-Korpus, der viele Werke bekannter Autoren bereit stellt, und "Zeit-Online" dient ebenfalls als Quelle.  
Mit diesen unannotierten Texten wurden zwei Korpora erstellt.

Der erste Korpus umfasst 1261 Dateien, die wie folgt in 4 grobe Klassen unterteilt wurden 

    222 Epische Texte
    291 Dramen
    302 Artikel
    446 Gedichte
    
Der zweite Korpus enthält 11950 Dateien, die wie folgt in x feinere Klassen eingeteilt wurden:

	efwefwe
	fwefwfe
	wefwff

Die Texte werden durch den "TextNormierer" (Parser) aufbereitet, d.h. Satzzeichen werden durch Tags (\</\>) ersetzt und unnötige Zeichen entfernt, sodass geordnete Zeilen- und Satzgrenzen entstehen.
Durch die Normierung ist die Weiterverarbeitung der Daten einfacher und nützliche Metadaten werden durch die Tag-Setzung eingebunden. Ein Nachteil ist allerdings, dass uns externe Metadaten
verloren gehen und der Nomierer viele Datentypen zu verarbeiten hat, wodurch eine optimale Normierung teilweise nicht möglich ist.  

**AUSSCHNITT NORM_TEXT**  
**AUSSCHNITT TAGGED_TEXT**

Zusätzlich lassen wir den TreeTagger die Texte bei der Featureberechnung annotieren, um die so entstandenen POS-Tags und die Baumstruktur in Features verwenden zu können.



3 Struktur
-------
Das einfache Prinzip bisheriger Theorien zu diesem Thema lautet, aus Trainingsdaten Features zu extrahieren und sie an einen Klassifizierungsalgorithmus zu übergeben.  
Z.B. Zelch und Engel (2005) haben Wort-Features aus ihren Texten extrahiert, Lexeme gebildet, lemmatisiert und diese Features dann mit einem 'SVM'-Algorithmus verarbeitet. 2015 beschrieb Ghaffari ebenfalls Vektoren aus extrahierten Worten, die er mit den 'SVM'-, 'Naive Bayes'- und 'Decision Tree'-Algorithmen zur Textklassifikation verwendet hatte.
Unsere Vorgehensweise ist (weitgehend) ohne Wortvektoren, mit mehr trivialen Features. Mit Weka lassen wir u.a. 'Naive Bayes', 'MultilayerPerceptron' und 'Decision Tree' über die Daten laufen.  

![architecture](tyrex_architecture.png?raw=true "Architecture")

4 Features
-------
Im Folgenden werden alle bisher verwendeten Features aufgezählt und ihre Funktion grob beschrieben (für einen genauen Einblick kann der Code in "/fea/FeatureExtractionAlgorithms.py" nachvollzogen werden).  
- *calcTextLength*  
Berechnet die Länge der Texte und ignoriert dabei XML-Tags.  
Annahme: z.B. epische Texte sind meist länger als Zeitungsartikel.  
- *calcSentenceLengthAvg* / *calcSentenceLengthMax* / *calcSentenceLengthMin*    
Berechnet die durschnittliche/maximalste/minimalste Anzahl von Wörtern aller Sätze.  
Annahme: z.B. während Dramen eher kurze Sätze (u.a. Regieanweisungen) beinhalten, sind epische Werke oder wissenschaftliche Arbeiten eventuell eher langsätzig.  
- *calcRhymeAvg*  
Zählt alle Aufkommen von Zeilenendungen und berechnet einen Durschnitt der wiederkehrenden Endungen.  
Annahme: z.B. sollten Gedichte mehr reimende Endungen enthalten als Zeitungsartikel.  
Revision: längere Texte besitzen mehr Endungen, somit eine erhöhte Chance auf gleiche Endungen, und Texte aus der 'Poetry'-Kategorie besitzen weniger reine Reime als gedacht;  
Feature muss z.B. mit einer Schema-Prüfung verbessert werden.  
- *calcPhrasesPerParagraph*    
Berechnet die Zahl der Sätze pro Zeile.  
Annahme: Sollte zur besseren Abgrenzung von Gedichten zu anderen Textsorten dienen. Während in Gedichten Sätze häufig über einen gesamten Vers mit mehreren Umbrüchen gehen, tritt bei epischen Texten und Artikeln
der erste Umbruch meist erst nach einen gesamten Absatz auf.  
Revision: Leider vermindert die Strukturierung der Dateien den Wert des Features. Auch in epischen Texten sind Zeilen künstlich umgebrochen.
- *calcDigitFrequency*   
Berechnet...  
Annahme: z.B....  
- *calcPunctuationFrequency*  
Berechnet...  
Annahme: z.B....  
- *calcWordLengthAvg*  
Berechnet...  
Annahme: z.B....  
- *calcWordVariance*  
Berechnet, wie unterschiedlich die Wortwahl im Text ist. Es wird die Zahl der einzigartigen Lemmata über die Gesamtzahl an Worten relativiert.  
Annahme: In Gedichten ist die Wortwahl häufig abwechslungsreicher, in Dramen und Artikeln vermutlich weniger.  
- *calcNEFrequency*  
Berechnet...  
Annahme: z.B....  
- *calcVerbFrequency*  
Berechnet...  
Annahme: z.B....  
- *calcNounFrequency*  
Berechnet...  
Annahme: z.B....  

Diese Features werden durch den FEA berechnet und vom ARFFBuilder in einer ARFF Datei zusammengefasst. Der folgende Ausschnitt zeigt einen Teil dieser ARFF Datei.

    @relation tyrex


    @attribute	NE_frequency	numeric
    @attribute	word_variance	numeric
    @attribute	digit_frequency	numeric
    @attribute	noun_frequency	numeric
    @attribute	phrases_per_paragraph	numeric
    @attribute	punctuation_frequency	numeric
    @attribute	rhyme_average	numeric
    @attribute	sentence_length_avg	numeric
    @attribute	sentence_length_max	numeric
    @attribute	sentence_length_min	numeric
    @attribute	text_length	numeric
    @attribute	verb_frequency	numeric
    @attribute	word_length_average	numeric
    @attribute	class	{ epic, drama, report, poetry }


    @DATA
    0.0020035491441982942, 0.35643988018827555, 0.0004677268475210477, 0.023241170072700212, 0.6939890710382514, 0.03014801173180547, 0.6153846153846154, 17.826771653543307, 89, 3, 2317, 0.13377983857118325, 0.8260315078769692, poetry
    0.0, 0.7014925373134329, 0.0, 0.02564102564102564, 1.1666666666666667, 0.022988505747126436, 0.0, 9.142857142857142, 18, 1, 63, 0.13214990138067062, 0.8297872340425532, epic
    0.004719101123595505, 0.4606205250596659, 0.0, 0.019325842696629212, 1.5223880597014925, 0.032768675367953345, 0.5970149253731343, 4.4411764705882355, 9, 1, 416, 0.09415730337078651, 0.8248465149873601, drama
    0.0148861646234676, 0.7090909090909091, 0.0, 0.021891418563922942, 1.7222222222222223, 0.03402854006586169, 0.1111111111111111, 3.967741935483871, 17, 1, 106, 0.09632224168126094, 0.8174962292609351, drama
    0.015503875968992248, 0.7073170731707317, 0.039473684210526314, 0.020671834625323, 2.2857142857142856, 0.03827751196172249, 0.0, 5.6875, 18, 1, 82, 0.10594315245478036, 0.835030549898167, epic
    0.006345177664974619, 0.64, 0.03225806451612903, 0.031725888324873094, 1.75, 0.03201219512195122, 0.0, 7.571428571428571, 26, 1, 100, 0.12690355329949238, 0.8156424581005587, epic
    0.0023745918670228555, 0.6093023255813953, 0.0, 0.029385574354407838, 0.4594594594594595, 0.02661064425770308, 0.19444444444444445, 24.0, 102, 4, 428, 0.12763431285247848, 0.8395340097707629, poetry
    0.00281483294578387, 0.432661717921527, 0.012987012987012988, 0.02753640925223351, 0.6415094339622641, 0.019772071948372924, 0.5, 13.441176470588236, 33, 1, 932, 0.11540815077713866, 0.8539696833258292, report
    0.002178649237472767, 0.7575757575757576, 0.0, 0.026143790849673203, 0.6, 0.027989821882951654, 0.5, 21.0, 29, 15, 65, 0.1437908496732026, 0.8227146814404432, poetry

5 Experimente und Evaluation  
-------
Es wurden Experimente auf den grob und fein gegliederten Datensätzen ausgeführt.  
Als Baseline wird in beiden Fällen ein ZeroR Algorithmus verwendet der alle Instanzen mit der häufigsten Klasse klassifiziert.  
Die Evaluation verwendet CrossValidation mit 10 folds.

**Grober Datensatz**  
Der grob gegliederte Datensatz enthält 1261 Instanzen die auf 4 Klassen verteilt sind. Diese Verteilung verhält sich wie folgt:

    222 Epische Texte
    291 Dramen
    302 Artikel
    446 Gedichte


Die *Baseline* klassifiziert etwa 35% aller Instanzen korrekt. Im folgenden eine detailliertere Übersicht der Ergebnisse der Baseline:

    Correctly Classified Instances         446               35.3688 %
    Incorrectly Classified Instances       815               64.6312 %
    Kappa statistic                          0     
    Mean absolute error                      0.3667
    Root mean squared error                  0.4282
    Relative absolute error                100      %
    Root relative squared error            100      %
    Total Number of Instances             1261     

    === Detailed Accuracy By Class ===

                   TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                     0         0          0         0         0          0.495    epic
                     0         0          0         0         0          0.498    drama
                     0         0          0         0         0          0.496    report
                     1         1          0.354     1         0.523      0.496    poetry
    Weighted Avg.    0.354     0.354      0.125     0.354     0.185      0.496

Es wurde ein *Experiment* mit 9 verschiedenen Algorithmen durchgeführt.

    (1) rules.ZeroR '' 48055541465867954
    (2) bayes.NaiveBayes '' 5995231201785697655
    (3) functions.Logistic '-R 1.0E-8 -M -1' 3932117032546553727
    (4) functions.MultilayerPerceptron '-L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a' -5990607817048210779
    (5) functions.SimpleLogistic '-I 0 -M 500 -H 50 -W 0.0' 7397710626304705059
    (6) functions.SMO '-C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"functions.supportVector.PolyKernel -C 250007 -E 1.0\"' -6585883636378691736
    (7) lazy.KStar '-B 20 -M a' 332458330800479083
    (8) meta.AdaBoostM1 '-P 100 -S 1 -I 10 -W trees.DecisionStump' -7378107808933117974
    (9) trees.J48 '-C 0.25 -M 2' -217733168393644444

Die Ergebnisse zeigen, dass alle gewählten Algorithmen in unterschiedlichem Ausmaß die Baseline übertreffen.

    Dataset                   (4) function | (1) rules (2) bayes (3) funct (5) funct (6) funct (7) lazy. (8) meta. (9) trees
    ------------------------------------------------------------------------------------------------------------------------
    tyrex                     (30)   92.10 |   35.37 *   85.80 *   91.65     92.04     89.56 *   91.09     56.54 *   87.73 *
    ------------------------------------------------------------------------------------------------------------------------
                                   (v/ /*) |   (0/0/1)   (0/0/1)   (0/1/0)   (0/1/0)   (0/0/1)   (0/1/0)   (0/0/1)   (0/0/1)


Die besten Ergebnisse erreicht der MultilayerPerceptron. Logistic, SimpleLogistic und KStar erreichen jedoch Leistungen, die nicht signifikant schlechter sind. Dies ist besonders in Hinsicht auf Logistic und SimpleLogistic von Bedeutung, da ihre Berechnung bedeutend weniger aufwendig ist.

Eine genauere Betrachtung des MultiLayerPerceptrons liefert die folgende Evaluierung:

    Correctly Classified Instances        1164               92.3077 %
    Incorrectly Classified Instances        97                7.6923 %
    Kappa statistic                          0.8949
    Mean absolute error                      0.0452
    Root mean squared error                  0.1816
    Relative absolute error                 12.3251 %
    Root relative squared error             42.4158 %
    Total Number of Instances             1261     

    === Detailed Accuracy By Class ===

                   TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                     0.82      0.03       0.854     0.82      0.837      0.963    epic
                     0.945     0.014      0.952     0.945     0.948      0.981    drama
                     0.993     0.006      0.98      0.993     0.987      0.999    report
                     0.913     0.056      0.898     0.913     0.905      0.973    poetry
    Weighted Avg.    0.923     0.03       0.923     0.923     0.923      0.979

Bei einer Precision von 62.3077 % sind diese Ergebnisse mehr als zufriedenstellend.

Anhand der verschiedenen Precision und Recall Werte für die einzelnen Klassen lässt sich bereits eine Vermutung machen die mit der Confusion Matrix bestätigt wird.

    === Confusion Matrix ===

       a   b   c   d   <-- classified as
     182   1   4  35 |   a = epic
       4 275   1  11 |   b = drama
       1   1 300   0 |   c = report
      26  12   1 407 |   d = poetry

Während `drama` und `report` sehr gut klassifiziert werden, sowohl hinsichtlich Precision als auch Recall, gibt es Verwirrungen zwischen Epic und Poetry.

Gründe hierfür sind u.a. wohl Ähnlichkeiten in Hinblick auf Zeichensetzung und Schreibstil. Sowohl bezüglich der NounFrequency als auch der VerbFrequency sind Texte beider Klassen kaum zu unterscheiden.  
Features, die zur besseren Unterscheidung dieser Klassen dienen sollten, konnten aufgrund der Beschaffenheit der Texte zudem nicht immer richtig greifen. So sind die Epischen Texte leider nicht anhand der Paragraphen umgebrochen. Dadurch kann nicht zwischen Gedichtszeilen und layoutbedingten Umbrüchen in epischen Texten unterschieden werden.

Verbesserte Features (z.B. bzgl. Rhymes) und evtl. Parserfunktionalität, die Paragraphen erkennt könnten dieses Problem umgeben.

**Feiner Datensatz**

verteilung

baseline

experimente

bester algo

	summary

	confusion

auswertung

6 Auswertung
-------
blablabla

7 Aussichten
-------
Probleme (mehr und besser verteilte Daten; Featureergebnisse nicht immer wie erwartet(z.B.Rhyme bei Poetry); weitere Features benötigt (z.B. Terminologien))  
Überlegungen (Kombination mit anderen Projekten; weitere Experimente; feinere Klassen; )  

8 Literatur
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
