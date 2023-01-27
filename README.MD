# Multidimesnional Data Structures

# Table of Contents

# General Info
The aim of the project is the implementation of multidimensional data structures in a Programming Environment and their experimental evaluation with real data sets in basic operations: Build, Insert, Delete, Update, Searching (Similarity, kNN, Interval, Stabbing, 3-sided..etc) Queries.

# Summary
Our task is to implement a multi-dimensional index structure (k-d trees, quad trees, Range Trees and R-trees) to index a set of texts from computer scientists from Wikipedia with the format (Surname: String, #Awards: Integer, Education: text-vector). The index will be created based on the first two fields (surname, #awards) to find the scientists whose names belong to an alphabetical range and have received more awards than a user-defined threshold. Then, similarity queries will be performed on the third field (education) using the LSH method. The task also involves comparing the four methods: k-d + LSH, Quad+LSH, Range+LSH, R-trees + LSH.


# Technologies
- Python

# Installation

1. Clone the repo
```
git clone https://github.com/d4g10ur0s/Multidimesnional_Data_Structures_2023.git
```
2. Run Scripts
  - First cd to the scripts directory. Then run the following commands
```
./run_scrapy.sh
./run_preprocess.sh
```
- The first command creates a folder called scientists in the data folder where we have multiple json files scrapped from a wikipedia page.
- The second command creates a csv file inside the data folder where we store all our scientists from our json files


# Contact
You can always contact us through email : 
- 
- [rnicolaouceng@gmail]()

# Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

# License

[MIT](https://choosealicense.com/licenses/mit/)