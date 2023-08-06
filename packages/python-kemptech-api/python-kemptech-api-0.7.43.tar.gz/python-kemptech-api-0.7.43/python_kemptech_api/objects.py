import re
import logging
from collections import OrderedDict

from python_kemptech_api.api_xml import (
    get_data,
    is_successful,
    get_error_msg)
from python_kemptech_api.exceptions import (
    KempTechApiException,
    SubVsCannotCreateSubVs,
    RealServerMissingVirtualServiceInfo,
    RealServerMissingLoadmasterInfo,
    VirtualServiceACLMissingVirtualServiceInfo,
    LDAPMissingLoadMasterInfo,
    ValidationError,
    RuleMissingLoadmasterInfo,
    RangeMissingLoadmasterInfo,
    LoadMasterParameterError,
    SiteMissingFQDNInfo,
    SiteMissingLoadmasterInfo,
    ClusterMissingLoadmasterInfo,
    CertificateMissingLoadmasterInfo,
    CipherListInvalid,
    RangeMaskInvalid,
    VirtualServiceMissingLoadmasterInfo)
from python_kemptech_api.generic import BaseKempObject
from python_kemptech_api.utils import (
    validate_ip,
    validate_port,
    validate_protocol,
    get_sub_vs_list_from_data,
    send_response,
    cast_to_list,
    falsey_to_none, build_object)

log = logging.getLogger(__name__)


