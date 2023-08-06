class params:
    HOST = 'https://tdvms.afad.gov.tr'
    API = '/api/'
    GET_STATIONS_URL = 'api/Data/GetStations/'
    GET_NETWORKS_URL = 'api/Data/GetNetworks/'
    CHECK_HAS_REQUEST_URL = 'https://tdvms.afad.gov.tr/api/Data/HasARequestAlready/'
    GET_WF_DATA_URL = 'https://tdvmservis.afad.gov.tr/GetData'
    GET_ORDER_NUMBER_URL = 'api/Data/SendMailRequest/'

    FILE_WEB_ROOT = '/home/afad/web'

    STATION_KEYS = [
        "id",
        "code",
        "country",
        "longitude",
        "latitude",
        "place",
        "start",
        "end",
        "deviceN",
        "deviceNE",
        "deviceNN",
        "deviceNZ",
        "deviceH",
        "deviceHE",
        "deviceHN",
        "deviceHZ",
        "deviceL",
        "deviceLE",
        "deviceLN",
        "deviceLZ",
        "network",
        "isSelected",
    ]


    NETWORKS = [
        'GZ',
        'KO',
        'TB',
        'TK',
        'TU',
    ]

    GET_STATIONS_DEFAULT_DATA = {
        'component': '',
        'deviceCode': '',
        'netcodes': NETWORKS,
    }

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    ]

    EMAIL_PROVIDERS = [
        'gmail.com',
        'fastmail.com',
        'boun.edu.tr',
        'metu.edu.tr',
    ]

    HEADERS_DEFAULT = {
        'Host': 'tdvms.afad.gov.tr',
        'User-Agent': USER_AGENTS[0],
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://tdvms.afad.gov.tr/continuous_data',
        'Host': 'tdvms.afad.gov.tr',
        'Content-Type': 'application/json',
        # 'Content-Length': '50',
        'Origin': 'https://tdvms.afad.gov.tr',
    }

    WF_HEADERS = {
        'Host': 'tdvmservis.afad.gov.tr',
        'User-Agent': USER_AGENTS[0],
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type',
        'Referer': 'https://tdvms.afad.gov.tr/continuous_data',
        'Origin': 'https://tdvms.afad.gov.tr',
        'Connection': 'keep-alive',
    }