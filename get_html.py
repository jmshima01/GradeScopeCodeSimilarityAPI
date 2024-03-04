import subprocess
import sys

"""
runs curl using a provided gradescope cookie to get html for parsing Similarity Report
"""

# hardcoded for CSCI 128
COURSE_ID = 687807
ASSIGNMENT_ID = {
    1:"3831764",
    2:"3831766",
    3:"3831768",
    4:"3831771",
    5:"3831772",
    6:"3831774",
    7:"3831777",
    8:"3831778",
    9:"3831781",
    10:"3831756",
    11:"3831758",
    12:"3831760",
    13:"3831763"
}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(sys.argv)
        print("Usage: python3 get_html.py assessment_num cookie")
        exit(1)

    f = open(f"report{sys.argv[1]}.html","w")
    cmd =f"curl \'https://www.gradescope.com/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID[int(sys.argv[1])]}/review_similarity\' -H \'Cookie: {sys.argv[2]}\' > report{sys.argv[1]}.html"
    process = subprocess.Popen(cmd,
                     stdout = f, 
                     stderr = subprocess.STDOUT,
                     text = True,
                     shell = True
                     )
    process.communicate()
    f.close()