#!/usr/bin/env python3

"""
Email: richard.lalonde@wwt.com
"""

__author__ = 'Richard Lalonde'
__version__ = '1.1'
__license__ = 'GNU GPL v3.0'

import re
import logging
import itertools
import smtplib
from os.path import getmtime
from time import time
from pathlib import Path
from openpyxl import load_workbook
from difflib import unified_diff
from email.message import EmailMessage


class SourceDevice:
    """
    Class containing networking device information
    """

    def __init__(self, log_path: Path):
        """
        Initiates all
        """
        self.log_file_path = log_path
        self.log_parent_path = log_path.parent
        self.log_filename = log_path.name
        self.log_modified_time = getmtime(log_path)
        self.device_type = None
        self.device_name = None
        self.site_name = None
        self.serial_number = None
        self.net_info = {}
        self.error_list = []


    @property
    def hostname(self):
        return f'{self.device_name}.{self.site_name}'

    @hostname.setter
    def hostname(self, name: str):
        device_name, site_name = name.split('.')
        self.device_name = device_name
        self.site_name = site_name

    @hostname.deleter
    def hostname(self):
        self.device_name = None
        self.site_name = None


    @property
    def device_type(self):
        if self.device_type == None:
            if re.match(r'^swc1', self.log_filename):
                device_type = 'core1'
            if re.match(r'^swc2', self.log_filename):
                device_type = 'core2'
            if re.match(r'^sw[0-9][a-z]|^swlp1', self.log_filename):
                device_type = 'access'
            if re.match(r'^SPARE', self.log_filename):
                device_type = 'spare'
        return device_type

    @property
    def net_info(self):
        """
        A function to verify the management network information in the startup config.
        Reference information was pulled from the documentation provided the Project Engineers
        and is not guaranteed or intended to cover every project.
        """
        if self.net_info == None:
            trigger = 0
            with open(self.log_file_path) as open_file:
                for line in open_file.readlines():
                    if 'interface Vlan31' in line:
                        trigger = 1
                        continue
                    if trigger == 1 and 'ip address ' in line:
                        net_info = line.strip().split(' ')
                        self.net_info.update({'ip': net_info[2]})
                        self.net_info.update({'netmask': net_info[3]})
                        trigger += 1
                        continue
                    if trigger == 2 and 'ip default-gateway' in line:
                        self.net_info.update({'gateway': line.strip().split(' ')[-1]})

        return self.net_info

    @property
    def startup_config(self):
        """
        Retrieves all data from a log file but saves only the startup config.
        This allows for easier comparison and parsing.
        """
        startup_config = {}
        append_state = False
        with open(self.log_file_path) as open_file:
            for index, line in enumerate(open_file.readlines(), start=1):
                if re.search(r'[Ss]h(ow)* start(up-config)*', line):
                    append_state = True
                    continue
                if append_state:
                    if line.strip() == 'end':
                        startup_config.update(
                            (index, line.strip()))
                        break
                    if line != '\n' and '!' not in line:
                        startup_config.update(
                            (index, line.strip()))
                else:
                    continue


    def is_valid_filename(self, regex: re.Pattern):
        match = re.match(regex, self.log_filename)
        if match == None:
            match = False
        return match


    def check_device_net_info(self, ip_info: dict):
        error_codes = {
            1: 'does not have the correct IP address.',
            2: 'does not have the correct subnet mask.',
            3: 'does not have the correct default gateway.'
        }

        error = []
        net_info = self.net_info
        if net_info['ip'].rsplit('.', 1)[1] == ip_info[self.device_name] \
                and net_info['netmask'] == ip_info['netmask'] \
                and net_info['gateway'].rsplit('.', 1)[1] == ip_info['gw']:
            return
        if net_info['ip'].rsplit('.', 1)[1] != ip_info[self.device_name]:
            error.append(f'{self.hostname} ' +
                        error_codes[1] + '\nCurrent: {}'.format(net_info['ip']))
        if net_info['netmask'] != ip_info['netmask']:
            error.append(f'{self.hostname} ' +
                        error_codes[2] + '\nCurrent: {}'.format(net_info['netmask']))
        if net_info['gateway'].rsplit('.', 1)[1] != ip_info['gw']:
            error.append(f'{self.hostname} ' +
                        error_codes[3] + '\nCurrent: {}'.format(net_info['gateway']))

        return error


