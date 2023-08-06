# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel

"""
Model for initing client
"""


class Config(TeaModel):
    def __init__(self, access_key_id=None, access_key_secret=None, auth_token=None, protocol=None, region_id=None, read_timeout=None, connect_timeout=None, http_proxy=None, https_proxy=None, endpoint=None, no_proxy=None, max_idle_conns=None, user_agent=None, socks_5proxy=None, socks_5net_work=None, tenant=None, workspace=None):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.auth_token = auth_token
        self.protocol = protocol
        self.region_id = region_id
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.endpoint = endpoint
        self.no_proxy = no_proxy
        self.max_idle_conns = max_idle_conns
        self.user_agent = user_agent
        self.socks_5proxy = socks_5proxy
        self.socks_5net_work = socks_5net_work
        self.tenant = tenant
        self.workspace = workspace

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['accessKeyId'] = self.access_key_id
        result['accessKeySecret'] = self.access_key_secret
        result['authToken'] = self.auth_token
        result['protocol'] = self.protocol
        result['regionId'] = self.region_id
        result['readTimeout'] = self.read_timeout
        result['connectTimeout'] = self.connect_timeout
        result['httpProxy'] = self.http_proxy
        result['httpsProxy'] = self.https_proxy
        result['endpoint'] = self.endpoint
        result['noProxy'] = self.no_proxy
        result['maxIdleConns'] = self.max_idle_conns
        result['userAgent'] = self.user_agent
        result['socks5Proxy'] = self.socks_5proxy
        result['socks5NetWork'] = self.socks_5net_work
        result['tenant'] = self.tenant
        result['workspace'] = self.workspace
        return result

    def from_map(self, map={}):
        self.access_key_id = map.get('accessKeyId')
        self.access_key_secret = map.get('accessKeySecret')
        self.auth_token = map.get('authToken')
        self.protocol = map.get('protocol')
        self.region_id = map.get('regionId')
        self.read_timeout = map.get('readTimeout')
        self.connect_timeout = map.get('connectTimeout')
        self.http_proxy = map.get('httpProxy')
        self.https_proxy = map.get('httpsProxy')
        self.endpoint = map.get('endpoint')
        self.no_proxy = map.get('noProxy')
        self.max_idle_conns = map.get('maxIdleConns')
        self.user_agent = map.get('userAgent')
        self.socks_5proxy = map.get('socks5Proxy')
        self.socks_5net_work = map.get('socks5NetWork')
        self.tenant = map.get('tenant')
        self.workspace = map.get('workspace')
        return self


class RiskSwitchInfo(TeaModel):
    def __init__(self, biz_op=None, biz_tag=None, error_msg=None, group=None, id=None, sec_request_url=None, value=None):
        self.biz_op = biz_op
        self.biz_tag = biz_tag
        self.error_msg = error_msg
        self.group = group
        self.id = id
        self.sec_request_url = sec_request_url
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['biz_op'] = self.biz_op
        result['biz_tag'] = self.biz_tag
        result['error_msg'] = self.error_msg
        result['group'] = self.group
        result['id'] = self.id
        result['sec_request_url'] = self.sec_request_url
        result['value'] = self.value
        return result

    def from_map(self, map={}):
        self.biz_op = map.get('biz_op')
        self.biz_tag = map.get('biz_tag')
        self.error_msg = map.get('error_msg')
        self.group = map.get('group')
        self.id = map.get('id')
        self.sec_request_url = map.get('sec_request_url')
        self.value = map.get('value')
        return self


class ExtraParamInfo(TeaModel):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['key'] = self.key
        result['value'] = self.value
        return result

    def from_map(self, map={}):
        self.key = map.get('key')
        self.value = map.get('value')
        return self