class VirtualService(BaseKempObject):
    _API_ADD = "/addvs"
    _API_MOD = "/modvs"
    _API_DELETE = "/delvs"
    _API_GET = "/showvs"
    _API_EXPORT = "/exportvstmplt"
    _API_LIST = "/listvs"
    API_TAG = "VS"
    API_INIT_PARAMS = {
        "vs": "VSAddress",
        "port": "VSPort",
        "prot": "Protocol"
    }
    _API_BASE_PARAMS = [
        "vs",
        "port",
        "prot"
    ]
    _API_DEFAULT_ATTRIBUTES = {
        "status": "Status",
        "index": "Index",
        "vs": "VSAddress",
        "altaddress": "AltAddress",
        "extraports": "ExtraPorts",
        "enable": "Enable",
        "vsaddress": "VSAddress",
        "vstype": "VStype",
        "mastervsid": "MasterVSID",
        "nickname": "NickName",

        # Scheduling and Persistence
        "schedule": "Schedule",
        "adaptive": "Adaptive",
        "persist": "Persist",
        "persisttimeout": "PersistTimeout",
        "querytag": "QueryTag",
        "cookie": "Cookie",

        # Advanced
        "standbyaddr": "StandbyAddr",
        "standbyport": "StandbyPort",
        "defaultgw": "DefaultGW",

        # HTTP
        "errorcode": "ErrorCode",
        "errorurl": "ErrorUrl",
        "errorpage": "ErrorPage",

        # Healthcheck
        "checktype": "CheckType",
        "checkport": "CheckPort",
        "checkurl": "CheckUrl",
        "checkheaders": "CheckHeaders",
        "checkuse1_1": "CheckUse1.1",
        "checkuseget": "CheckUseGet",
        "checkpostdata": "CheckPostData",
        "checkpattern": "CheckPattern",
        "checkcodes": "CheckCodes",
        "matchlen": "MatchLen",
        "enhancedhealthchecks": "EnhancedHealthChecks",
        "rsminimum": "RsMinimum",

        # L7
        "forcel7": "ForceL7",
        "transparent": "Transparent",
        "subnetoriginating": "SubnetOriginating",
        "useforsnat": "UseforSnat",
        "localbindaddrs": "LocalBindAddrs",
        "serverinit": "ServerInit",
        "idletime": "Idletime",
        "addvia": "AddVia",
        "extrahdrkey": "ExtraHdrKey",
        "extrahdrvalue": "ExtraHdrValue",
        "qos": "QoS",

        # Content Rules
        "rsruleprecedence": "RSRulePrecedence",
        "rsruleprecedencepos": "RSRulePrecedencePos",

        # SSL
        "sslacceleration": "SSLAcceleration",
        "sslrewrite": "SSLRewrite",
        "sslreverse": "SSLReverse",
        "sslreencrypt": "SSLReencrypt",
        "starttlsmode": "StartTLSMode",
        "tlstype": "TlsType",
        "cipherset": "CipherSet",
        "certfile": "CertFile",
        "clientcert": "ClientCert",
        "ocspverify": "OCSPVerify",
        "reversesnihostname": "ReverseSNIHostname",
        "needhostname": "NeedHostName",

        # AFE
        "multiconnect": "MultiConnect",
        "verify": "Verify",
        "compress": "Compress",
        "cache": "Cache",
        "cachepercent": "CachePercent",

        # WAF
        "alertthreshold": "AlertThreshold",
        "intercept": "Intercept",

        # ESP
        "espenabled": "EspEnabled",
        "allowedhosts": "AllowedHosts",
        "alloweddirectories": "AllowedDirectories",
        "domain": "Domain",
        "logoff": "Logoff",
        "addauthheader": "AddAuthHeader",
        "displaypubpriv": "DisplayPubPriv",
        "disablepasswordform": "DisablePasswordForm",
        "captcha": "Captcha",
        "captchapublickey": "CaptchaPublicKey",
        "captchaprivatekey": "CaptchaPublicKey",
        "captchaaccessurl": "CaptchaAccessUrl",
        "captchaverifyurl": "CaptchaVerifyUrl",
        "esplogs": "ESPLogs",
        "smtpalloweddomains": "SMTPAllowedDomains",
        "excludedirectories": "ExcludeDirectories",
        "inputauthmode": "InputAuthMode",
        "outputauthmode": "OutputAuthMode",
        "serverfbapath": "ServerFbaPath",
        "serverfbapost": "ServerFBAPost",
        "serverfbausernameonly": "ServerFbaUsernameOnly",
        "outconf": "OutConf",
        "singlesignondir": "SingleSignOnDir",
        "singlesignonmessage": "SingleSignOnMessage",
        "allowedgroups": "AllowedGroups",
        "groupsids": "GroupSIDs",
        "includenestedgroups": "IncludeNestedGroups",
        "steeringgroups": "SteeringGroups",
        "verifybearer": "VerifyBearer",
        "bearercertificatename": "BearerCertificateName",
        "bearertext": "BearerText",
        "excludeddomains": "BearerText",
        "altdomains": "AltDomains",
        "userpwdchangeurl": "UserPwdChangeURL",
        "userpwdchangemsg": "UserPwdChangeMsg",
        "userpwdexpirywarn": "UserPwdExpiryWarn",
        "userpwdexpirywarndays": "UserPwdExpiryWarnDays",
    }
    _ESP_PARAMS = [
        "espenabled"
    ]
    _WAF_PARAMS = [
        "alertthreshold",
        "intercept"
    ]
    _SSL_PARAMS = [
        "sslrewrite",
        "sslreverse",
        "sslreencrypt",
        "starttlsmode",
        "tlstype",
        "cipherset",
        "certfile",
        "clientcert",
        "ocspverify",
        "reversesnihostname",
        "needhostname",
    ]
    _AFE_PARAMS = [
        "verify",
        "compress",
        "cache",
        "cachepercent",
    ]

    def __init__(self, loadmaster_info, vs, port=80, prot="tcp",
                 is_sub_vs=False):
        """Construct VirtualService object.

        :param loadmaster_info: The loadmaster dict with the endpoint params.
        :param vs: IP or index of the VS. When creating a subvs you
               must pass the index and set the is_sub_vs flag to true in order
               for createsubvs to behave correctly. The index will be
               overwritten with the index of the newly created subvs on save().
        :param port: Port of the virtual service.
        :param prot: Protocol of the virtual service.
        :param is_sub_vs: Whether or not it is a subvs, mark this as true and
               pass the parent VS index as the ip_or_index parameter.
        """
        self.index = None  # to avoid AttributeErrors later
        self._is_sub_vs = is_sub_vs
        self.subvs_data = None
        self.subvs_entries = []
        self.real_servers = []
        self.sslrewrite = None
        self.certfile = None

        self._waf = False
        self._esp = False
        self._ssl = False
        self._afe = False

        if not is_sub_vs:
            # Skip validation when it is a subvs as they do not have ip/port
            self.vs = vs
            self.port = port
            self.prot = prot

            validate_ip(vs)
            validate_port(port)
            validate_protocol(prot)
        else:
            self.index = self.vs = vs

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise VirtualServiceMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise VirtualServiceMissingLoadmasterInfo("ip_address")

        super(VirtualService, self).__init__(loadmaster_info)
        self.cert = loadmaster_info.get("cert")

    def __str__(self):
        try:
            if int(self.vs):
                return 'Sub Virtual Service {} on LoadMaster {}'.format(
                    self.vs, self.ip_address)
        except ValueError:
            return 'Virtual Service {} {}:{} on LoadMaster {}'.format(
                self.prot.upper(), self.vs, self.port, self.ip_address)

    @property
    def servers(self):
        return {int(rs.rsindex): rs for rs in self.get_real_servers()}

    def to_api_dict(self):
        api = super(VirtualService, self).to_api_dict()

        def delete_non_existing_parameters(api_params, mode, params):
            if not mode:
                for entry in params:
                    try:
                        del api_params[entry]
                    except KeyError:
                        # If it doesn't exist don't do anything
                        pass
            return api_params

        api = delete_non_existing_parameters(api, self._waf, self._WAF_PARAMS)
        api = delete_non_existing_parameters(api, self._esp, self._ESP_PARAMS)
        api = delete_non_existing_parameters(api, self._ssl, self._SSL_PARAMS)
        api = delete_non_existing_parameters(api, self._afe, self._AFE_PARAMS)

        try:
            if self._is_sub_vs:
                del api['enable']
        except KeyError:
            pass

        return api

    def export(self):
        return self._get(self._API_EXPORT, self._get_base_parameters())

    def _get_base_parameters(self):
        """Returns the bare minimum VS parameters. IP, port and protocol"""
        if self.index is None:
            return {
                "vs": self.vs,
                "port": self.port,
                "prot": self.prot,
            }
        return {"vs": self.index}

    def _subvs_to_dict(self):
        return {
            "vs": self.subvs_data['parentvs'],
            "rs": "!{}".format(self.subvs_data['RsIndex']),
            "name": self.subvs_data['Name'],
            "forward": self.subvs_data['Forward'],
            "weight": self.subvs_data['Weight'],
            "limit": self.subvs_data['Limit'],
            "critical": self.subvs_data['Critical'],
            "enable": self.subvs_data['Enable']
        }

    @property
    def checkuse1_1(self):
        """This property exists because . can not be in a variable name.
        vs.checkuse1_1 is used for access to this variable, but internally the
        data is stored as obj.checkuse1.1 - this is because in order to write
        to the API, the parameter uses the string literal 'checkuse1.1' """
        return self.__dict__.get('checkuse1.1', None)

    @checkuse1_1.setter
    def checkuse1_1(self, value):
        """This property exists because . can not be in a variable name.
        vs.checkuse1_1 is used for access to this variable, but internally the
        data is stored as obj.checkuse1.1 - this is because in order to write
        to the API, the parameter uses the string literal 'checkuse1.1' """
        self.__dict__['checkuse1.1'] = value

    def save(self, update=False):
        # Parse certfile field if SSL acceleration is enabled
        if hasattr(self, "sslacceleration") and self.sslacceleration == "Y":
            if hasattr(self, "certfile"):
                if isinstance(self.certfile, list):
                    self.certfile = " ".join(self.certfile)
                if isinstance(self.certfile, str):
                    self.certfile = self.certfile.strip()
        else:
            self.certfile = None

        # Clear the persist timeout if persistence is not used
        if hasattr(self, "persist") and self.persist is None:
            # Setting persisttimeout=0 via the API
            # also clears the persist field on the service
            self.persist = ''
            self.persisttimeout = 0

        if self.subvs_entries:
            self.enhancedhealthchecks = None

        if not update:
            if self._is_sub_vs:
                # Hell, thy name be subvs
                response = self._get("/showvs", self._get_base_parameters())
                data = get_data(response)
                existing_subvs_entries = get_sub_vs_list_from_data(data)[0]
                params = self._get_base_parameters()
                params["createsubvs"] = ""
                response = self._get("/modvs", params)
                data = get_data(response)
                new_subvs_entries, subvs_data = get_sub_vs_list_from_data(data)
                s = set(existing_subvs_entries)
                # Subtracts the existing ID's from the new IDs to know what ID
                # to use when populating the self's attributes
                created_subvs_id = [x for x in new_subvs_entries
                                    if x not in s]
                newly_created_vs_params = {"vs": created_subvs_id}
                self.subvs_data = subvs_data[created_subvs_id[0]]
                self.subvs_data['parentvs'] = self.vs
                response = self._get("/showvs", newly_created_vs_params)
            else:
                response = self._get("/addvs", self.to_api_dict())
        else:  # Update
            if self._is_sub_vs:
                # Update the underlying "Rs" part of the subvs as well
                self._get("/modrs", self._subvs_to_dict())
            response = self._get("/modvs", self.to_api_dict())

        if is_successful(response):
            vs_data = get_data(response)
            self.populate_default_attributes(vs_data)
        else:
            raise KempTechApiException(get_error_msg(response))

    def create_sub_virtual_service(self):
        """VirtualService factory with pre-configured LoadMaster connection

        When creating a virtual service that is a sub virtual service you must
        pass the parent index to the constructor and mark the is_sub_vs flag
        as true. This will allow the save() method on the newly created subvs
        instance to be able to create a subvs against the parent vs. The index
        attribute will then be overwritten on save with the subvs's index.
        """
        if self._is_sub_vs:
            raise SubVsCannotCreateSubVs()
        return VirtualService(self.access_info, self.index, is_sub_vs=True)

    def create_real_server(self, ip, port=80):
        """RealServer factory with pre-configured LoadMaster connection."""
        return RealServer(self.access_info, ip, port)

    def create_access_control(self, addvs, addr):
        """AccessControl factory with pre-configured LoadMaster connection and
        ACL definition."""

        log.info("This method has been deprecated, please manipualte ACL "
                 "objects directly")

        acl = self.acl

        if addvs == "black":
            acl.blacklist[addr] = ""
        elif addvs == "white":
            acl.whitelist[addr] = ""
        else:
            log.warning("ACL List %s is not valid, ACLs have not been modified",
                        addvs)

        acl.update()

        return acl

    @property
    def acl(self):
        return self.get_vs_acl()

    def get_vs_acl(self):
        access_info = self.access_info
        access_info["ip"] = self.vs
        access_info["port"] = self.port
        access_info["prot"] = self.prot

        return VirtualServiceACL(self.access_info)

    def get_real_server(self, real_server_address=None, real_server_port=None):
        validate_port(real_server_port)

        if self.index is None:
            server_id = {
                "vs": self.vs,
                "port": self.port,
                "prot": self.prot,
                "rs": real_server_address,
                "rsport": real_server_port,
            }
        else:
            server_id = {
                "vs": self.index,
                "rs": real_server_address,
                "rsport": real_server_port,
            }
        response = self._get("/showrs", server_id)
        response_data = get_data(response)
        server = response_data.get("Rs", {})
        # if there is no Rs key, the following will fail with a ValidationError
        # which is the best we can do for now
        real_server = self.build_real_server(server)
        return real_server

    def get_real_servers(self):
        response = self._get("/showvs", self._get_base_parameters())
        data = get_data(response)
        real_servers = []
        servers = data.get('Rs', [])
        servers = cast_to_list(servers)
        for server in servers:
            real_server = self.build_real_server(server)
            real_servers.append(real_server)
        return real_servers

    def build_real_server(self, server):
        if "Addr" not in server:
            raise ValidationError('"Addr" key not present {}'.format(server))
        if "Port" not in server:
            raise ValidationError('"Port" key not present {}'.format(server))
        real_server = build_object(RealServer, self.access_info, server)
        return real_server

    def populate_default_attributes(self, params):
        """Populate VirtualService instance with standard defaults"""
        # pylint: disable=too-many-branches,too-many-statements
        #super(VirtualService, self).populate_default_attributes(dictionary)
        self.status = params.get('Status', None)
        self.index = params.get('Index', None)
        self.enable = params.get('Enable', None)
        self.forcel7 = params.get('ForceL7', None)
        self.vstype = params.get('VStype', None)
        self.schedule = params.get('Schedule', None)
        self.nickname = params.get('NickName', None)
        self.altaddress = params.get('AltAddress', None)
        self.transparent = params.get('Transparent', None)
        self.useforsnat = params.get('UseforSnat', None)
        self.persist = params.get('Persist', None)
        self.cookie = params.get('Cookie', None)
        self.extraports = params.get('ExtraPorts', None)
        self.qos = params.get('QoS', None)
        self.idletime = params.get('Idletime', None)
        self.mastervsid = params.get('MasterVSID', None)

        self.querytag = params.get('QueryTag', None)
        self.serverinit = params.get('ServerInit', None)
        self.addvia = params.get('AddVia', None)
        self.subnetoriginating = params.get('SubnetOriginating', None)
        self.localbindaddrs = params.get('LocalBindAddrs', None)
        self.defaultgw = params.get('DefaultGW', None)
        #self.followvsid = falsey_to_none(int(service.get('FollowVSID', 0)))
        self.standbyaddr = params.get('StandbyAddr', None)
        self.standbyport = params.get('StandbyPort', None)
        self.errorcode = params.get('ErrorCode', None)
        self.errorurl = params.get('ErrorUrl', None)
        self.errorpage = params.get('ErrorPage', None)

        # WAF
        self.alertthreshold = params.get('AlertThreshold', None)
        self.intercept = params.get('Intercept', None)
        # ESP
        self.espenabled = params.get('EspEnabled', None)
        self.espenabled = params.get("EspEnabled", None)
        self.allowedhosts = params.get("AllowedHosts", None)
        self.alloweddirectories = params.get("AllowedDirectories", None)
        self.domain = params.get("Domain", None)
        self.logoff = params.get("Logoff", None)
        self.addauthheader = params.get("AddAuthHeader", None)
        self.displaypubpriv = params.get("DisplayPubPriv", None)
        self.disablepasswordform = params.get("DisablePasswordForm", None)
        self.captcha = params.get("Captcha", None)
        self.captchapublickey = params.get("CaptchaPublicKey", None)
        self.captchaprivatekey = params.get("CaptchaPublicKey", None)
        self.captchaaccessurl = params.get("CaptchaAccessUrl", None)
        self.captchaverifyurl = params.get("CaptchaVerifyUrl", None)
        self.esplogs = params.get("ESPLogs", None)
        self.smtpalloweddomains = params.get("SMTPAllowedDomains", None)
        self.excludedirectories = params.get("ExcludeDirectories", None)
        self.inputauthmode = params.get("InputAuthMode", None)
        self.outputauthmode = params.get("OutputAuthMode", None)
        self.serverfbapath = params.get("ServerFbaPath", None)
        self.serverfbapost = params.get("ServerFBAPost", None)
        self.serverfbausernameonly = params.get("ServerFbaUsernameOnly", None)
        self.outconf = params.get("OutConf", None)
        self.singlesignondir = params.get("SingleSignOnDir", None)
        self.singlesignonmessage = params.get("SingleSignOnMessage", None)
        self.allowedgroups = params.get("AllowedGroups", None)
        self.groupsids = params.get("GroupSIDs", None)
        self.includenestedgroups = params.get("IncludeNestedGroups", None)
        self.steeringgroups = params.get("SteeringGroups", None)
        self.verifybearer = params.get("VerifyBearer", None)
        self.bearercertificatename = params.get("BearerCertificateName", None)
        self.bearertext = params.get("BearerText", None)
        self.excludeddomains = params.get("BearerText", None)
        self.altdomains = params.get("AltDomains", None)
        self.userpwdchangeurl = params.get("UserPwdChangeURL", None)
        self.userpwdchangemsg = params.get("UserPwdChangeMsg", None)
        self.userpwdexpirywarn = params.get("UserPwdExpiryWarn", None)
        self.userpwdexpirywarndays = params.get("UserPwdExpiryWarnDays", None)
        # Set meta values for whether WAF and ESP are enabled
        if self.alertthreshold is None or int(self.alertthreshold) == 0:
            self._waf = False
        else:
            self._waf = True

        if self.espenabled is None or self.espenabled == 'N':
            self._esp = False
        else:
            self._esp = True

        # AFE
        self.multiconnect = params.get('MultiConnect', None)
        self.verify = params.get('Verify', None)
        self.compress = params.get('Compress', None)
        self.cache = params.get('Cache', None)
        self.cachepercent = params.get('CachePercent', None)

        if self.verify is not None and int(self.verify) != 0:
            self._afe = True
        elif self.compress is not None and self.compress != 'N':
            self._afe = True
        elif self.cache is not None and self.cache != 'N':
            self._afe = True
        else:
            self._afe = False

        self.sslacceleration = params.get('SSLAcceleration', None)
        self.sslrewrite = params.get('SSLRewrite', None)
        self.sslreverse = params.get('SSLReverse', None)
        self.sslreencrypt = params.get('SSLReencrypt', None)
        self.starttlsmode = params.get('StartTLSMode', None)
        self.tlstype = params.get('TlsType', None)
        self.cipherset = params.get('CipherSet', None)
        self.certfile = params.get('CertFile', None)
        self.clientcert = params.get('ClientCert', None)
        self.ocspverify = params.get('OCSPVerify', None)
        self.reversesnihostname = params.get('ReverseSNIHostname', None)
        self.needhostname = params.get('NeedHostName', None)

        if self.sslacceleration is None or self.sslacceleration == 'N':
            self._ssl = False
        else:
            self._ssl = True

        # If SSL Acceleration is not enabled, clear the TLS type and Ciphers
        # These are not valid to set if Acceleration is off
        if not self._ssl:
            self.tlstype = None
            self.cipherset = None
            self.ciphers = None
            self.needhostname = None

        else:
            # Rewrite the SSL Rewrite value based on the table:
            # SSL Rewrite cannot be set as an integer, even
            # though it outputs as an integer
            sslrewrite = {
                "0": None,
                "1": "http",
                "2": "https"
            }

            try:
                # Try casting to an int in the case that the end user passes
                # the string version of the int.
                self.sslrewrite = sslrewrite[int(self.sslrewrite)]
            except (KeyError, TypeError):
                self.sslrewrite = None

            #
            if self.certfile is not None:
                log.info("Splitting certfile field into a list")
                self.certfile = str(self.certfile).split()
            else:
                self.certfile = []

            # If there's just one certificate, identified by a 32 character
            # hex string, it's a self signed certificate and the list should
            # be cleared since setting this value is invalid.
            if len(self.certfile) == 1:
                if re.match("[0-9a-f]{32}", self.certfile[0]) is not None:
                    self.certfile = []

        # Real servers section
        self.checktype = params.get('CheckType', None)
        self.checkhost = params.get('CheckHost', None)
        self.checkpattern = params.get('CheckPattern', None)
        self.checkurl = params.get('CheckUrl', None)
        self.checkcodes = params.get('CheckCodes', None)
        self.checkheaders = params.get('CheckHeaders', None)
        self.matchlen = params.get('MatchLen', None)
        self.checkuse1_1 = params.get('CheckUse1.1', None)
        self.checkport = falsey_to_none(int(params.get('CheckPort', 0)))
        self.checkuseget = params.get('CheckUseGet', None)
        self.extrahdrkey = params.get('ExtraHdrKey', None)
        self.extrahdrvalue = params.get('ExtraHdrValue', None)
        self.checkpostdata = params.get('CheckPostData', None)
        self.rsruleprecedence = params.get('RSRulePrecedence', None)
        self.rsruleprecedencepos = params.get('RSRulePrecedencePos', None)
        self.enhancedhealthchecks = params.get('EnhancedHealthChecks', None)

        # Handle non-standard behavior of Adaptive and Schedule parameters
        self.adaptive = params.get('Adaptive', None)
        if self.adaptive == 'http_rs':
            self.adaptive = None
            self.schedule = 'adaptive'
        elif self.adaptive == 'sdn_gstats':
            self.adaptive = None
            self.schedule = 'sdn-adaptive'

        # Disable enable argument if it's a SubVS
        if self.vs is None:
            self.enable = None

        self.persisttimeout = falsey_to_none(int(params.get(
            'PersistTimeout', 0)))

        self.rsminimum = falsey_to_none(int(params.get('RsMinimum', 0)))