class ReferenceInformation:
    """
    Class containing Reference information
    """

    def __init__(self, ref_log_path: Path):
        """
        Initiates all
        """
        self.log_file_path = ref_log_path
        self.log_parent_path = ref_log_path.parent
        self.log_filename = ref_log_path.name
        self.site_name = None
        self.ip_info = {}
        self.show_inv = None
        self.show_ver = None
        self.show_env = None
        self.show_vlan = None
        self.show_license = None
        self.show_dir = None
        self.show_active_install = None
        self.startup_config = {}

    def build_reference_logs(self, site_name: str):
        """
        Creates a dictionary object of the reference templates to be called for each device type.
        So far, two core switches, access, and spare switches have been added to the reference document.

        A template Excel workbook is accessed, the worksheets are ID'ed and config contents are retrieved.
        Then, the data is processed line-by-line, stripping whitespace characters and ignoring blank lines.
        The header row is also ignored.

        This retrieves all the reference data we will need and stores it in memory all at once
        as opposed to opening, reading, and closing the file multiple times.
        """
        wb = load_workbook(filename=(str(self.log_file_path)))

        # Due to a config adjustment adding TACACs and AAA after these sites left - RL 3/2
        if site_name in ['0489', '2352']:
            self.startup_config = {
                # Takes cell value, strips leading white space characters, and creates a list of these values to assign them to a keyword for calling later
                'core1': [x.value.strip() for x in wb['core']['A'] if x.value != None and '!' not in x.value],
                'core2': [x.value.strip() for x in wb['core']['B'] if x.value != None and '!' not in x.value],
                'access': [x.value.strip() for x in wb['access']['A'] if x.value != None and '!' not in x.value],
                'spare': [x.value.strip() for x in wb['spare']['A'] if x.value != None and '!' not in x.value],
                'show': [x.value.strip() for x in wb['show']['A'] if x.value != None and '!' not in x.value]
            }
        else:
            self.startup_config = {
                # Takes cell value, strips leading white space characters, and creates a list of these values to assign them to a keyword for calling later
                'core1': [x.value.strip() for x in wb['core']['C'] if x.value != None and '!' not in x.value],
                'core2': [x.value.strip() for x in wb['core']['D'] if x.value != None and '!' not in x.value],
                'access': [x.value.strip() for x in wb['access']['B'] if x.value != None and '!' not in x.value],
                'spare': [x.value.strip() for x in wb['spare']['A'] if x.value != None and '!' not in x.value],
                'show': [x.value.strip() for x in wb['show']['A'] if x.value != None and '!' not in x.value]
            }
        return self.startup_config

    def update_reference_show_log(self, dev_hostname: str):
        show_dict={
            'show_inv': '',
            'show_ver': '',
            'show_env': '',
            'show_vlan': '',
            'show_license': '',
            'show_dir': '',
            'show_install_active': ''
        }

        with open(self.log_file_path, mode='r', encoding='UTF-8-sig') as sf:
            read_show=sf.read()
            read_show=re.sub(r'<HOSTNAME>', dev_hostname, read_show)
            show_regex_list=[re.compile(x.strip())
                            for x in read_show.split('!!!')]
            show_dict=dict(zip(show_dict.keys(), show_regex_list))

        return show_dict

    def update_unique_reference_info(self, source_device: SourceDevice):
        """
        Takes an existing reference configuration template and populates it with device specific information
        in order to check against a correct, expected value.
        """
        sourceList=self.startup_config[source_device.device_type]
        unique_source_list=[]

        for line in sourceList:
            if '!' in line:
                continue
            if '<STORE>' in line:
                unique_source_list.append(line.replace(
                    '<STORE>', source_device.site_name))
                continue
            if '<HOSTNAME>' in line:
                unique_source_list.append(line.replace(
                    '<HOSTNAME>', source_device.hostname))
                continue
            if all(substring in line for substring in ['<IP>', '<SUBNET>']):
                unique_source_list.append(
                    line.replace('<IP>', source_device.net_info['ip']).replace('<SUBNET>', source_device.net_info['netmask']))
                continue
            if '<GATEWAY>' in line:
                unique_source_list.append(line.replace(
                    '<GATEWAY>', source_device.net_info['gateway']))
                continue
            unique_source_list.append(line)

        return unique_source_list