class AddBizpunishRequest(TeaModel):
    def __init__(self, action_code=None, action_type=None, ext_params=None, instance_id=None, object_type=None, prod_code=None, reason=None, request_id=None, risk_level=None, src_request_id=None, tenant_id=None):
        self.action_code = action_code
        self.action_type = action_type
        self.ext_params = ext_params
        self.instance_id = instance_id
        self.object_type = object_type
        self.prod_code = prod_code
        self.reason = reason
        self.request_id = request_id
        self.risk_level = risk_level
        self.src_request_id = src_request_id
        self.tenant_id = tenant_id

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['action_code'] = self.action_code
        result['action_type'] = self.action_type
        result['ext_params'] = self.ext_params
        result['instance_id'] = self.instance_id
        result['object_type'] = self.object_type
        result['prod_code'] = self.prod_code
        result['reason'] = self.reason
        result['request_id'] = self.request_id
        result['risk_level'] = self.risk_level
        result['src_request_id'] = self.src_request_id
        result['tenant_id'] = self.tenant_id
        return result

    def from_map(self, map={}):
        self.action_code = map.get('action_code')
        self.action_type = map.get('action_type')
        self.ext_params = map.get('ext_params')
        self.instance_id = map.get('instance_id')
        self.object_type = map.get('object_type')
        self.prod_code = map.get('prod_code')
        self.reason = map.get('reason')
        self.request_id = map.get('request_id')
        self.risk_level = map.get('risk_level')
        self.src_request_id = map.get('src_request_id')
        self.tenant_id = map.get('tenant_id')
        return self


class AddBizpunishResponse(TeaModel):
    def __init__(self, action_result=None, request_id=None):
        self.action_result = action_result
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['action_result'] = self.action_result
        result['request_id'] = self.request_id
        return result

    def from_map(self, map={}):
        self.action_result = map.get('action_result')
        self.request_id = map.get('request_id')
        return self


class ConfirmRiskRequest(TeaModel):
    def __init__(self, biz_op=None, biz_tag=None, ext_params=None, operator_id=None, security_id=None):
        self.biz_op = biz_op
        self.biz_tag = biz_tag
        self.ext_params = []
        self.operator_id = operator_id
        self.security_id = security_id

    def validate(self):
        if self.ext_params:
            for k in self.ext_params:
                if k :
                    k.validate()

    def to_map(self):
        result = {}
        result['biz_op'] = self.biz_op
        result['biz_tag'] = self.biz_tag
        result['ext_params'] = []
        if self.ext_params is not None:
            for k in self.ext_params:
                result['ext_params'].append(k.to_map() if k else None)
        else:
            result['ext_params'] = None
        result['operator_id'] = self.operator_id
        result['security_id'] = self.security_id
        return result

    def from_map(self, map={}):
        self.biz_op = map.get('biz_op')
        self.biz_tag = map.get('biz_tag')
        self.ext_params = []
        if map.get('ext_params') is not None:
            for k in map.get('ext_params'):
                temp_model = ExtraParamInfo()
                temp_model = temp_model.from_map(k)
                self.ext_params.append(temp_model)
        else:
            self.ext_params = None
        self.operator_id = map.get('operator_id')
        self.security_id = map.get('security_id')
        return self


class ConfirmRiskResponse(TeaModel):
    def __init__(self, confirm_success=None):
        self.confirm_success = confirm_success

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['confirm_success'] = self.confirm_success
        return result

    def from_map(self, map={}):
        self.confirm_success = map.get('confirm_success')
        return self


class QueryRiskSwitchRequest(TeaModel):
    def __init__(self, biz_op=None, biz_tag=None, group=None, sec_request_url=None):
        self.biz_op = biz_op
        self.biz_tag = biz_tag
        self.group = group
        self.sec_request_url = sec_request_url

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['biz_op'] = self.biz_op
        result['biz_tag'] = self.biz_tag
        result['group'] = self.group
        result['sec_request_url'] = self.sec_request_url
        return result

    def from_map(self, map={}):
        self.biz_op = map.get('biz_op')
        self.biz_tag = map.get('biz_tag')
        self.group = map.get('group')
        self.sec_request_url = map.get('sec_request_url')
        return self


