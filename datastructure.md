Die Texte (*raw_data*) werden im Rohformat nach Dateitypen/Formatierung sortiert und dementsprechend an den geeigneten **Parser** übergeben.
Die vom **Parser** erstellte *normierte* Version des Textes wird im Datensatz (*data*) des Programms hinterlegt.

Der **Feature Extractor Algorithm** (FEA) enthält verschiedene Methoden, mit denen er die Features aus den normierten Texten extrahiert und in einem JSON File
hinterlegt. Aus diesem kann wahlweise vom **FEA** auch gelesen werden um je nach Bedarf die Daten neu zu berechnen oder nur zu erweitern.

Zuletzt liest ein **ARFF-Builder** dieses *dataset* und wandelt es in ARFF um, um von WEKA verarbeitet werden zu können.
