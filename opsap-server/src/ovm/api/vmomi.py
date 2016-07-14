# coding: utf-8
# Author: Dunkle Qiu

import ssl
import warnings

from pyVim.connect import SmartConnect
from pyVmomi import vim

_sis = {}
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
ssl_context.verify_mode = ssl.CERT_NONE
warnings.filterwarnings("ignore")


def get_si(uuid):
    if _sis.has_key(uuid):
        return _sis[uuid]
    else:
        return None


def set_si(uuid, si):
    global _sis
    _sis[uuid] = si


def get_moid(vimobj):
    return str(vimobj._GetMoId())


def discover_vc(ip, port, user, pwd):
    uuid, version = "", ""
    si = SmartConnect(host=ip, user=user, pwd=pwd, port=port, sslContext=ssl_context)
    if not si:
        return uuid, version
    content = si.RetrieveContent()
    uuid = content.about.instanceUuid
    version = content.about.apiVersion
    set_si(uuid, si)
    return uuid, version


def connect_vc(uuid, ip, port, user, pwd):
    si = get_si(uuid)
    try:
        content = si.RetrieveContent()
        cur_session = content.sessionManager.currentSession
        if cur_session and isinstance(cur_session, vim.UserSession):
            return content
        else:
            content.sessionManager.Login(user, pwd)
    except:
        si = SmartConnect(host=ip, user=user, pwd=pwd, port=port, sslContext=ssl_context)
        set_si(uuid, si)
    finally:
        content = si.RetrieveContent()
        return content


def get_all_custspec(content):
    result_li = []
    for spec in content.customizationSpecManager.info:
        result_li.append({
            'name': spec.name,
            'spec_type': spec.type,
        })
    return result_li


def get_custspec_data(content, name, ipaddress=None):
    custspec = content.customizationSpecManager.Get(name).spec
    if ipaddress:
        ipsetting = custspec.nicSettingMap[0].adapter
        fixip = vim.vm.customization.FixedIp()
        fixip.ipAddress = ipaddress
        ipsetting.ip = fixip
    return custspeck
