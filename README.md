# GradeScopeCodeSimilarityAPI
This is a python script to grab and parse the Review Similarity Report html into nicely formated `.csv` files 
with more helpful data formating such as group collaberations

# Dependencies
`python3.10+` may work for earlier versions but not tested\
`pandas`

# Usage
`python3 parse.py <assessment_num> <gradescope_html> <similarity_cuttoff> <file_to_compare_1> ... <file_to_compare_N>`

# How to get report html `<gradescope_html>`
sign into gradescope and navigate to the simularity report you want to collect

next press `CTRL+SHIFT+I` and click on the network tab

refresh the page and you should see a html file pop up

right click the request and select `copy as cUrl`

![alt text](https://github.com/jmshima01/GradescopeCodeSimilarityAPI/blob/main/img.png)

then paste the result in your terminal and redirect it to a file of your choice
`curl ... > file.html`

Now you have the raw html and are ready to parse!

# Full Example for Assessment 2:

`python3 parse.py 2 report2.html 70 submission.py main.py`
