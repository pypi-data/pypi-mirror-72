# This file is auto-generated, don't edit it. Thanks.
import time

from antchain_sdk_risk import models as risk_models
from alibabacloud_tea_util.client import Client as UtilClient
from Tea.exceptions import TeaException
from alibabacloud_tea_util import models as util_models
from Tea.request import TeaRequest
from Tea.core import TeaCore
from Tea.response import TeaResponse
from antchain_alipay_util.client import Client as AlipayUtilClient
from alibabacloud_rpc_util.client import Client as RPCUtilClient
from Tea.exceptions import UnretryableException


class Client:
    def __init__(self, config, _endpoint=None, _region_id=None, _access_key_id=None, _access_key_secret=None, _protocol=None, _user_agent=None, _read_timeout=None, _connect_timeout=None, _http_proxy=None, _https_proxy=None, _socks_5proxy=None, _socks_5net_work=None, _no_proxy=None, _max_idle_conns=None, _auth_token=None, _tenant=None, _workspace=None):
        """
        Init client with Config
        @param config: config contains the necessary information to create a client
        """
        self._endpoint = _endpoint
        self._region_id = _region_id
        self._access_key_id = _access_key_id
        self._access_key_secret = _access_key_secret
        self._protocol = _protocol
        self._user_agent = _user_agent
        self._read_timeout = _read_timeout
        self._connect_timeout = _connect_timeout
        self._http_proxy = _http_proxy
        self._https_proxy = _https_proxy
        self._socks_5proxy = _socks_5proxy
        self._socks_5net_work = _socks_5net_work
        self._no_proxy = _no_proxy
        self._max_idle_conns = _max_idle_conns
        self._auth_token = _auth_token
        self._tenant = _tenant
        self._workspace = _workspace
        if UtilClient.is_unset(config.to_map()):
            raise TeaException({
                "code": "ParameterMissing",
                "message": "'config' can not be unset"
            })
        self._access_key_id = config.access_key_id
        self._access_key_secret = config.access_key_secret
        self._tenant = config.tenant
        self._workspace = config.workspace
        self._endpoint = config.endpoint
        self._auth_token = config.auth_token
        self._protocol = config.protocol
        self._region_id = config.region_id
        self._user_agent = config.user_agent
        self._read_timeout = config.read_timeout
        self._connect_timeout = config.connect_timeout
        self._http_proxy = config.http_proxy
        self._https_proxy = config.https_proxy
        self._no_proxy = config.no_proxy
        self._socks_5proxy = config.socks_5proxy
        self._socks_5net_work = config.socks_5net_work
        self._max_idle_conns = config.max_idle_conns

    def do_request(self, action, protocol, method, pathname, request, runtime):
        """
        Encapsulate the request and invoke the network
        @param action: api name
        @param protocol: http or https
        @param method: e.g. GET
        @param pathname: pathname of every api
        @param request: which contains request params
        @param runtime: which controls some details of call api, such as retry times
        @return the response
        """
        runtime.validate()
        _runtime = {
            "timeouted": "retry",
            "readTimeout": UtilClient.default_number(runtime.read_timeout, self._read_timeout),
            "connectTimeout": UtilClient.default_number(runtime.connect_timeout, self._connect_timeout),
            "httpProxy": UtilClient.default_string(runtime.http_proxy, self._http_proxy),
            "httpsProxy": UtilClient.default_string(runtime.https_proxy, self._https_proxy),
            "noProxy": UtilClient.default_string(runtime.no_proxy, self._no_proxy),
            "maxIdleConns": UtilClient.default_number(runtime.max_idle_conns, self._max_idle_conns),
            "retry": {
                "retryable": runtime.autoretry,
                "maxAttempts": UtilClient.default_number(runtime.max_attempts, 3)
            },
            "backoff": {
                "policy": UtilClient.default_string(runtime.backoff_policy, "no"),
                "period": UtilClient.default_number(runtime.backoff_period, 1)
            },
            "ignoreSSL": runtime.ignore_ssl
        }
        _last_request = None
        _last_exception = None
        _now = time.time()
        _retry_times = 0
        while TeaCore.allow_retry(_runtime.get('retry'), _retry_times, _now):
            if _retry_times > 0:
                _backoff_time = TeaCore.get_backoff_time(_runtime.get('backoff'), _retry_times)
                if _backoff_time > 0:
                    TeaCore.sleep(_backoff_time)
            _retry_times = _retry_times + 1
            try:
                _request = TeaRequest()
                _request.protocol = UtilClient.default_string(self._protocol, protocol)
                _request.method = method
                _request.pathname = pathname
                _request.query = {
                    "method": action,
                    "version": "1.0",
                    "sign_type": "HmacSHA1",
                    "req_time": AlipayUtilClient.get_timestamp(),
                    "req_msg_id": UtilClient.get_nonce()
                }
                if not UtilClient.empty(self._tenant):
                    _request.query["tenant"] = self._tenant
                if not UtilClient.empty(self._workspace):
                    _request.query["workspace"] = self._workspace
                if not UtilClient.empty(self._auth_token):
                    _request.query["auth_token"] = self._auth_token
                else:
                    _request.query["access_key"] = self._access_key_id
                _request.headers = {
                    "host": self._endpoint,
                    "user-agent": self.get_user_agent()
                }
                tmp = UtilClient.anyify_map_value(RPCUtilClient.query(request))
                _request.body = UtilClient.to_form_string(tmp)
                _request.headers["content-type"] = "application/x-www-form-urlencoded"
                signed_param = TeaCore.merge(_request.query,
                    RPCUtilClient.query(request))
                _request.query["sign"] = AlipayUtilClient.get_signature(signed_param, self._access_key_secret)
                _last_request = _request
                _response = TeaCore.do_action(_request, _runtime)
                obj = UtilClient.read_as_json(_response.body)
                res = UtilClient.assert_as_map(obj)
                resp = UtilClient.assert_as_map(res.get('response'))
                if AlipayUtilClient.has_error(res):
                    raise TeaException({
                        "message": resp.get('result_msg'),
                        "data": resp,
                        "code": resp.get('result_code')
                    })
                return resp
            except Exception as e:
                if TeaCore.is_retryable(e):
                    _last_exception = e
                    continue
                raise e
        raise UnretryableException(_last_request, _last_exception)

    def get_user_agent(self):
        """
        Get user agent
        @return user agent
        """
        user_agent = UtilClient.get_user_agent(self._user_agent)
        return user_agent

    def add_bizpunish(self, request):
        """
        Description: 风控新增业务处罚API，用于新增业务处罚信息
        Summary: 风控新增业务处罚API
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.add_bizpunish_ex(request, runtime)

    def add_bizpunish_ex(self, request, runtime):
        """
        Description: 风控新增业务处罚API，用于新增业务处罚信息
        Summary: 风控新增业务处罚API
        """
        UtilClient.validate_model(request)
        return risk_models.AddBizpunishResponse().from_map(self.do_request("antcloud.riskcontrol.bizpunish.add", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def confirm_risk(self, request):
        """
        Description: 风险结果确认（后端进行doublecheck），用于业务执行前，业务方发起风险确认，判定对应的操作是否确实安全
        Summary: 风险结果确认
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.confirm_risk_ex(request, runtime)

    def confirm_risk_ex(self, request, runtime):
        """
        Description: 风险结果确认（后端进行doublecheck），用于业务执行前，业务方发起风险确认，判定对应的操作是否确实安全
        Summary: 风险结果确认
        """
        UtilClient.validate_model(request)
        return risk_models.ConfirmRiskResponse().from_map(self.do_request("antcloud.riskcontrol.risk.confirm", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def query_risk_switch(self, request):
        """
        Description: 查询风险事件的开关信息
        Summary: 查询风险事件的开关信息
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.query_risk_switch_ex(request, runtime)

    def query_risk_switch_ex(self, request, runtime):
        """
        Description: 查询风险事件的开关信息
        Summary: 查询风险事件的开关信息
        """
        UtilClient.validate_model(request)
        return risk_models.QueryRiskSwitchResponse().from_map(self.do_request("antcloud.riskcontrol.risk.switch.query", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def query_risk(self, request):
        """
        Description: 风险事件查询API，用于查询当前业务是否存在风险
        Summary: 风险事件查询API
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.query_risk_ex(request, runtime)

    def query_risk_ex(self, request, runtime):
        """
        Description: 风险事件查询API，用于查询当前业务是否存在风险
        Summary: 风险事件查询API
        """
        UtilClient.validate_model(request)
        return risk_models.QueryRiskResponse().from_map(self.do_request("antcloud.riskcontrol.risk.query", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def analyze_contentrisk(self, request):
        """
        Description: 内容风险分析API，用于分析当前内容是否存在风险
        Summary: 内容风险分析API
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.analyze_contentrisk_ex(request, runtime)

    def analyze_contentrisk_ex(self, request, runtime):
        """
        Description: 内容风险分析API，用于分析当前内容是否存在风险
        Summary: 内容风险分析API
        """
        UtilClient.validate_model(request)
        return risk_models.AnalyzeContentriskResponse().from_map(self.do_request("antcloud.riskcontrol.contentrisk.analyze", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def notify_risk(self, request):
        """
        Description: 业务处理完成后，将结果通知给风险
        Summary: 业务结果通知
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.notify_risk_ex(request, runtime)

    def notify_risk_ex(self, request, runtime):
        """
        Description: 业务处理完成后，将结果通知给风险
        Summary: 业务结果通知
        """
        UtilClient.validate_model(request)
        return risk_models.NotifyRiskResponse().from_map(self.do_request("antcloud.riskcontrol.risk.notify", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))


    def query_contentrisk_result(self, request):
        """
        Description: 内容风险分析结果查询API，用于风险分析结果的异步查询
        Summary: 内容风险分析结果查询API
        """
        runtime = util_models.RuntimeOptions(

        )
        return self.query_contentrisk_result_ex(request, runtime)

    def query_contentrisk_result_ex(self, request, runtime):
        """
        Description: 内容风险分析结果查询API，用于风险分析结果的异步查询
        Summary: 内容风险分析结果查询API
        """
        UtilClient.validate_model(request)
        return risk_models.QueryContentriskResultResponse().from_map(self.do_request("antcloud.riskcontrol.contentrisk.result.query", "HTTPS", "POST", "/gateway.do", request.to_map(), runtime))