class QueryRiskSwitchResponse(TeaModel):
    def __init__(self, risk_switch_info=None):
        self.risk_switch_info = []

    def validate(self):
        if self.risk_switch_info:
            for k in self.risk_switch_info:
                if k :
                    k.validate()

    def to_map(self):
        result = {}
        result['risk_switch_info'] = []
        if self.risk_switch_info is not None:
            for k in self.risk_switch_info:
                result['risk_switch_info'].append(k.to_map() if k else None)
        else:
            result['risk_switch_info'] = None
        return result

    def from_map(self, map={}):
        self.risk_switch_info = []
        if map.get('risk_switch_info') is not None:
            for k in map.get('risk_switch_info'):
                temp_model = RiskSwitchInfo()
                temp_model = temp_model.from_map(k)
                self.risk_switch_info.append(temp_model)
        else:
            self.risk_switch_info = None
        return self


class QueryRiskRequest(TeaModel):
    def __init__(self, biz_op=None, biz_tag=None, callback_url=None, client_ip=None, ext_params=None, login_name=None, operator_id=None, server_name=None, tenant=None, token_id=None, umid=None):
        self.biz_op = biz_op
        self.biz_tag = biz_tag
        self.callback_url = callback_url
        self.client_ip = client_ip
        self.ext_params = []
        self.login_name = login_name
        self.operator_id = operator_id
        self.server_name = server_name
        self.tenant = tenant
        self.token_id = token_id
        self.umid = umid

    def validate(self):
        if self.ext_params:
            for k in self.ext_params:
                if k :
                    k.validate()

    def to_map(self):
        result = {}
        result['biz_op'] = self.biz_op
        result['biz_tag'] = self.biz_tag
        result['callback_url'] = self.callback_url
        result['client_ip'] = self.client_ip
        result['ext_params'] = []
        if self.ext_params is not None:
            for k in self.ext_params:
                result['ext_params'].append(k.to_map() if k else None)
        else:
            result['ext_params'] = None
        result['login_name'] = self.login_name
        result['operator_id'] = self.operator_id
        result['server_name'] = self.server_name
        result['tenant'] = self.tenant
        result['token_id'] = self.token_id
        result['umid'] = self.umid
        return result

    def from_map(self, map={}):
        self.biz_op = map.get('biz_op')
        self.biz_tag = map.get('biz_tag')
        self.callback_url = map.get('callback_url')
        self.client_ip = map.get('client_ip')
        self.ext_params = []
        if map.get('ext_params') is not None:
            for k in map.get('ext_params'):
                temp_model = ExtraParamInfo()
                temp_model = temp_model.from_map(k)
                self.ext_params.append(temp_model)
        else:
            self.ext_params = None
        self.login_name = map.get('login_name')
        self.operator_id = map.get('operator_id')
        self.server_name = map.get('server_name')
        self.tenant = map.get('tenant')
        self.token_id = map.get('token_id')
        self.umid = map.get('umid')
        return self


class QueryRiskResponse(TeaModel):
    def __init__(self, security_id=None, sec_result=None, template_code=None, template_desc=None, verify_id=None, verify_url=None):
        self.security_id = security_id
        self.sec_result = sec_result
        self.template_code = template_code
        self.template_desc = template_desc
        self.verify_id = verify_id
        self.verify_url = verify_url

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['security_id'] = self.security_id
        result['sec_result'] = self.sec_result
        result['template_code'] = self.template_code
        result['template_desc'] = self.template_desc
        result['verify_id'] = self.verify_id
        result['verify_url'] = self.verify_url
        return result

    def from_map(self, map={}):
        self.security_id = map.get('security_id')
        self.sec_result = map.get('sec_result')
        self.template_code = map.get('template_code')
        self.template_desc = map.get('template_desc')
        self.verify_id = map.get('verify_id')
        self.verify_url = map.get('verify_url')
        return self