class RealServer(BaseKempObject):
    _API_ADD = "/addrs"
    _API_MOD = "/modrs"
    _API_DELETE = "/delrs"
    _API_GET = "/showrs"
    _API_LIST = "/showvs"
    API_TAG = "Rs"
    API_INIT_PARAMS = {
        "ip": "Addr",
        "port": "Port"
    }
    _API_BASE_PARAMS = [
        "vs",
        "port",
        "prot",
        "rs",
        "rsport"
    ]
    _API_DEFAULT_ATTRIBUTES = {
        "addr": "Addr",
        "status": "Status",
        "rsindex": "RsIndex",
        "vsindex": "VsIndex",
        "enable": "Enable",
        "forward": "Forward",
        "weight": "Weight",
        "limit": "Limit",
        "critical": "Critical",
        "follow": "Follow",
        "dnsname": "DnsName"
    }

    @property
    def rs(self):
        if hasattr(self, "dnsname") and self.dnsname is not None:
            return self.dnsname
        return self.addr

    @rs.setter
    def rs(self, value):
        try:
            validate_ip(value)
        except ValidationError:
            self.dnsname = value
        else:
            self.addr = value

    def to_api_dict(self):
        # Populate RS field into dictionary manually
        as_dict = super(RealServer, self).to_api_dict()
        as_dict['rs'] = self.rs
        as_dict.pop('addr')
        return as_dict

    def __init__(self, loadmaster_virt_service_info, ip, port=80):
        self.rsindex = None
        self.rs = ip
        self.rsport = port
        validate_port(port)

        try:
            self.vs = loadmaster_virt_service_info["vs"]
        except KeyError:
            raise RealServerMissingVirtualServiceInfo("vs")

        self.port = loadmaster_virt_service_info.get("port", None)
        self.prot = loadmaster_virt_service_info.get("prot", None)

        try:
            self.endpoint = loadmaster_virt_service_info["endpoint"]
        except KeyError:
            raise RealServerMissingLoadmasterInfo("endpoint")

        try:
            self.ip_address = loadmaster_virt_service_info["ip_address"]
        except KeyError:
            raise RealServerMissingLoadmasterInfo("ip_address")

        super(RealServer, self).__init__(loadmaster_virt_service_info)
        self.cert = loadmaster_virt_service_info.get("cert")

    def __str__(self):
        return 'Real Server {} on {}'.format(self.rs, self.vs)

    def save(self, update=False):
        super(RealServer, self).save(update)
        # If a new port is set, update the assigned port value
        # in order to correctly look up the updated RS
        # If .save fails, this will never be performed
        if update and getattr(self, 'newport', None):
            self.rsport = self.newport
        self.refresh()


