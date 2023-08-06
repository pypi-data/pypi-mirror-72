import json
import random
from urllib.parse import urljoin
import re
import fnmatch
import sys
import logging
import string
import time
import zipfile
import os
import pickle
import hashlib 

import requests
from obspy import UTCDateTime
# from params import params as p

try:
    pickle_dir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    pickle_dir = './'

pickle_path = os.path.join(pickle_dir,"params.pickle")

with open(pickle_path, "rb") as file:
    params = pickle.load(file) 

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


p = Struct(**params)

# params obj
##############
# pickle_path = os.path.join(pickle_dir,"params_obj.pickle")

# with open(pickle_path, "rb") as file:
#     p = pickle.load(file) 
##############



# 10 day / single station
# 1 day / multiple stations
# 50 stations
# Clearly this whole API is designed by someone who has no clue about seismic data

# Results codes of getData requests:
#   101: something wrong
#   109: success

ONE_DAY = 60*60*24
TEN_DAYS = ONE_DAY * 10
DISPOSABLE_EMAIL_API = 'https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/md5/'

class WFRequest:
    order_number = None
    start_time = None
    end_time = None
    data_type = None
    instrument = None
    networks = None
    stations = None
    location = None
    device_codes = None
    components = None
    e_mail = None

    def __init__(self,**kwargs):
        # print(kwargs)
        self.create_request(**kwargs)

    def time_formatter(self,time):
        if type(time) != UTCDateTime:
            t = UTCDateTime(time)
        else:
            t = time
        return f'{t.year}-{t.month}-{t.day} {t.hour}:{t.minute}:{t.second}'

    def create_request(self,stations=[],components=[],email='',order_number=None,starttime=None,endtime=None):
        # order is important!
        self.order_number = f'{order_number}'
        self.start_time = self.time_formatter(starttime)
        self.end_time = self.time_formatter(endtime)
        self.data_type = "mseed"
        self.instrument = False # return instrument response?
        self.networks = [station.network for station in stations]
        self.stations = [station.code for station in stations]
        self.location = [None] * len(stations)
        self.device_codes = [station.device_code for station in stations]
        self.components = [components] * len(stations)
        self.e_mail = email
    
    @property
    def data(self):
        return self.__dict__

class Network:
    pass

class Station:
    network = ''
    code = ''
    def __init__(self,sta_dict={},**kwargs):
        if not sta_dict:
            for key in p.STATION_KEYS:
                setattr(self,key,None)
        else:
            for key in p.STATION_KEYS:
                setattr(self,key,sta_dict[key])
    
    def __str__(self):
        return f'Network: {self.network}, Code: {self.code}'

    def __repr__(self):
        return f'<Station: {self.code}, Network: {self.network}>'

    @property
    def device_code(self):
        if self.deviceN or self.deviceNE or self.deviceNN or self.deviceNZ:
            return 'N'
        elif self.deviceH or self.deviceHE or self.deviceHN or self.deviceHZ:
            return 'H'
        elif self.deviceL or self.deviceLE or self.deviceLN or self.deviceLZ:
            return 'L'

