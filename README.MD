# Multidimesnional Data Structures

# Table of Contents

# General Info
The purpose of this computer science project is to present the focuses on optimizing range and similarity queries on text datasets using quadratic trees, range trees, and R-trees. The project aims to compare the performance of these tree-based data structures in terms of query processing time, space complexity, and accuracy.


# Technologies && Library Versions
- Python
```:Libraries
gensim              4.2.0
numpy               1.23.5
pandas              1.3.5
scikit-learn        1.2.1
Scrapy              2.7.1
```
# Installation

1. Clone the repo
```
git clone https://github.com/d4g10ur0s/Multidimesnional_Data_Structures_2023.git
```

2. Create a folder called data in the main directory

3. Run Scripts
  - First cd to the scripts directory. Then run the following commands
```
./run_scrapy.sh
```
- The first command creates a folder called scientists in the data folder where we have multiple json files scrapped from a wikipedia page.

4. Run preprocess.py
- If you are running preprocess.py for the first time u need to uncomment the following lines once. Run it and then comment them again.
```python
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus = api.load('text8')
    print(inspect.getsource(corpus.__class__))
    print(inspect.getfile(corpus.__class__))
    model = w2v(corpus)
    model.save('.\\readyvocab.model')
```


# Contact
You can always contact us through email : 
- [aledadu@hotmail.com]()
- [rnicolaouceng@gmail]()

# Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

# License

[MIT](https://choosealicense.com/licenses/mit/)