class LDAP(BaseKempObject):
    _API_ADD = "/addldapendpoint"
    _API_MOD = "/modifyldapendpoint"
    _API_DELETE = "/deleteldapendpoint"
    _API_GET = "/showldapendpoint"
    _API_LIST = "/showldaplist"
    API_TAG = "LDAP"
    API_INIT_PARAMS = {
        "ip": "Addr",
        "port": "Port"
    }
    _API_BASE_PARAMS = [
        "name"
    ]
    _API_DEFAULT_ATTRIBUTES = {
        "name": "name",
        "ldaptype": "ldaptype",
        "server": "server",
        "vinterval": "vinterval",
        "referralcount": "referralcount",
        "timeout": "timeout",
        "adminuser": "adminuser",
        "adminpass": "adminpass"
    }

    @property
    def ldap(self):
        return self.server

    def to_api_dict(self):
        # Populate RS field into dictionary manually
        as_dict = super(LDAP, self).to_api_dict()
        as_dict['LDAP'] = self.ldap
        return as_dict

    def __init__(self, loadmaster_info,  LDAP_obj):
        self.ldaptype = LDAP_obj.get('ldaptype', 0)
        self.server = LDAP_obj.get('server', None)
        self.vinterval = LDAP_obj.get('vinterval',60)
        self.referralcount = LDAP_obj.get('referralcount', None)
        self.timeout = LDAP_obj.get('timeout', 5)
        self.adminuser = LDAP_obj.get('adminuser', None)
        self.adminpass = LDAP_obj.get('adminpass', None)
        try:
            self.name = LDAP_obj['name']
        except KeyError:
            raise LDAPMissingLoadMasterInfo("name")
        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise LDAPMissingLoadMasterInfo("endpoint")

        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise LDAPMissingLoadMasterInfo("ip_address")

        super(LDAP, self).__init__(loadmaster_info)
        self.cert = loadmaster_info.get("cert")

    def __str__(self):
        return 'LDAP {}'.format(self.server)

    def save(self, update=False):
        super(LDAP, self).save(update)

    def get_ldap_endpoint(self, name=None):
        if name:
            response = self._get(self._API_GET, {'name': name})
        else:
            response = self._get(self._API_LIST)
        if is_successful(response):
            ldap_data = get_data(response)
            self.populate_default_attributes(ldap_data)


class BaseACLObject(BaseKempObject):
    _API = "/aclcontrol"
    _API_ADD = ""
    _API_DEL = ""
    _API_LIST = ""

    API_INIT_PARAMS = {
    }
    _API_BASE_PARAMS = [
    ]
    _API_DEFAULT_ATTRIBUTES = {
    }

    def __init__(self, loadmaster_info):
        # Attach to the LoadMaster

        self.appliance = loadmaster_info['appliance']
        self.blacklist = {}
        self.whitelist = {}

        super(BaseACLObject, self).__init__(loadmaster_info)

        self.refresh()

    def save(self, update=False):
        self._sync()
        self.refresh()

    def _sync(self):
        # Sync the blacklist and whitelist to the LoadMaster

        # Grab the new data and save it before refreshing to get the old data
        new_blacklist = self.blacklist
        new_whitelist = self.whitelist
        self.refresh()
        old_blacklist = self.blacklist
        old_whitelist = self.whitelist

        # Handle the blacklist changes
        for address, comment in old_blacklist.items():
            if address not in new_blacklist.keys():
                self._delete_entry('black', address)
            else:
                if new_blacklist[address] != comment:
                    self._delete_entry('black', address)
                    self._add_entry('black', address, new_blacklist[address])

        for address, comment in {key: value for key, value in new_blacklist.items()
                                 if key not in old_blacklist.keys()}.items():
            self._add_entry('black', address, comment)

        # Now handle the whitelist
        for address, comment in old_whitelist.items():
            if address not in new_whitelist.keys():
                self._delete_entry('white', address)
            else:
                if new_whitelist[address] != comment:
                    self._delete_entry('white', address)
                    self._add_entry('white', address, new_whitelist[address])

        for address, comment in {key: value for key, value in new_whitelist.items()
                                 if key not in old_whitelist.keys()}.items():
            self._add_entry('white', address, comment)

    def _add_entry(self, list_type, address, comment=None):
        parameters = self._get_base_parameters()

        parameters[self._API_ADD] = list_type
        parameters['addr'] = address

        # Only valid on 7.2.37.0 and higher
        if self.appliance['version'] >= "7.2.37.0":
            parameters['comment'] = comment

        response = self._get(  # pylint: disable=protected-access
            self._API,
            parameters)

        if not is_successful(response):
            raise KempTechApiException(get_error_msg(response))

    def _delete_entry(self, list_type, address):
        parameters = self._get_base_parameters()

        parameters[self._API_DEL] = list_type
        parameters['addr'] = address

        response = self._get(  # pylint: disable=protected-access
            self._API,
            parameters)

        if not is_successful(response):
            raise KempTechApiException(get_error_msg(response))

    def refresh(self):
        # First handle whitelist
        parameters = self._get_base_parameters()

        parameters[self._API_LIST] = "white"

        whitelist_response = self._get(  # pylint: disable=protected-access
            self._API,
            parameters)

        whitelist_data = get_data(whitelist_response)

        if isinstance(self, VirtualServiceACL):
            whitelist_xml = whitelist_data['VS']['Whitelist']
        else:
            whitelist_xml = whitelist_data['Whitelist']

        if whitelist_xml is None:
            self.whitelist = {}
        # Handle pre-7.2.37.0 cases
        elif "addr" in whitelist_xml.keys():
            self.whitelist = {
                address: "" for
                address in cast_to_list(whitelist_xml['addr'])
            }
        else:
            self.whitelist = {
                ip['addr']: ip['comment'] or ""
                for ip in cast_to_list(whitelist_xml['IP'])
            }

        # Next verse, same as the first!
        parameters = self._get_base_parameters()

        parameters[self._API_LIST] = "black"

        blacklist_response = self._get(  # pylint: disable=protected-access
            self._API,
            parameters)

        blacklist_data = get_data(blacklist_response)

        if isinstance(self, VirtualServiceACL):
            blacklist_xml = blacklist_data['VS']['Blacklist']
        else:
            blacklist_xml = blacklist_data['Blacklist']

        if blacklist_xml is None:
            self.blacklist = {}
        # Handle pre-7.2.37.0 cases
        elif "addr" in blacklist_xml.keys():
            self.blacklist = {
                address: ""
                for address in cast_to_list(blacklist_xml['addr'])
            }
        else:
            self.blacklist = {
                ip['addr']: ip['comment'] or ""
                for ip in cast_to_list(blacklist_xml['IP'])
            }


class GlobalACL(BaseACLObject):
    _API_ADD = "add"
    _API_DEL = "del"
    _API_LIST = "list"

    def __repr__(self):
        return 'Global ACL on {}'.format(self.appliance)


class VirtualServiceACL(BaseACLObject):
    _API_ADD = "addvs"
    _API_DEL = "delvs"
    _API_LIST = "listvs"

    _API_BASE_PARAMS = [
        "vsip",
        "vsport",
        "vsprot"
    ]

    def __init__(self, loadmaster_virt_service_info):
        try:
            self.vsip = loadmaster_virt_service_info["vs"]
        except KeyError:
            raise VirtualServiceACLMissingVirtualServiceInfo("vs")

        try:
            self.vsport = loadmaster_virt_service_info.get("port", None)
        except KeyError:
            raise VirtualServiceACLMissingVirtualServiceInfo("port")

        try:
            self.vsprot = loadmaster_virt_service_info.get("prot", None)
        except KeyError:
            raise VirtualServiceACLMissingVirtualServiceInfo("prot")

        super(VirtualServiceACL, self).__init__(loadmaster_virt_service_info)

    def __repr__(self):
        return 'Virtual Service ACL on {}/{}:{}'.format(
            self.vsprot,
            self.vsip,
            self.vsport)