class Client:
    all_stations = []
    stations = []
    networks = []
    queue = []
    starttime = None
    endtime = None
    _user_agent = p.USER_AGENTS[0]
    randomize_user_agent = True
    randomize_email = True
    _headers = p.HEADERS_DEFAULT
    _email = ''
    _order_number = None
    _wf_request = None
    _max_retries = 1
    verbosity = 0
    dry_run = False
    _CHUNK_SIZE = 128

    def __init__(self, dry_run=False, email="", verbosity=0, temp_path="temp"):
        print(p.WARNING)
        # randomly select a user agent
        self.verbosity = verbosity
        self._init_verbosity()
        self.dry_run = dry_run
        self.temp_path = temp_path
        if email:
            self._email = email
            self.randomize_email = False
        if self.randomize_user_agent:
            self.shuffle_useragent()
        else:
            self._user_agent = p.USER_AGENTS[0]

    def _init_verbosity(self):
        if self.verbosity == 3:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1

            logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
            
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def set__user_agent(self, user_agent):
        self._user_agent = user_agent
        self._headers['User-Agent'] = user_agent

    def _generate_email(self):
        # using temp-mail.org to generate random email address
        if not self.randomize_email:
            # self._email = 'hefix31026@mailrnl.com'
            return 
        else:
            n = random.randint(5,15)
            self._email = ''.join(random.choice(string.ascii_letters) for x in range(n)) + '@mailrnl.com'

    def shuffle_useragent(self):
        self._user_agent = random.choice(p.USER_AGENTS)

    def make_request(self,url,params=None, request_type="GET",json=None, headers=None, suppress_log=False):
        if not headers:
            headers = self._headers
        if request_type == "GET":
            resp = requests.get(url,params=params,headers=headers)
        elif request_type == "POST":
            resp = requests.post(url,json=json,headers = headers)
        elif request_type == "OPTIONS":
            resp = requests.options(url,headers=headers)
        if self.verbosity >= 2:
            print('*'*10)
            print(f'URL: {url}')
            print(f'JSON: {json}')
            print(f'HEADERS: {resp.request.headers}')
            print(f'METHOD: {request_type}')
            print(f'REQUEST BODY: {resp.request.body}')
            if not suppress_log:
                print(f'RESPONSE CONTENT:')
                print(resp.content)
            print('*'*10)
        return resp

    def make_post_request(self, url, json=None, headers=None, suppress_log=False):
        if self.randomize_user_agent:
            self.shuffle_useragent()
        resp = self.make_request(url, json=json, request_type="POST", headers=headers, suppress_log=suppress_log)
        # if resp.status_code == 200:
        # return resp.json()
        return resp
    
    def get_networks(self):
        pass

    def get_stations(self,networks=p.NETWORKS):
        data = p.GET_STATIONS_DEFAULT_DATA
        url = urljoin(p.HOST,p.GET_STATIONS_URL)
        stations_dict = self.make_post_request(url, json=data, suppress_log=True).json()
        stations = [Station(station_dict) for station_dict in stations_dict]
        self.all_stations = stations

    def _get_order_number(self):
        url = urljoin(p.HOST,p.GET_ORDER_NUMBER_URL)
        data = self._order_request()
        resp = self.make_request(urljoin(p.CHECK_HAS_REQUEST_URL, self._email),request_type="GET")
        # print('has request already?')
        # print(resp.json())
        # print('order request data')
        # print(data)
        # print('order number')
        # print(self._order_number)
        return self.make_post_request(url,json=data).json()

    def _order_request(self):
        return {
            'e_mail': self._email,
            'date': UTCDateTime().__str__(),
            'id': 0, 
        }

        
    def match_stations(self, net_glob, sta_glob, cha_glob):
        sta_regexp = fnmatch.translate(sta_glob)
        cha_regexp = fnmatch.translate(cha_glob)
        net_regexp = fnmatch.translate(net_glob)
        return [station for station in self.all_stations if re.match(sta_regexp,station.code) and re.match(cha_regexp,station.device_code) and re.match(net_regexp,station.network)]

    def _extract_file(self, file_path, outdir):
        if not zipfile.is_zipfile(file_path):
            print(f'ERROR: not a zip file: {file_path}')
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            file_list = zip_ref.infolist()
            zip_ref.extractall(outdir)
        return file_list

    def _download_file(self, url, outdir,file_path):
        file_name = os.path.basename(file_path)
        file_path = os.path.join(outdir, file_name)
        if self.verbosity >= 1:
            print(f'Downloading {url} to {file_path}')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        resp = requests.get(url, stream=True)
        with open(file_path, 'wb') as fd:
            for chunk in resp.iter_content(chunk_size=self._CHUNK_SIZE):
                fd.write(chunk)
        if self.verbosity >= 1:
            print(f'Download finished')
        return file_path

    def _process_file(self, file_path, order_number):
        file_url = os.path.relpath(file_path,p.FILE_WEB_ROOT)
        url = urljoin(p.HOST,file_url)
        outdir = os.path.join(self.temp_path,f'{order_number}')
        file_path = self._download_file(url,outdir,file_path)
        if self.verbosity >= 1:
            print('Unzipping')
        if file_path:
            file_list = self._extract_file(file_path,outdir)
            if self.verbosity >= 1:
                print("Extracted:")
                print([file.filename for file in file_list])

    def _validate(self,network, station, stations, starttime, endtime):
        # startttime < endtime
        if UTCDateTime(starttime) >= UTCDateTime(endtime):
            print('ERROR: starttime can not be larger than endtime')
            return False
        if len(stations) == 0:
            print(f'ERROR: no stations match the expression: network ~ {network}, station ~ {station}')
            return False
        
        return True

    def create_wf_request(self, stations=[], starttime=None, endtime=None, components=["Z","N","E"]):
        if not stations:
            print('Error: No stations given')
        if not starttime:
            print('No start time given')
        if not endtime:
            print('No end time given')
        if not (starttime and endtime and stations and components):
            print(f'Something missing: starttime {starttime}, endtime {endtime}')
            # print(f'Stations:')
            # print(stations)
            return False
        return WFRequest(
            stations = stations, 
            components = components,
            order_number='0',
            starttime=starttime,
            endtime=endtime,
            email=self._email,
            )

    def make_wf_request(self, wf_request):
        if not self.dry_run:
            order_number = self._get_order_number() # need a new one for each request
            time.sleep(1)
            wf_request.order_number = f'{order_number}'
        else:
            order_number = '1234'
        if not wf_request:
            print('Missing parameters')
            return False
        url = p.GET_WF_DATA_URL
        if not self.dry_run:
            for retry in range(self._max_retries):
                self.make_request(url, request_type='OPTIONS', headers=p.WF_HEADERS)
                resp = self.make_post_request(url, json=wf_request.data ,headers = p.WF_HEADERS)
                if not resp.status_code == 200:
                    print(f'WARNING: request failed with {resp.status_code}')
                    if self.verbosity >= 1:
                        print(f'response: {resp}')
                    wait_time = 2 ** retry * 0.5 + 0.1
                    print(f'Trying again after {wait_time}')
                    time.sleep(wait_time)
                    res = False
                else: 
                    res = resp.json()
        else:
            print('Dry Run: ', wf_request.data)
            res = False
        return res

    def _create_chunks(self,stations):
        # 10 day / single station
        # 1 day / multiple stations
        # 50 stations
        win_length = self.endtime - self.starttime
        self.queue = []
        if (len(stations) > 1 and len(stations) < 50 and win_length <= ONE_DAY) or \
            len(stations) == 1 and win_length <= ONE_DAY*10:
            # single request
            if self.verbosity >= 1:
                print(f'Chunker: Single Request station({len(stations)})')
            wf_request = self.create_wf_request(starttime=self.starttime, endtime=self.endtime,stations=stations)
            self.queue = [wf_request]
            return
        elif len(stations) > 1:
            # divide by ten day - one station windows
            if self.verbosity >= 1:
                print(f'Chunker: Multiple Requests for station({len(stations)})')
            for station in stations:
                chunk_starttime = self.starttime
                while chunk_starttime < self.endtime:
                    if chunk_starttime + TEN_DAYS >= self.endtime:
                        chunk_endtime = self.endtime
                    else:
                        chunk_endtime = chunk_starttime + TEN_DAYS
                    wf_request = self.create_wf_request(starttime=chunk_starttime, endtime=chunk_endtime,stations=[station])
                    if self.verbosity >= 1:
                        print('Chunker: request created:',wf_request.data)
                    self.queue.append(wf_request)
                    chunk_starttime += TEN_DAYS
        else:
            print('ERROR: Chunker: No stations selected')
            return

    def get_waveforms(self, network, station, starttime, endtime, quality=None, minimumlength=None, longestonly=None, filename=None, attach_response=False, **kwargs):
        self.starttime = UTCDateTime(starttime)
        self.endtime = UTCDateTime(endtime)
        if not self._email:
            self._generate_email()
        if not self.all_stations:
            self.get_stations()
        stations = self.match_stations(network, station, '*')
        if not self._validate(network, station, stations, starttime, endtime):
            print('ERROR: parameters not valid')
            return

        self._create_chunks(stations)
        if self.verbosity >= 1:
            print(f'Queue length: {len(self.queue)}')
        for wf_request in self.queue:
            if self.verbosity >= 1:
                print(f'Requesting waveform {wf_request.data}')
            res = self.make_wf_request(wf_request)
            time.sleep(1)
            if not res:
                print(f'WARNING: No response {res}')
                continue
            file_path = res['File_Path']
            if self.verbosity >= 1:
                print('res')
                print(res)
                print('file_path')
                print(file_path)
            if file_path:
                self._process_file(file_path,wf_request.order_number)