class AnalyzeContentriskRequest(TeaModel):
    def __init__(self, app_main_scene=None, app_main_scene_id=None, app_name=None, app_scene=None, app_scene_data_id=None, audio_urls=None, link_urls=None, operator_id=None, picture_urls=None, publish_date=None, tenant=None, text=None, video_urls=None):
        self.app_main_scene = app_main_scene
        self.app_main_scene_id = app_main_scene_id
        self.app_name = app_name
        self.app_scene = app_scene
        self.app_scene_data_id = app_scene_data_id
        self.audio_urls = []
        self.link_urls = []
        self.operator_id = operator_id
        self.picture_urls = []
        self.publish_date = publish_date
        self.tenant = tenant
        self.text = text
        self.video_urls = []

    def validate(self):
        if self.app_main_scene:
            self.validate_max_length(app_main_scene, 'app_main_scene', 0)
        if self.app_main_scene_id:
            self.validate_max_length(app_main_scene_id, 'app_main_scene_id', 0)
        if self.app_name:
            self.validate_max_length(app_name, 'app_name', 0)
        if self.app_scene:
            self.validate_max_length(app_scene, 'app_scene', 0)
        if self.app_scene_data_id:
            self.validate_max_length(app_scene_data_id, 'app_scene_data_id', 0)
        if self.publish_date:
            self.validate_pattern(publish_date, 'publish_date', '\\d{4}[-]\\d{1,2}[-]\\d{1,2}(\\s\\d{2}:\\d{2}(:\\d{2})?)?')
        if self.text:
            self.validate_max_length(text, 'text', 0)

    def to_map(self):
        result = {}
        result['app_main_scene'] = self.app_main_scene
        result['app_main_scene_id'] = self.app_main_scene_id
        result['app_name'] = self.app_name
        result['app_scene'] = self.app_scene
        result['app_scene_data_id'] = self.app_scene_data_id
        result['audio_urls'] = []
        if self.audio_urls is not None:
            for k in self.audio_urls:
                result['audio_urls'].append(k)
        else:
            result['audio_urls'] = None
        result['link_urls'] = []
        if self.link_urls is not None:
            for k in self.link_urls:
                result['link_urls'].append(k)
        else:
            result['link_urls'] = None
        result['operator_id'] = self.operator_id
        result['picture_urls'] = []
        if self.picture_urls is not None:
            for k in self.picture_urls:
                result['picture_urls'].append(k)
        else:
            result['picture_urls'] = None
        result['publish_date'] = self.publish_date
        result['tenant'] = self.tenant
        result['text'] = self.text
        result['video_urls'] = []
        if self.video_urls is not None:
            for k in self.video_urls:
                result['video_urls'].append(k)
        else:
            result['video_urls'] = None
        return result

    def from_map(self, map={}):
        self.app_main_scene = map.get('app_main_scene')
        self.app_main_scene_id = map.get('app_main_scene_id')
        self.app_name = map.get('app_name')
        self.app_scene = map.get('app_scene')
        self.app_scene_data_id = map.get('app_scene_data_id')
        self.audio_urls = []
        if map.get('audio_urls') is not None:
            for k in map.get('audio_urls'):
                self.audio_urls.append(k)
        else:
            self.audio_urls = None
        self.link_urls = []
        if map.get('link_urls') is not None:
            for k in map.get('link_urls'):
                self.link_urls.append(k)
        else:
            self.link_urls = None
        self.operator_id = map.get('operator_id')
        self.picture_urls = []
        if map.get('picture_urls') is not None:
            for k in map.get('picture_urls'):
                self.picture_urls.append(k)
        else:
            self.picture_urls = None
        self.publish_date = map.get('publish_date')
        self.tenant = map.get('tenant')
        self.text = map.get('text')
        self.video_urls = []
        if map.get('video_urls') is not None:
            for k in map.get('video_urls'):
                self.video_urls.append(k)
        else:
            self.video_urls = None
        return self