class Template(BaseKempObject):
    _API_ADD = ""
    _API_MOD = ""
    _API_DELETE = "/deltemplate"
    _API_GET = "/listtemplates"
    _API_LIST = "/listtemplates"
    _API_APPLY = "/addvs"
    _API_UPLOAD = "/uploadtemplate"
    API_TAG = "template"
    API_INIT_PARAMS = {
        "name": "name"
    }
    _API_BASE_PARAMS = {
        "name": "name"
    }
    _API_DEFAULT_ATTRIBUTES = {
        "name": "name",
        "comment": "comment",
        "certified": "certified"
    }

    def __init__(self, loadmaster_info, name):
        self.name = name
        self.file = None

        super(Template, self).__init__(loadmaster_info)

    def save(self, update=False):
        raise KempTechApiException("Templates are read-only objects")


class Rule(BaseKempObject):
    _API_ADD = "/addrule"
    _API_MOD = "/modrule"
    _API_DELETE = "/delrule"
    _API_GET = "/showrule"
    _API_LIST = "/showrule"
    API_INIT_PARAMS = {
        "name": "Name",
        "pattern": "Pattern"
    }
    _API_BASE_PARAMS = {
        "name": "Name",
        "type": "Type",
        "pattern": "Pattern"
    }
    _API_DEFAULT_ATTRIBUTES = {
        "name": "Name",
        "type": "Type",
        "pattern": "Pattern",
        "matchtype": "MatchType",
        "addhost": "AddHost",
        "negate": "Negate",
        "caseindependant": "CaseIndependent",
        "includequery": "IncludeQuery",
        "header": "Header",
        "mustfail": "MustFail",
        "headervalue": "HeaderValue",
        "replacement": "Replacement",
        "setflagonmatch": "SetFlagOnMatch",
        "onlyonflag": "OnlyOnFlag"
    }

    @property
    def type_string(self):
        types = {
            "0": "MatchContentRule",
            "1": "AddHeaderRule",
            "2": "DeleteHeaderRule",
            "3": "ReplaceHeaderRule",
            "4": "ModifyURLRule"
        }

        if self.type is None:
            return None
        return types[str(self.type)]

    @type_string.setter
    def type_string(self, value):
        types = {
            "MatchContentRule": "0",
            "AddHeaderRule": "1",
            "DeleteHeaderRule": "2",
            "ReplaceHeaderRule": "3",
            "ModifyURLRule": "4"
        }

        if value is None:
            self.type = None
        else:
            self.type = types[value]

    def __init__(self, loadmaster_info, name, pattern):
        self.populate_default_attributes({})
        self.name = name
        self.pattern = pattern
        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise RuleMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise RuleMissingLoadmasterInfo("ip_address")
        super(Rule, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Rule {} on LoadMaster {}'.format(
            self.name, self.ip_address)

    def _get_base_parameters(self):
        base_parameters = super(Rule, self)._get_base_parameters()

        # Pattern is not necessary for AddHeader rules
        if self.type == 1:
            base_parameters.pop("pattern")

        return base_parameters

    def populate_default_attributes(self, params):
        """Populate object instance with standard defaults"""
        # Get data from inside tag
        # Tag is unknown since different rule types have
        # different tag names. The generic code using API_TAG
        # isn't usable in this case.
        #params = params.popitem()[1]

        for attribute, tag in self._API_DEFAULT_ATTRIBUTES.items():
            setattr(self, attribute, params.get(tag, None))

        self.type_string = self.type


class Sso(BaseKempObject):
    def __init__(self, loadmaster_info, name):
        self.name = name

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise RangeMissingLoadmasterInfo("endpoint")
        super(Sso, self).__init__(loadmaster_info)

    def __str__(self):
        return 'SSO {} on LoadMaster {}'.format(
            self.name, self.ip_address)

    def _get_base_parameters(self):
        """Returns the bare minimum FQDN parameters."""
        return {
            "domain": self.name
        }

    def save(self, update=False):
        if not update:
            response = self._get("/adddomain", self._get_base_parameters())

            if not is_successful(response):
                raise KempTechApiException(get_error_msg(response))

        response = self._get("/moddomain", self.to_api_dict())

        if is_successful(response):
            sso_data = get_data(response)
            self.populate_default_attributes(sso_data)
        else:
            raise KempTechApiException(get_error_msg(response))

    def delete(self):
        response = self._get("/deldomain", self._get_base_parameters())
        return send_response(response)

    def populate_default_attributes(self, params):
        """Populate SSO instance with standard defaults"""
        self.id = params.get('Id', None)
        self.name = params.get('Name', None)
        self.auth_type = params.get('auth_type', None)
        self.ldap_endpoint = params.get('ldap_endpoint', None)
        self.radius_shared_secrret = params.get('radius_shared_secrret', None)
        self.radius_send_nas_id = params.get('radius_send_nas_id', None)
        self.logon_fmt = params.get('logon_fmt', None)
        self.logon_fmt2 = params.get('logon_fmt2', None)
        self.logon_domain = params.get('logon_domain', None)
        self.logon_transcode = params.get('logon_transcode', None)
        self.max_failed_auths = params.get('max_failed_auths', None)
        self.sess_tout_idle_pub = params.get('sess_tout_idle_pub', None)
        self.sess_tout_duration_pub = params.get('sess_tout_duration_pub', None)
        self.sess_tout_idle_priv = params.get('sess_tout_idle_priv', None)
        self.sess_tout_type = params.get('sess_tout_type', None)
        self.testuser = params.get('testuser', None)
        self.testpass = params.get('testpass', None)
        self.reset_fail_tout = params.get('reset_fail_tout', None)
        self.unblock_tout = params.get('unblock_tout', None)
        self.server = params.get('server', None)
        self.server2 = params.get('server2', None)
        self.kerberos_domain = params.get('kerberos_domain', None)
        self.kerberos_kdc = params.get('kerberos_kdc', None)
        self.kcd_username = params.get('kcd_username', None)
        self.kcd_password = params.get('kcd_password', None)
        self.ldap_admin = params.get('ldap_admin', None)
        self.ldap_password = params.get('ldap_password', None)
        self.cert_check_asi = params.get('cert_check_asi', None)
        self.cert_check_cn = params.get('cert_check_cn', None)
        self.server_side = params.get('server_side', None)
        self.idp_entity_id = params.get('idp_entity_id', None)
        self.idp_sso_url = params.get('idp_sso_url', None)
        self.idp_logoff_url = params.get('Idp_logoff_url', None)
        self.idp_cert = params.get('idp_cert', None)
        self.idp_match_cert = params.get('idp_match_cert', None)
        self.sp_entity_id = params.get('sp_entity_id', None)
        self.sp_cert = params.get('sp_cert', None)
        self.ldapephc = params.get('ldapephc', None)
        self.ldap_version = params.get('ldap_version', None)
        self.sess_tout_duration_priv = params.get('sess_tout_duration_priv', None)



