# TyRex
TyRex - Text Type Recognition (Textarterkennung)
========================================================================

Authors
-------
Lydia Hofmann, Svenja Lohse and Tonio Weidler  
(hofmann|lohse|weidler)@cl.uni-heidelberg.de  
Institute of Computational Linguistics  
Heidelberg University, Germany  

Outline  
----
Goal of this project ...  
In the first step the algorithm ...  
Further steps to be made ...  
  
Requirements  
------------
TyRex is written in *Python3*!  
  - https://pypi.python.org/pypi/html2text or ```pip install html2text``` (needs sudo)  
  - https://perso.limsi.fr/pointal/doku.php?id=dev:treetaggerwrapper or ```pip install treetaggerwrapper``` (needs sudo)  
  - http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/ the TreeTagger  
  
Usage  
-----  
  - learn from data and create arff: ```bash learn.sh -s DIR -d DIR -m DIR -f FILE [options]```  
    (all directories need a trailing "/")
  - run ```bash learn.sh -h``` to get further help and options
  
  - get a files text type: ```bash tyrex.sh FILENAME```
  
Structure of the Single Program Parts - Preprocessing  
---------------------------------------------------------------
**Parser**    
*parser/Parser.py*  
Main Parser SuperClass, that takes a single path to a file. Contains methods to read this File (with different Encodings) and the converter method, that creates the normalized text.

**MultiParser**    
*parser/MultiParser.py*  
Subclass of a/the Parser. Takes a directory instead of a single files path and converts all contained files to a normalized version. Saves this Version as a new file at a given location.

Structure of the Single Program Parts - Main Algorithm  
----------------------------------------------------------------
**Feature Extraction Algorithm (FEA)**  
*FeatureExtractionAlgorithm.py*  
Main Class, containing all the Methods that calc the Features.

**Automized FEA**  
*AutomizedFEA.py*

Structure of the Single Program Parts - Postprocessing  
----------------------------------------------------------------
**ARFFBuilder**  
*ARFFBuilder.py*  
Description  

**Text Type Recognizer**  
*recognizeTextType.py*  
Description  

See the comments in the files for more information regarding other methods of the Class.  
