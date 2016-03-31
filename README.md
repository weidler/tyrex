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
Goal of this project is an unsupervised classification of text types.  
In the first step the algorithm normalises the given texts, with a so-called "Parser". After that it analyses the preprocessed data with an extensible set of features returning an ARFF-file with the results, which Weka uses to run algorithms with and to evaluate the outcome.  
Further steps would be i.a. an expansion of features and data to differentiate more classes successfully.   

Requirements  
------------
TyRex is written in *Python3*!  
  - https://pypi.python.org/pypi/html2text or ```pip3 install html2text``` (needs sudo)  
  - https://perso.limsi.fr/pointal/doku.php?id=dev:treetaggerwrapper or ```pip3 install treetaggerwrapper``` (needs sudo)  
  - http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/ the TreeTagger  

Though this *should* be all additional software needed, you might miss some usually standard packages in python.
Contact us if further help is needed.

Data (not included in GitHub due to copyright)
-----

| Directory    | Content                                                                                                                                                                                                                                                                                                              |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| raw_data     | unnormalized files for coarse classes                                                                                                                                                                                                                                                                                |
| fine_data    | contains for fine-grained classes:   <br>new_data - unnormalized files <br>new_data.zip - those as archive data_fine - normalized files  <br>feature_maps_fine - JSON feature map files  this data takes more than 3h to compute, you should not recompute it if not necessary. Use -j in learn.sh to use the already calced data! |
| data         | normalized files for coarse classes                                                                                                                                                                                                                                                                                  |
| feature_maps | JSON feature maps for coarse classes                                                                                                                                                                                                                                                                                 |
| test_data    | few files to test learn.sh without waiting too long for results                                                                                                                                                                                                                                                      |

data* and feature_maps* folders contain precalculated data, that takes some time to get calculated. To test the system, test_data may be enough.

Usage  
-----  
  * learn from data and create arff: ```bash learn.sh -s DIR -d DIR -m DIR -f FILE [options]```  
    (all directories need a trailing "/")
  * run ```bash learn.sh -h``` to get further help and options
  * get a files text type: ```bash tyrex.sh FILENAME```

Structure of the Single Program Parts - Preprocessing  
---------------------------------------------------------------
**Parser**    
*parser/Parser.py*  
Main 'Parser' SuperClass, that takes a single path to a file. Contains methods to read this File (with different Encodings) and the converter method, that creates the normalized text.

**MultiParser**    
*parser/MultiParser.py*  
Subclass of a/the 'Parser'. Takes a directory instead of a single files path and converts all contained files to a normalized version. Saves this Version as a new file at a given location.

Structure of the Single Program Parts - Main Algorithm  
----------------------------------------------------------------
**Feature Extraction Algorithm (FEA)**  
*FeatureExtractionAlgorithm.py*  
Main Class, containing all the Methods that calc the Features.

**Automized FEA**  
*AutomizedFEA.py*
Automatically applies FEA on a whole directory with some options.  

Structure of the Single Program Parts - Postprocessing  
----------------------------------------------------------------
**ARFFBuilder**  
*ARFFBuilder.py*  
This class manages ARFF file construction out of FEA results.

**Text Type Recognizer**  
*recognizeTextType.py*  
Class that takes a filepath and calculates the files normed text and vector.
It then returns the most likely text type.

See the comments in the files for more information regarding other methods of the Class and detailed descriptions.  
