# GradeScopeCodeSimilarityAPI
This is a python script to grab and parse the Review Similarity Report html into nicely formated `.csv` files 
with more helpful data formating such as group collaberations

Many params Hardcoded currently for CSCI128

# Dependencies
`python3.10+` may work for earlier versions but not tested\
`pandas`

# Usage
`python3 parse.py <assessment_num> <gradescope_html> <similarity_cuttoff> <file_to_compare_1> ... <file_to_compare_N>`

# How to get report html `<gradescope_html>`
`python3 get_html.py <assesment_num> <gradescope_cookie>`

# How to get a cookie `<gradescope_cookie>`
There are many ways to obtain a gradescope cookie for `<gradescope_cookie>`, the easiest\
is to sign into gradescope and then press...\
`CTRL+SHIFT+I`\
and type into console...\
`console.log(document.cookie)`\
and the resulting should be passes quoted into the above arg for the python script\

# Full Example for Assessment 2:
`python3 get_html.py 2 '<gradescope_cookie>'`\
`python3 parse.py 3 report2.html 50 submission.py main.py`
