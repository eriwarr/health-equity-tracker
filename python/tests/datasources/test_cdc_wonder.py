import os
import pandas as pd
import requests
import xml.etree.ElementTree as ET

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(THIS_DIR, os.pardir, 'state_all.xml')


def load_xml_request(file_path):
    """
    Loads XML request data from a file.

    Args:
    file_path (str): Path to the XML file containing the request data.

    Returns:
    str: XML request data as a string.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='unicode')
    except Exception as e:
        print(f"Error loading XML file: {e}")
        return None


xml_request = load_xml_request(TEST_DIR)

# CDC WONDER API endpoint
url = "https://wonder.cdc.gov/controller/datarequest/D76"


def is_year(s):
    return s.strip().isdigit() and len(s.strip()) == 4


def test_fetch_and_save_xml_data(geo_level='state', breakdown='all'):
    response = requests.post(
        url, data={"request_xml": xml_request, "accept_datause_restrictions": "true"}
    )

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        data_table = root.find('.//data-table')

        data = []
        current_year = None

        for row in data_table.findall('r'):
            row_data = {}
            columns = row.findall('c')

            first_label = columns[0].get('l')
            if first_label and is_year(first_label):
                current_year = first_label.strip()

            if current_year:
                row_data['time_period'] = current_year
                breakdown_col = columns[1].get('l')
                row_data[breakdown] = breakdown_col or first_label

                if breakdown_col:
                    row_data['deaths'] = columns[2].get('v')
                    row_data['population'] = columns[3].get('v')
                    row_data['gun_deaths_per_100k'] = columns[4].get('v')
                else:
                    row_data['deaths'] = columns[1].get('v')
                    row_data['population'] = columns[2].get('v')
                    row_data['gun_deaths_per_100k'] = columns[3].get('v')

                data.append(row_data)

        df = pd.DataFrame(data)
        df.to_csv('testing_output.csv', index=False)
    else:
        print("Error:", response.status_code)
        print(response)