class Fqdn(BaseKempObject):
    _API_ADD = "/addfqdn"
    _API_MOD = "/modfqdn"
    _API_DELETE = "/delfqdn"
    _API_GET = "/showfqdn"
    _API_LIST = "/listfqdns"
    API_TAG = "fqdn"
    API_INIT_PARAMS = {
        "fqdn": "FullyQualifiedDomainName"
    }
    _API_BASE_PARAMS = [
        "fqdn"
    ]
    _API_DEFAULT_ATTRIBUTES = {
        "fqdn": "FullyQualifiedDomainName",
        "status": "Status",
        "selectioncriteria": "SelectionCriteria",
        "failtime": "FailTime",
        "siterecoverymode": "SiteRecoveryMode",
        "failover": "failover",
        "publicrequestvalue": "publicRequestValue",
        "privaterequestvalue": "privateRequestValue",
        "localsettings": "LocalSettings",
        "localttl": "LocalTTL",
        "localsticky": "LocalSticky",
        "unanimouschecks": "UnanimousChecks"
    }

    def __init__(self, loadmaster_info, fqdn):
        self.fqdn = fqdn  # to avoid AttributeErrors later

        super(Fqdn, self).__init__(loadmaster_info)

    def __str__(self):
        return 'FQDN {} on LoadMaster {}'.format(
            self.fqdn, self.ip_address)

    def save(self, update=False):
        try:
            if self.selectioncriteria != "lb":
                # Failover is not available when not using Location Based
                del self.failover
        except AttributeError:
            pass

        super(Fqdn, self).save(update)
        self.refresh()

    def populate_default_attributes(self, params):
        super(Fqdn, self).populate_default_attributes(params)

        # Failtime is set by minute, but recorded by second
        try:
            # Try to cast to integer first
            self.failtime = int(self.failtime)
            # Check if failtime is a non-zero factor of 60
            if self.failtime > 0 and self.failtime % 60 == 0:
                # Convert from seconds to minutes
                self.failtime = int(self.failtime / 60)
        except (TypeError, AttributeError):
            self.failtime = None

    @property
    def sites(self):
        return {site.ipaddress: site for site in self.get_sites()}

    def create_site(self, ip):
        """Site factory with pre-configured LoadMaster connection."""
        return Site(self.access_info, ip)

    def get_site(self, ip):
        validate_ip(ip)

        service_id = {
            "fqdn": self.fqdn,
            "ipaddress": ip
        }

        response = self._get("/showfqdn", service_id)
        xml_object = get_data(response)

        maps = xml_object["fqdn"].get(Site.API_TAG, {})
        if not isinstance(maps, list):
            maps = [maps]

        map = [m for m in maps if m['IPAddress'] == service_id["ipaddress"]]

        # This shouldn't happen, but we should catch it anyway
        if len(map) != 1:
            raise LoadMasterParameterError(
                "Unexpected number of matching sites specified.", map)

        return build_object(Site, self.access_info, map[0])

    def get_sites(self):
        fqdn = {
            "fqdn": self.fqdn
        }

        try:
            response = self._get(self._API_LIST, fqdn)
            data = get_data(response)
            xml_object = data[self.API_TAG].get(Site.API_TAG, [])
        except KempTechApiException:
            xml_object = []

        obj_list = []

        # If there is no API_TAG key, build will fail with a
        # ValidationError, which is the best we can do for now
        # (without changing the upstream code and raising an
        # exception earlier, possibly retrying)

        xml_object = cast_to_list(xml_object)

        for x in xml_object:
            obj = self.build_site(x)
            obj_list.append(obj)
        return obj_list

    def build_site(self, site):
        """Create a object instance with standard defaults"""
        build_parameters = {}

        for parameter, tag in Site.API_INIT_PARAMS.items():
            build_parameters[parameter] = site.get(tag)

        obj = Site(self.access_info, **build_parameters)
        obj.populate_default_attributes(site)
        return obj


class Site(BaseKempObject):
    _API_ADD = "/addmap"
    _API_MOD = "/modmap"
    _API_DELETE = "/delmap"
    _API_GET = "/showfqdn"
    _API_LIST = "/showfqdn"
    API_TAG = "Map"
    API_INIT_PARAMS = {
        "ip": "IPAddress"
    }
    _API_BASE_PARAMS = {
        "fqdn": "fqdn",
        "ip": "ip"
    }
    _API_DEFAULT_ATTRIBUTES = {
        "index": "Index",
        "status": "Status",
        "clustervsaddress": "ClusterVSAddress",
        "checker": "Checker",
        "checkeraddr": "checkerAddr",
        "checkerport": "CheckerPort",
        "weight": "Weight",
        "enable": "Enable",
        "locationlatitude": "LocationLatitude",
        "locationlongitude": "LocationLongitude",
        "continent": "continent",
        "country": "country",
        "customlocation": "customLocation",
        "cluster": "Cluster",
        "mapaddress": "MappedAddress",
        "mapport": "MappedPort"
    }
    _API_IGNORE = (
        "log_urls", "ip_address", "endpoint", "index", "status",
        "continent", "country", "customlocation", "ipaddress"
    )

    # Remap ipaddress to ip because the API is inconsistent
    @property
    def ipaddress(self):
        return self.ip

    @ipaddress.setter
    def ipaddress(self, value):
        self.ip = value

    @property
    def mappedaddress(self):
        return self.mapaddress

    @mappedaddress.setter
    def mappedaddress(self, value):
        self.mapaddress = value

    @property
    def mappedport(self):
        return self.mapport

    @mappedport.setter
    def mappedport(self, value):
        self.mapport = value

    def __init__(self, loadmaster_fqdn_info, ip):
        self.fqdn = loadmaster_fqdn_info["fqdn"]
        self.ip = ip
        validate_ip(ip)

        try:
            self.fqdn = loadmaster_fqdn_info["fqdn"]
        except KeyError:
            raise SiteMissingFQDNInfo("fqdn")

        try:
            self.endpoint = loadmaster_fqdn_info["endpoint"]
        except KeyError:
            raise SiteMissingLoadmasterInfo("endpoint")

        try:
            self.ip_address = loadmaster_fqdn_info["ip_address"]
        except KeyError:
            raise SiteMissingLoadmasterInfo("ip_address")

        super(Site, self).__init__(loadmaster_fqdn_info)

    def __str__(self):
        return 'Site {} in FQDN {} on LoadMaster {}'.format(
            self.ip, self.fqdn, self.ip_address)

    def _get_base_parameters(self):
        return {
            "fqdn": self.fqdn,
            "ip": self.ip
        }

    def populate_default_attributes(self, params):
        super(Site, self).populate_default_attributes(params)

        # Fix annoying API inconsistencies

        # Normalize location lists so we always get a regular list
        if not isinstance(self.continent, list):
            if self.continent is None:
                self.continent = []
            else:
                self.continent = [self.continent]

        if not isinstance(self.country, list):
            if self.country is None:
                self.country = []
            else:
                self.country = [self.country]

        if not isinstance(self.customlocation, list):
            if self.customlocation is None:
                self.customlocation = []
            else:
                self.customlocation = [self.customlocation]

        try:
            self.checkerport = int(self.checkerport)
        except (ValueError, AttributeError):
            self.checkerport = None
        finally:
            if not 1 < self.checkerport < 65530:
                self.checkerport = None

    def save(self, update=False):
        if not update:
            response = self._get(self._API_ADD, self._get_base_parameters())
        else:
            response = self._get(self._API_MOD, self.to_api_dict())

        if not is_successful(response):
            raise KempTechApiException(get_error_msg(response))

        # Secondary request is needed because the add/mod action
        # does not return any data. Therefore, we need to explicitly
        # retrieve the info.
        response = self._get(self._API_GET, self._get_base_parameters())

        if is_successful(response):
            response = self._get(self._API_GET, self._get_base_parameters())
            data = get_data(response)
            maps = data["fqdn"].get(self.API_TAG, {})

            if not isinstance(maps, list):
                maps = [maps]

            map = [m for m in maps if m['IPAddress'] == self.ipaddress]

            # This shouldn't happen, but we should catch it anyway
            if len(map) > 1:
                raise LoadMasterParameterError(
                    "Multiple matching sites specified.",
                    map)
            if len(map) < 1:
                raise LoadMasterParameterError(
                    "No matching sites specified.",
                    map)

            site = map[0]
            self.populate_default_attributes(site)
        else:
            raise KempTechApiException(get_error_msg(response))

    def refresh(self):
        response = self._get(
            self._API_GET,
            self._get_base_parameters())
        if is_successful(response):
            response = self._get(self._API_GET, self._get_base_parameters())
            data = get_data(response)
            maps = data["fqdn"].get(self.API_TAG, {})

            if not isinstance(maps, list):
                maps = [maps]

            map = [m for m in maps if m['IPAddress'] == self.ipaddress]

            # This shouldn't happen, but we should catch it anyway
            if len(map) > 1:
                raise LoadMasterParameterError(
                    "Multiple matching sites specified.",
                    map)
            if len(map) < 1:
                raise LoadMasterParameterError(
                    "No matching sites specified.",
                    map)

            site = map[0]
            self.populate_default_attributes(site)
        else:
            raise KempTechApiException(get_error_msg(response))

    @property
    def locations(self):
        return {
            "continent": self.continent,
            "country": self.country,
            "customlocation": self.customlocation
        }

    @staticmethod
    def __get_map_parameters(location, is_continent=False, is_custom=False):
        if is_custom is False:
            parameters = {
                "countrycode": location.upper()
            }

            if is_continent is True:
                parameters["iscontinent"] = "yes"
            else:
                parameters["iscontinent"] = "no"
        else:
            parameters = {
                "customlocation": location
            }

        return parameters

    def __mod_location(self, location, is_continent=False, is_custom=False,
                       remove=False):
        parameters = self.__get_map_parameters(location,
                                               is_continent,
                                               is_custom)
        parameters.update(self._get_base_parameters())

        if not remove:
            url = "/addcountry"
        else:
            url = "/removecountry"

        response = self._get(url, parameters)
        if is_successful(response):
            self.refresh()
        else:
            raise KempTechApiException(get_error_msg(response))

    def set_locations(self, locations):

        # Remove all existing locations
        for location in self.continent or []:
            self.remove_location(location['code'], True, False)

        for location in self.country or []:
            self.remove_location(location['code'], False, False)

        for location in self.customlocation or []:
            self.remove_location(location['name'], False, True)

        # Add new set of locations
        for location in locations.get("continent", []):
            self.add_location(location['code'], True, False)

        for location in locations.get("country", []):
            self.add_location(location['code'], False, False)

        for location in locations.get("customlocation", []):
            self.add_location(location['name'], False, True)

        self.refresh()

    def add_location(self, location=None, is_continent=False, is_custom=False):
        self.__mod_location(location,
                            is_continent,
                            is_custom,
                            remove=False)

    def remove_location(self, location, is_continent=False, is_custom=False):
        self.__mod_location(location,
                            is_continent,
                            is_custom,
                            remove=True)

    def set_coordinates(self, latitude=None, longitude=None):
        latitude = latitude or self.locationlatitude
        longitude = longitude or self.locationlongitude

        parameters = {
            "lat": latitude,
            "long": longitude
        }

        parameters.update(self._get_base_parameters())

        url = "/changemaploc"

        response = self._get(url, parameters)
        if is_successful(response):
            self.refresh()
        else:
            raise KempTechApiException(get_error_msg(response))


