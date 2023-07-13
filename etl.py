import requests


class EtlProccess:
    def __init__(self):
        self.url = None
        self.period = -1
        self.output_enable = False
        self.output_filepath = None
        self.output_file_format = None
        self.output_rewrite = False
        self.output_xls_sheetname = None
        self.output_xls_write_header = None
        self.output_xls_write_rownums = None
        self.output_csv_write_header = None
        self.output_csv_write_rownums = None
        self.output_csv_sep = None

    def get_text_by_url(self, url=None):
        if url:
            try:
                if response := requests.get(url):
                    result_text = response.text
                else:
                    result_text = f"\n Ошибка с кодом {response.status_code} \n"
            except Exception as e:
                result_text = f"\n Ошибка {e} \n"

        return result_text