class AnalyzeContentriskResponse(TeaModel):
    def __init__(self, app_scene_data_id=None, event_id=None, need_query=None, reason=None, result_action=None):
        self.app_scene_data_id = app_scene_data_id
        self.event_id = event_id
        self.need_query = need_query
        self.reason = reason
        self.result_action = result_action

    def validate(self):
        if self.app_scene_data_id:
            self.validate_max_length(app_scene_data_id, 'app_scene_data_id', 0)
        if self.event_id:
            self.validate_max_length(event_id, 'event_id', 0)
        if self.need_query:
            self.validate_max_length(need_query, 'need_query', 0)
        if self.reason:
            self.validate_max_length(reason, 'reason', 0)
        if self.result_action:
            self.validate_max_length(result_action, 'result_action', 0)

    def to_map(self):
        result = {}
        result['app_scene_data_id'] = self.app_scene_data_id
        result['event_id'] = self.event_id
        result['need_query'] = self.need_query
        result['reason'] = self.reason
        result['result_action'] = self.result_action
        return result

    def from_map(self, map={}):
        self.app_scene_data_id = map.get('app_scene_data_id')
        self.event_id = map.get('event_id')
        self.need_query = map.get('need_query')
        self.reason = map.get('reason')
        self.result_action = map.get('result_action')
        return self


class NotifyRiskRequest(TeaModel):
    def __init__(self, biz_op=None, biz_result=None, biz_tag=None, ext_params=None, operator_id=None, security_id=None, tenant=None):
        self.biz_op = biz_op
        self.biz_result = biz_result
        self.biz_tag = biz_tag
        self.ext_params = []
        self.operator_id = operator_id
        self.security_id = security_id
        self.tenant = tenant

    def validate(self):
        if self.ext_params:
            for k in self.ext_params:
                if k :
                    k.validate()

    def to_map(self):
        result = {}
        result['biz_op'] = self.biz_op
        result['biz_result'] = self.biz_result
        result['biz_tag'] = self.biz_tag
        result['ext_params'] = []
        if self.ext_params is not None:
            for k in self.ext_params:
                result['ext_params'].append(k.to_map() if k else None)
        else:
            result['ext_params'] = None
        result['operator_id'] = self.operator_id
        result['security_id'] = self.security_id
        result['tenant'] = self.tenant
        return result

    def from_map(self, map={}):
        self.biz_op = map.get('biz_op')
        self.biz_result = map.get('biz_result')
        self.biz_tag = map.get('biz_tag')
        self.ext_params = []
        if map.get('ext_params') is not None:
            for k in map.get('ext_params'):
                temp_model = ExtraParamInfo()
                temp_model = temp_model.from_map(k)
                self.ext_params.append(temp_model)
        else:
            self.ext_params = None
        self.operator_id = map.get('operator_id')
        self.security_id = map.get('security_id')
        self.tenant = map.get('tenant')
        return self


class NotifyRiskResponse(TeaModel):
    def __init__(self):
        pass

    def validate(self):
        pass

    def to_map(self):
        result = {}
        return result

    def from_map(self, map={}):
        return self


class QueryContentriskResultRequest(TeaModel):
    def __init__(self, app_scene=None, app_scene_data_id=None, event_id=None):
        self.app_scene = app_scene
        self.app_scene_data_id = app_scene_data_id
        self.event_id = event_id

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['app_scene'] = self.app_scene
        result['app_scene_data_id'] = self.app_scene_data_id
        result['event_id'] = self.event_id
        return result

    def from_map(self, map={}):
        self.app_scene = map.get('app_scene')
        self.app_scene_data_id = map.get('app_scene_data_id')
        self.event_id = map.get('event_id')
        return self


class QueryContentriskResultResponse(TeaModel):
    def __init__(self, reason=None, result_action=None):
        self.reason = reason
        self.result_action = result_action

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['reason'] = self.reason
        result['result_action'] = self.result_action
        return result

    def from_map(self, map={}):
        self.reason = map.get('reason')
        self.result_action = map.get('result_action')
        return self
