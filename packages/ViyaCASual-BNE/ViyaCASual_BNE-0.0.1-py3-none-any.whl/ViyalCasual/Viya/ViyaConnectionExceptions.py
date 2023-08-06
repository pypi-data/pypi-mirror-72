class ViyaConnectionError(Exception):
    pass


class ViyaConfigURL(ViyaConnectionError):
    def __init__(self):
        self.expression = 'You need to provide the URL for your Viya application'
        self.message = 'You need to provide the URL for your Viya application'


class ViyaConfigPort(ViyaConnectionError):
    def __init__(self):
        self.message = 'You need to provide the PORT for your Viya application'


class ViyaConfigUserName(ViyaConnectionError):
    def __init__(self):
        self.message = 'You need to provide the USERNAME for your Viya application'


class ViyaConfigPassword(ViyaConnectionError):
    def __init__(self):
        self.message = 'You need to provide the PASSWORD for your Viya application'


class ViyaSWATConnection(ViyaConnectionError):
    def __init__(self):
        self.message = 'Unable to connect to the sas viya server, please check the connections'


class ViyaSASCTLConnection(ViyaConnectionError):
    def __init__(self):
        self.message = 'Unable to connect to the sas viya server, please check the connections'
