import requests 
from bs4 import BeautifulSoup
import pandas as pd

drug_df = pd.read_csv("drug-accession-numbers.csv")
pd.set_option('display.max_colwidth', -1)

def parse_html(url):
    html = requests.get(url)
    data = BeautifulSoup(html.content, "html.parser")
    
    return data

def return_approved(url):
    """[summary]

    Args:
        data ([type]): [description]
        
    Returns:
        A list of the approved drugs for the selected cancer type
        
    """
    
    data = parse_html(url)
    
    links_list = [li.find("a") for li in data.find_all("ul", class_="no-bullets no-description")[0]]

    links_list = [x for x in links_list if x!=None]
    
    links_list = [x for x in links_list if not isinstance(x, int)]
    

    link_text_list = [link.text for link in links_list ]

    
    return link_text_list

def generate_dan(drug):
    dan = drug_df.loc[ (drug_df["DRUG"]==drug), "DAN"]
    i = int(drug_df[drug_df["DRUG"]==drug].index.values)
    dan = drug_df.loc[i, "DAN"]
    
    url = "https://go.drugbank.com/drugs/" + dan
    
    return dan, url

def name_drug(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    generic_name = data.find_all("dd", class_="col-xl-4 col-md-9 col-sm-8 pr-xl-2")[0].text
    
    return generic_name

def state_drug_status(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    status = data.find_all("dd", class_="col-xl-4 col-md-9 col-sm-8")[-1].text
    
    return status

def return_formula(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    weight_formula = data.find_all("dd", class_="col-xl-8 col-md-9 col-sm-8")
    
    formula = weight_formula[-1].text

    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    return (formula.translate(SUB))

def return_weight(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    weight_formula = data.find_all("dd", class_="col-xl-8 col-md-9 col-sm-8")

    weight = float(weight_formula[0].text.split(" ")[((weight_formula[0].text.split(" ").index("Monoisotopic:")) + 1)])
    
    weight = float("{:.2f}".format(weight))
    
    return weight
    
def return_img_url(drug):
    dan = generate_dan(drug)[0]
    image_url = "https://go.drugbank.com/structures/" + dan + "/image.svg"
    
    return image_url

def return_targets(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    targets_links_list = (data.find_all("table", class_="table table-sm responsive-table"))[0].find_all("a")
    
    targets_links_list = [target.text for target in targets_links_list]
    
    return targets_links_list

def return_enzymes(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    try:
        enzymes_list = (data.find("div", class_="bond-list-container enzymes").find_all("strong"))
        
        enzymes_list = [enzyme.find("a").text for enzyme in enzymes_list]
        
        return enzymes_list
    except:
        return ["No Enzymes Found"]

def return_transporters(drug):
    url = generate_dan(drug)[-1]
    data = parse_html(url)
    
    try:
        transporters_list = (data.find("div", class_="bond-list-container transporters").find_all("strong"))
        
        transporters_list = [transporter.find("a").text for transporter in transporters_list]
    
        return transporters_list
    except:
        return ["No Transporters Found"]

def return_similar(drug):
    dan = generate_dan(drug)[0]
    
    url = "https://go.drugbank.com/structures/search/small_molecule_drugs/structure?database_id=" + str(dan) + "&search_type=similarity#results"
    
    data = parse_html(url)
      
    similar_structures = (data.find("tbody"))
    
    names_list = similar_structures.find_all("strong")
    names_list = [name.text for name in names_list[1: ]]
    
    score_list = similar_structures.find_all("div", class_="search-score label label-default")
    score_list = [score.text for score in score_list]
    
    L = []
    status_list = (similar_structures.find_all("td", class_="search-hit-info"))
    status_list = [status.find_all("span") for status in status_list]

    for i in range(len(status_list)):
        for j in range(len(status_list[i])):
            status_list[i][j] = status_list[i][j].text
        L.append(" ".join(status_list[i])) 

    L = L[1: ]
    
    formula_list = similar_structures.find_all("div", class_="structure-formula mb-3")
    formula_list = [formula.text for formula in formula_list[1: ]] 
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    formula_list = [formula.translate(SUB) for formula in formula_list] 
    
    mass_list = similar_structures.find_all("div", class_="structure-mass-mt-3")
    mass_list = [mass.text for mass in mass_list[1: ]]
    
    dan_list = similar_structures.find_all("a", class_="btn btn-card")
    dan_list = [dan.text for dan in dan_list[1: ]]
    ana_url_list = ["https://go.drugbank.com/drugs/" + dan for dan in dan_list]
    
    ana_html_list = [requests.get(ana_url) for ana_url in ana_url_list]
    ana_data_list = [BeautifulSoup(ana_html.content, "html.parser") for ana_html in ana_html_list]
    
    remarks_list = [ana_data.find("dd", class_="col-xl-10 col-md-9 col-sm-8").text for ana_data in ana_data_list]
    
    
    analogous_df = pd.DataFrame(columns=["Name of Compound", "Tanimoto Coefficient", "Research Status", "Chemical Formula", "Monoisotopic Mass"])
    
    analogous_df["Name of Compound"] = pd.Series(names_list)
    analogous_df["Tanimoto Coefficient"] = pd.Series(score_list)
    analogous_df["Research Status"] = pd.Series(status_list)
    analogous_df["Chemical Formula"] = pd.Series(formula_list)
    analogous_df["Monoisotopic Mass"] = pd.Series(mass_list)
    analogous_df["Remarks"] = pd.Series(remarks_list)
    
    return analogous_df