class Cluster(BaseKempObject):
    _API_ADD = "/addcluster"
    _API_MOD = "/modcluster"
    _API_DELETE = "/delcluster"
    _API_GET = "/showcluster"
    _API_LIST = "/listclusters"
    API_TAG = "cluster"
    API_INIT_PARAMS = {
        "ip": "IPAddress",
        "name": "Name"
    }
    _API_BASE_PARAMS = {
        "ip": "IPAddress",
        "name": "Name"
    }
    _API_DEFAULT_ATTRIBUTES = {
        "status": "Status",
        "id": "Index",
        "name": "Name",
        "checker": "Checker",
        "checkerport": "CheckerPort",
        "type": "Type",
        "enable": "Enable",
        "locationlatitude": "LocationLatitude",
        "locationlongitude": "LocationLongitude",
        "clustervsaddress": "ClusterVSAddress"
    }

    def __init__(self, loadmaster_info, ip, name):
        self.id = None
        self.name = name
        self.ip = ip
        validate_ip(ip)

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise ClusterMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise ClusterMissingLoadmasterInfo("ip_address")
        super(Cluster, self).__init__(loadmaster_info)

    def __str__(self):
        if self.id is None:
            return 'Cluster {} at {} on LoadMaster {}'.format(
                self.name, self.ip, self.ip_address)
        return 'Cluster #{} {} at {} on LoadMaster {}'.format(
            self.id, self.name, self.ip, self.ip_address)

    def save(self, update=False):
        super(Cluster, self).save(update)
        self.refresh()

    def populate_default_attributes(self, params):
        super(Cluster, self).populate_default_attributes(params)

        # Clear checkerport if it's not in use
        if hasattr(self, "checkerport") and self.checkerport == "0":
            if self.checker != "tcp":
                self.checkerport = None
            else:
                # PD-7338
                self.checkerport = "80"


class Range(BaseKempObject):
    _API_ADD = "/addip"
    _API_MOD_LOC = "/modiploc"
    _API_DEL_LOC = "/deliploc"
    _API_ADD_CC = "/addipcountry"
    _API_DEL_CC = "/removeipcountry"
    _API_DELETE = "/delip"
    _API_GET = "/showip"
    _API_LIST = "/listips"
    API_TAG = "IPAddress"
    API_INIT_PARAMS = {
        "ip": "IPAddress",
        "mask": "Mask"
    }
    _API_BASE_PARAMS = [
        "ip",
        "mask"
    ]
    _API_DEFAULT_ATTRIBUTES = {
        "status": "Status",
        "index": "Index",
        "country": "Country",
        "iscustom": "IsCustom",
        "long": "Longitude",
        "lat": "Latitude"
    }
    _API_IGNORE = (
        "log_urls", "ip_address", "endpoint", "index", "status", "country",
        "iscustom", "mask",
    )

    def __init__(self, loadmaster_info, ip, mask):
        self.ip = ip
        validate_ip(self.ip)

        self.mask = int(mask)
        if not 8 <= self.mask <= 32:
            raise RangeMaskInvalid(mask)

        self.lat = None
        self.long = None
        self.country = None
        self.iscustom = None

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise RangeMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise RangeMissingLoadmasterInfo("ip_address")
        super(Range, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Range {}/{} on LoadMaster {}'.format(
            self.ip, self.mask, self.ip_address)

    @property
    def latitude(self):
        if self.lat is not None:
            return self.lat / 3600
        return None

    @latitude.setter
    def latitude(self, value):
        self.lat = value * 3600

    @property
    def longitude(self):
        if self.lat is not None:
            return self.long / 3600
        return None

    @longitude.setter
    def longitude(self, value):
        self.long = value * 3600

    def _get_base_parameters(self):
        """Returns the bare minimum FQDN parameters."""
        return {
            "ip": self.ip
        }

    def save(self, update=False):
        if not update:
            base_parameters = {
                "ip": self.ip + "/" + str(self.mask)
            }

            response = self._get(self._API_ADD, base_parameters)

            if not is_successful(response):
                raise KempTechApiException(get_error_msg(response))

            # We need to refresh here, creating the range does not return data
            self.refresh()

        # Set Coordinates
        if self.lat is not None and self.long is not None:
            response = self._get(self._API_MOD_LOC,
                                 self.to_api_dict())
        else:
            response = self._get(self._API_DEL_LOC,
                                 self._get_base_parameters())

        if is_successful(response):
            pass
        else:
            raise KempTechApiException(get_error_msg(response))

        # Set Country
        if self.iscustom is True:
            key = "customloc"
        else:
            key = "countrycode"

        parameters = {
            key: self.country
        }

        if self.country is not None:
            parameters.update(self._get_base_parameters())
            response = self._get(self._API_ADD_CC, parameters)
        else:
            response = self._get(self._API_DEL_CC, self._get_base_parameters())

        if is_successful(response):
            range_data = get_data(response)
            self.populate_default_attributes(range_data)
        else:
            raise KempTechApiException(get_error_msg(response))

    def populate_default_attributes(self, params):
        super(Range, self).populate_default_attributes(params)

        if self.country == "-1":
            self.country = None

        if self.lat is not None:
            self.lat = int(self.lat)

        if self.long is not None:
            self.long = int(self.long)


class CustomLocation(BaseKempObject):
    def __init__(self, loadmaster_info, name):
        self.name = name
        self.old_name = name

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise RangeMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise RangeMissingLoadmasterInfo("ip_address")
        super(CustomLocation, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Custom Location {} on LoadMaster {}'.format(
            self.name, self.ip_address)

    def _get_base_parameters(self):
        """Returns the bare minimum FQDN parameters."""
        return {
            "clname": self.name,
            "location": self.name
        }

    def save(self, update=False):
        if not update:
            response = self._get("/addcustomlocation",
                                 self._get_base_parameters())

            if not is_successful(response):
                raise KempTechApiException(get_error_msg(response))
        else:
            parameters = {
                "cloldname": self.old_name,
                "clnewname": self.name
            }

            response = self._get("/editcustomlocation", parameters)

            if is_successful(response):
                # range_data = get_data(response)
                self.old_name = self.name
                # Unfinished. Need to implement populate_attributes
            else:
                raise KempTechApiException(get_error_msg(response))

    def delete(self):
        response = self._get("/deletecustomlocation",
                             self._get_base_parameters())
        return send_response(response)