def list_site_info(filepath: Path):
    """
    Scans QA directory tree for branches containing log files
    """
    if filepath.name.split(' ')[0] == 'POC':
        site_name=filepath.name.split(' ')[1][-4:]
    else:
        site_name=filepath.name.split(' ')[0][-4:]
    for branch in filepath.iterdir():
        if branch.is_dir() and 'QA' in branch.name:
            branch_info=(str(site_name), Path(branch))
        else:
            branch_info=(str(site_name), Path(filepath))

    return branch_info


def compare_show_commands(show_reference):
    return

def find_log_differences(target_list: list, reference_list: list):
    """
    Uses difflib to generate delta objects after comparing contents of two files.
    Read more about how difflib does this here: https://docs.python.org/3/library/difflib.html
    """
    diff=unified_diff(reference_list, target_list,
                        fromfile='reference', tofile='target', n=0)
    target_diff = []

    for result in diff:
        if re.match(r'^\+[A-Za-z]', result) and result[1:] not in reference_list:
            target_diff.append(result[1:])

    return target_diff


def add_reference_cert_id(target_diff_list: list, source_device: SourceDevice):
    """
    Adds the TrustPoint Self Signed certificate information to the reference configuration
    """
    token_id_pattern=re.compile(
        r'crypto pki trustpoint TP-self-signed-(?P<SelfSignedID>[0-9]{8,10})$')
    match_token_id=list(token_id_pattern.search(x).group('SelfSignedID')
                          for x in target_diff_list if token_id_pattern.search(x))

    regex_list=[re.compile(x) for x in (r'Using [0-9]{4,5} out of 2097152 bytes',
                  r'certificate self-signed 01 nvram:IOS-Self-Sig#[0-9].cer',
                  r'username cisco privilege 15 secret 9 [^ \t\n\r\f\v]{61}$',
                  r'enable secret 9 [^ \t\n\r\f\v]{61}$',
                  r'ntp authentication-key 40 md5 [A-Z0-9]{18} 7',
                  r'certificate ca 01 nvram:CiscoLicensi#[0-9]CA.cer',
                  r'client 172.26.202.21 server-key 7 [0-9A-Z]{22}',
                  r'client 172.29.202.21 server-key 7 [0-9A-Z]{22}',
                  r'memory free low-watermark processor 22917|memory free low-watermark processor 87534')]

    token_id_regex_list=[r'crypto pki trustpoint TP-self-signed-##########',
                           r'subject-name cn=IOS-Self-Signed-Certificate-##########',
                           r'rsakeypair TP-self-signed-##########',
                           r'crypto pki certificate chain TP-self-signed-##########']

    if match_token_id in [None, False]:
        print('No matches were found for the Token ID.')
    elif len(match_token_id) > 1:
        print("Multiple strings were matched while looking for the Token ID.\n" +
              '\n'.join(match_token_id))
    else:
        regex_list.extend([re.compile(re.sub(r'##########', match_token_id[0], x))
                           for x in token_id_regex_list])

    return regex_list


def compare_log_crypto(target_difference_list: list, crypto_regex_list: list):
    """
    Checks unique crypto hashes to ensure they are in the correct format and contain the correct characters before
    accepting them as correct.
    """
    issues_list=[]
    for difference in target_difference_list:
        print(f'\nChecking for match with {difference}...\n')
        if any([re.match(regex, difference) for regex in crypto_regex_list]):
            print('Match found!')
            continue
        else:
            print('No match found. Reporting...')
            issues_list.append(difference)

    return issues_list


def send_html_email(from_address: str, to_addresses: list, subject: str, filepath: Path, message: str, mail_server='mailhost.wwt.com', port=25):
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']=from_address
    msg['To']=to_addresses
    msg.set_content(message, subtype='html')
    try:
        with smtplib.SMTP(host=mail_server, port=port) as smtpObj:
            smtpObj.send_message(msg)
        print("Successfully sent email")
    except smtplib.SMTPException:
        logging.error(f'{filepath.name} - Unable to send email')
        print("Error: unable to send email")
    return


def autobot_love():
    love=('<code>'
            r'|        o      |<br>'
            r'|   _____|__    |<br>'
            r'|  (O   O)  )   |<br>'
            r'|   |---   |    |<br>'
            r'|  /=====   \   |<br>'
            r'| O)AUTO(O)  )  |<br>'
            r'|  |________|   |<br>'
            r'|  /____/____\  |<br>'
            r'| {-----(OOOOOO)|<br>'
            '</code>'
            )
    return love

