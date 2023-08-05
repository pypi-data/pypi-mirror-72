import datetime
from pathlib import Path
from librec_auto.util import xml_load_from_path, extract_from_path, force_list, SubPaths, LogFile

# A .status file looks like this
# <librec-auto-status>
#    <message>Completed</message>
#    <exp-no>1</exp-no>\
#    <param><name>rec.neighbors.knn.number</name><value>30</value></param>
#    <date>June 28, 11:00 PM</date>
# </librec-auto-status>


class Status():

    _HEADER = '<?xml version="1.0"?>\n<!-- DO NOT EDIT. File automatically generated by librec-auto -->\n'
    _TEMPLATE_FRONT = '<librec-auto-status>\n<message>{}</message>\n<exp-no>{}</exp-no>\n<date>{}</date>\n'
    _TEMPLATE_END = '</librec-auto-status>\n'
    _TEMPLATE_LINE = '<param><name>{}</name><value>{}</value></param>\n'

    m_name = None
    m_status_xml = None
    m_message = None
    m_params = None
    m_vals = None
    m_log = None
    m_subpaths = None

    def __init__(self, sub_paths):
        self.m_subpaths = sub_paths
        status_path = self.m_subpaths.get_path('status')

        if status_path.exists():
            self.m_name = sub_paths.subexp_name
            self.m_status_xml = xml_load_from_path(status_path)
            self.m_message = extract_from_path(self.m_status_xml, ['librec-auto-status', 'message'])
            self.m_log = LogFile(self.m_subpaths)
            params = extract_from_path(self.m_status_xml, ['librec-auto-status', 'param'])
            if params != None:
                self.process_params(force_list(params))
            else:
                self.m_params = []
                self.m_vals = []

    def __str__(self):
        params_string = self.get_params_string()
        results_string = self.get_log_info()
        return f'Status({self.m_name}:{self.m_message}{params_string} Overall{results_string})'

    def is_completed(self):
        return self.m_message == 'Completed'

    def process_params(self, param_xml):
        param_list = []
        val_list = []

        for pdict in param_xml:
            param_list.append(pdict['name'])
            val_list.append(pdict['value'])

        self.m_params = param_list
        self.m_vals = val_list

    def get_params_string(self):
        params_string = ''
        if self.m_params == []:
            return " No parameters"
        for param, val in zip(self.m_params, self.m_vals):
            params_string += f' {param}: {val}'
        return params_string

    def get_log_info(self):
        kcv_count = self.m_log.get_kcv_count()
        if kcv_count is None:
            return self.get_metric_info(self.m_log, 0)
        else:
            return self.get_metric_info(self.m_log, -1)

    def get_metric_info(self, log, idx):
        metric_info = ''
        for metric_name in log.get_metrics():
            metric_value = log.get_metric_values(metric_name)[idx]
            metric_info = metric_info + f' {metric_name}: {float(metric_value):.3f}'
        return metric_info


    # Accept list of vars and tuples
    @staticmethod
    def save_status(msg, exp_count, var_names, value_tuple, config, paths):
        status_file = paths.get_path('status')
        status_front = Status._TEMPLATE_FRONT.format(msg, exp_count, datetime.datetime.now())

        status_params = ''

        for var, val in zip(var_names, value_tuple):
            status_params = status_params + Status._TEMPLATE_LINE.format(var, val)

        status_info = Status._HEADER + status_front + status_params + Status._TEMPLATE_END

        with status_file.open(mode='w') as fh:
            fh.write(str(status_info))