class CipherSet(BaseKempObject):
    def __init__(self, loadmaster_info, cipherset_name, ciphers):
        self.cipherset_name = cipherset_name
        cipher_regex = re.compile("^([A-Z0-9-]*:*)*[^:]$")
        if isinstance(ciphers, list):
            self.ciphers = ":".join(ciphers)
        elif isinstance(ciphers, str) and cipher_regex.match(ciphers):
            self.ciphers = ciphers
        else:
            raise CipherListInvalid(ciphers)

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("endpoint")

        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("ip_address")

        super(CipherSet, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Cipher List {}'.format(self.ciphers)

    def _get_base_parameters(self):
        """Returns the bare minimum cipherset parameters"""
        return {
            "name": self.cipherset_name,
            "value": self.ciphers
        }

    def save(self, update=False):
        response = self._get('/modifycipherset',
                             parameters=self._get_base_parameters())
        if is_successful(response):
            pass
        else:
            raise KempTechApiException(get_error_msg(response))

    def delete(self):
        response = self._get("/delcipherset", self._get_base_parameters())
        return send_response(response)


class Certificate(BaseKempObject):
    def __init__(self, loadmaster_info, certname,
                 certfile=None, certpass=None):
        self.certname = certname

        # If certname is a structure, pull out the name and set the modulus
        if isinstance(self.certname, dict):
            self.modulus = self.certname['modulus']
            self.certname = self.certname['name']

        if certfile is not None:
            self.certfile = certfile

        if certpass is not None:
            self.certpass = certpass
        else:
            self.certpass = None

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("endpoint")

        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("ip_address")

        super(Certificate, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Certificate {}'.format(self.certname)

    def _get_base_parameters(self):
        """Returns the bare minimum VS parameters. IP, port and protocol"""

        if self.certpass is None:
            return {
                "cert": self.certname,
                "replace": "0"
            }
        return {
            "cert": self.certname,
            "replace": "0",
            "password": self.certpass
        }

    def save(self, update=False):
        response = self._post("/addcert", file=self.certfile,
                              parameters=self._get_base_parameters())

        if is_successful(response):
            pass
        else:
            raise KempTechApiException(get_error_msg(response))

    def delete(self):
        response = self._get("/delcert",
                             self._get_base_parameters())

        return send_response(response)

    def populate_default_attributes(self, params):
        super(Certificate, self).populate_default_attributes(params)

        # If certname is a structure, pull out the name and set the modulus
        if isinstance(self.certname, dict):
            self.modulus = self.certname['modulus']
            self.certname = self.certname['name']


class IntermediateCertificate(BaseKempObject):
    def __init__(self, loadmaster_info, certname, certfile=None):
        self.certname = certname

        # If certname is a structure, pull out the name and set the modulus
        if isinstance(self.certname, dict):
            self.modulus = self.certname['modulus']
            self.certname = self.certname['name']

        if certfile is not None:
            self.certfile = certfile

        try:
            self.endpoint = loadmaster_info["endpoint"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("endpoint")
        try:
            self.ip_address = loadmaster_info["ip_address"]
        except KeyError:
            raise CertificateMissingLoadmasterInfo("ip_address")

        super(IntermediateCertificate, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Intermediate Certificate {}'.format(self.certname)

    def _get_base_parameters(self):
        """Returns the bare minimum VS parameters. IP, port and protocol"""
        return {
            "cert": self.certname,
        }

    def save(self, update=False):
        response = self._post("/addintermediate",
                              file=self.certfile,
                              parameters=self._get_base_parameters())

        if is_successful(response):
            pass
        else:
            raise KempTechApiException(get_error_msg(response))

    def delete(self):
        response = self._get("/delintermediate", self._get_base_parameters())
        return send_response(response)


class Interface(BaseKempObject):
    _API_MOD = "/modiface"
    _API_GET = "/showiface"
    _API_LIST = "/stats"
    _API_ADD_ADDRESS = "/addadditional"
    _API_DELETE_ADDRESS = "/deladditional"
    API_TAG = "Interface"
    _API_LIST_TAG = "Network"
    API_INIT_PARAMS = {
        "interface": "Id"
    }
    _API_BASE_PARAMS = {
        "interface": "Id"
    }
    _API_DEFAULT_ATTRIBUTES = {
        "interface": "Id",
        "addr": "IPAddress",
        "shared": "SharedIPAddress",
        "partner": "PartnerIPAddress",
        "hacheck": "hacheck",
        "mtu": "Mtu",
        "interfacetype": "InterfaceType",
        "geotraffic": "GeoTrafficEnable",
        "gwiface": "DefaultInterface",
        "additionaladdresses": "AdditionalAddresses",
        "adminwuienable": "AdminWuiEnable"
    }
    _API_IGNORE = (
        "log_urls", "ip_address", "endpoint", "name"
        "interfacetype", "additionaladdresses"
    )

    def __init__(self, loadmaster_info, interface, params=None):
        """ Interface constructor

        :param loadmaster_info: LoadMaster access_info
        :param interface: LoadMaster interface ID.
        """
        self.interface = interface
        # Set addr and cidr to empty strings to allow the properties
        # to work correctly when there are no IPs or CIDR set.
        self.addr = ""
        self.cidr = ""
        self.shared = None
        self.partner = None
        self.populate_default_attributes(params)
        super(Interface, self).__init__(loadmaster_info)

    def __str__(self):
        return 'Interface {} on LoadMaster {}'.format(
            self.interface, self.ip_address)

    @property
    def address(self):
        # self.addr can be None as it is not mandatory for an interface to have an address
        return self.addr.split("/")[0] if self.addr is not None else None

    @address.setter
    def address(self, value):
        self.addr = "{}/{}".format(value, self.cidr) if value is not None else None

    @property
    def cidr(self):
        return self.addr.split("/")[1] if self.addr is not None else None

    @cidr.setter
    def cidr(self, value):
        self.addr = "{}/{}".format(self.address, value) if value is not None else None

    def save(self, update=True):
        # pylint: disable=duplicate-code
        # Duplicate code required due to the lacking nature of interfaces API
        for key, value in self.to_api_dict().items():
            parameters = {
                "interface": self.interface,
                key: value
            }

            try:
                response = self._get(self._API_MOD, parameters)
            except KempTechApiException as e:
                if str(e) == "Nothing Modified":
                    pass
                else:
                    raise
            else:
                self._is_successful_or_raise(response)

    def stats(self):
        try:
            response = self._get(  # pylint: disable=protected-access
                self._API_LIST)
            data = get_data(response)
            xml_object = data.get(self._API_LIST_TAG, [])
        except KempTechApiException:
            xml_object = []

        # If there is no API_TAG key, build will fail with a
        # ValidationError, which is the best we can do for now
        # (without changing the upstream code and raising an
        # exception earlier, possibly retrying)

        stats = {}

        for interface_details in xml_object.values():
            if interface_details['ifaceID'] == self.interface:
                for k, v in interface_details.items():
                    stats[k.lower()] = v

        return stats

    def populate_default_attributes(self, params):
        params = {} if params is None else params
        super(Interface, self).populate_default_attributes(params)

        # Strip additional addresses into a list
        if not hasattr(self, "additionaladdresses"):
            self.additionaladdresses = []
        elif self.additionaladdresses is None:
            self.additionaladdresses = []
        elif isinstance(self.additionaladdresses, OrderedDict):
            self.additionaladdresses = self.additionaladdresses['IPaddress']
            self.additionaladdresses = cast_to_list(self.additionaladdresses)

        if not hasattr(self, "geotraffic"):
            self.geotraffic = None
        elif self.geotraffic == "no":
            self.geotraffic = "0"
        elif self.geotraffic == "yes":
            self.geotraffic = "1"

        self._additionaladdresses = []

        for address in self.additionaladdresses:
            self._additionaladdresses.append(address)

    def set_additionaladdresses(self):
        new = self.additionaladdresses
        old = self._additionaladdresses

        for address in list(set(old) - set(new)):
            self._delete_additionaladdress(address)

        for address in list(set(new) - set(old)):
            self._add_additionaladdress(address)

        self.refresh()

    def _add_additionaladdress(self, address):
        parameters = {
            "interface": self.interface,
            "addr": address
        }

        response = self._get(  # pylint: disable=protected-access
            self._API_ADD_ADDRESS,
            parameters)

        if not is_successful(response):
            raise KempTechApiException(get_error_msg(response))

    def _delete_additionaladdress(self, address):
        parameters = {
            "interface": self.interface,
            "addr": address
        }

        response = self._get(  # pylint: disable=protected-access
            self._API_DELETE_ADDRESS,
            parameters)

        if not is_successful(response):
            raise KempTechApiException(get_error_msg(response))


class License(BaseKempObject):
    _API_DEFAULT_ATTRIBUTES = {
        "uuid": "uuid",
        "activationdate": "activationdate",
        "licenseduntil": "licenseduntil",
        "supportuntil": "supportuntil",
        "supportlevel": "supportlevel",
        "licensetype": "licensetype",
        "licensestatus": "licensestatus",
        "appliancemodel": "appliancemodel",
        "freelicense": "freelicense",
    }

    def __init__(self, loadmaster_info, params=None):
        """ License constructor

        :param loadmaster_info: LoadMaster access_info
        """
        self.subscriptions = []
        self.populate_default_attributes(params)
        super(License, self).__init__(loadmaster_info)

    def populate_default_attributes(self, params):
        params = {} if params is None else params
        super(License, self).populate_default_attributes(params)

    def save(self, update=False):
        pass

    def __str__(self):
        return 'License type: {}'.format(self.licensetype)


class Subscription(BaseKempObject):
    _API_DEFAULT_ATTRIBUTES = {
        "name": "Name",
        "expires": "Expires",
        "featurelist": "FeatureList",
    }

    def __init__(self, loadmaster_info, params=None):
        """Subscription constructor

        :param loadmaster_info: LoadMaster access_info
        """
        self.populate_default_attributes(params)
        super(Subscription, self).__init__(loadmaster_info)

    def populate_default_attributes(self, params):
        params = {} if params is None else params
        super(Subscription, self).populate_default_attributes(params)

    def save(self, update=False):
        pass

    def __str__(self):
        return 'Subscription type: {}'.format(self.name)
