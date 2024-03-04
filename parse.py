from sys import argv
from html_parse import Gradscope_Similarity_HTML_Parser

if __name__ == "__main__":
    
    if len(argv) < 5:
        print("Usage: python3 main.py assessment_num html_path percent_cutoff submission_name1 ... submission_nameN")
        exit(1)
    
    assessment,path,cutoff,files_to_comp = argv[1],argv[2],argv[3],argv[4:]
    
    try:
        cutoff = int(argv[3])
    except:
        print("percent_cutoff must be int!")
        print("Usage: python3 main.py assessment_num html_path percent_cutoff file_to_comp")
        exit(1)
    
    parser = Gradscope_Similarity_HTML_Parser(html_file_path=path,cutoff_simularity=cutoff,assessment=assessment,files_to_comp=files_to_comp)

    parser.generate_all_csv()
    parser.generate_group_csv()
    parser.generate_pairs_csv()
