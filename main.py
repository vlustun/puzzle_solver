import requests
from bs4 import BeautifulSoup

def compile_table_list(rows):
    table_list = []
    for row in rows[1:]: 
        cells = row.find_all("td")
        for cell in cells:
            table_list.append(cell.get_text())
    return table_list

def process_html(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    table_tag = soup.table
    if table_tag is None:
        return "No table found in the HTML content."
    rows = table_tag.find_all("tr")
    table_list = compile_table_list(rows)
    return compile_list_of_dicts(table_list)

def compile_list_of_dicts(cells):
    list_compiled = []
    for i, item in enumerate(cells):
        if i % 3 == 0:
            new_dict = {}
            new_dict["x"] = int(item.strip())
        if i % 3 == 1:
            new_dict["char"] = item.strip()
        if i % 3 == 2:
            new_dict["y"] = int(item.strip())
            list_compiled.append(new_dict)

    
    if not list_compiled:
        return "No data found to process."
    ordered_y_list = []
    max_y = max(d["y"] for d in list_compiled)
    for y in range(max_y, -1, -1):
        y_list = [item for item in list_compiled if item["y"] == y]
        x_ordered = sorted(y_list, key=lambda d: d['x'])
        ordered_y_list.append(x_ordered)
    return prepare_lines(ordered_y_list)
    
    
def prepare_lines(lines):
    return "\n".join(prepare_line(line) for line in lines)

def prepare_line(line):
    string_to_print = ""
    previous_x_position = -1
    for item in line:
        x_position = item["x"] - previous_x_position - 1
        string_to_print += " " * x_position + item["char"]
        previous_x_position = item["x"]
    return string_to_print
         

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def solve_crypto(url): 
     content = fetch_html(url)
     message = process_html(content)
     print(message)
     

url = 'https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub'
# url = 'https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub'
solve_crypto(url)
