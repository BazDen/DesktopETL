import xmltodict
import pandas as pd
import json


def _recurse_parse_dict(d: dict) -> list:
    output_list = []
    for v in d.values():
        if isinstance(v, dict):
            output_list = output_list + _recurse_parse_dict(v)
        elif isinstance(v, list):
            output_list = output_list + v

    return output_list


def xml_to_df(input_text: str, clear_NaN: bool = False):
    df = pd.DataFrame()
    try:
        xml_dict = xmltodict.parse(input_text)
        xml_list = _recurse_parse_dict(xml_dict)
        df = pd.DataFrame(xml_list)
        if clear_NaN:
            df = df.fillna('')
    except Exception as e:
        print(e)

    return df


def json_to_df(input_text: str, clear_NaN: bool = False):
    df = pd.DataFrame()
    try:
        json_dict = json.loads(input_text)
        json_list = _recurse_parse_dict(json_dict)
        df = pd.DataFrame(json_list)
        if clear_NaN:
            df = df.fillna('')
    except Exception as e:
        print(e)
    
    return df