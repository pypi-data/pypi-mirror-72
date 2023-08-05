README.md
=========

Kola-indicator is a set of scripts to compute a collective dynamic
indicator from MOOC forums. It applies LSA and SNA technics to identify
groups of messages that could be working in groups.

The following scripts are also module. To get usage use the -h flag

circuits
~~~~~~~~

-  programme principal qui appelle les autres et effectue le calculs de
   circuits

harmonize (harmonisation:sub:`data`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  En entrée: les bases de données coursera c17 et c18. Différents
   format
-  En sortie: les données dans une même table et avec les mêmes noms de
   colonnes

tokenizer (mlk:sub:`tokenizer`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  à partir du fichier généré par harmonisation data

le tokenize et en sauvegarde les textest dans le dossier Tokenized

koNLP
~~~~~

-  Effecute le texte wrangling. Peut utiliser le mutliprocessing

koNMF
~~~~~

-  Effecture la réduction de matrice. Peut utiliser le mutliprocessing
