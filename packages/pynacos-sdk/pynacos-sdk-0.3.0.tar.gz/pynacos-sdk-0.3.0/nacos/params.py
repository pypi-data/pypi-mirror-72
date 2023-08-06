import json
from .errors import ParamError


class Param(object):
    """参数基类"""
    def json(self):
        return self.__dict__


class ServiceRegisterParam(Param):
    def __init__(self,
                 service_name,
                 group_name="",
                 protect_threshold=0,
                 metadata="",
                 selector=None):
        self.serviceName = service_name
        self.groupName = group_name
        self.protectThreshold = protect_threshold
        self.metadata = metadata
        self.selector = selector
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class ServiceRemoveParam(Param):
    def __init__(self, service_name, group_name=""):
        self.serviceName = service_name
        self.groupName = group_name

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class ServiceUpdateParam(Param):
    def __init__(self,
                 service_name,
                 group_name="",
                 metadata="",
                 protect_threshold=0,
                 selector=None):
        self.serviceName = service_name
        self.groupName = group_name
        self.metadata = metadata
        self.selector = selector
        self.protectThreshold = protect_threshold
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class ServiceGetParam(Param):
    def __init__(self, service_name, group_name=""):
        self.serviceName = service_name
        self.groupName = group_name
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class ServiceListParam(Param):
    def __init__(self, group_name="", page_no=1, page_size=10):
        self.groupName = group_name
        self.pageNo = page_no
        self.pageSize = page_size
        self._validate()

    def _validate(self):
        if not isinstance(self.pageNo, int):
            raise TypeError(
                "page_no should be type of int, but {} found".format(
                    type(self.page_no)))
        if not isinstance(self.pageSize, int):
            raise TypeError(
                "page_size should be type of int, but {} found".format(
                    type(self.page_size)))


class SwitchUpdateParam(Param):
    def __init__(self, entry, value, debug=False):
        self.entry = entry
        self.value = value
        self.debug = debug

    def _validate(self):
        if not self.entry:
            raise ParamError("entry should not be null")


class InstanceRegisterParam(Param):
    def __init__(self,
                 service_name: str,
                 ip: str,
                 port: int,
                 group_name: str = None,
                 weight: float = 0,
                 enabled: bool = False,
                 healthy: bool = True,
                 metadata: str = "",
                 cluster_name: str = "",
                 ephemeral: bool = False):
        self.ip = ip
        self.port = port
        self.serviceName = service_name
        self.groupName = group_name
        self.weight = weight
        self.enabled = enabled
        self.healthy = healthy
        self.metadata = metadata
        self.clusterName = cluster_name
        self.ephemeral = ephemeral
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")
        if not self.ip:
            raise ParamError("ip should not be null")
        if not self.port:
            raise ParamError("port should not be null")
        if not isinstance(self.ip, str):
            raise TypeError("ip should be type of str, but {} found".format(
                type(self.ip)))
        if not isinstance(self.port, int):
            raise TypeError("port should be type of int, but {} found".format(
                type(self.port)))
        if not isinstance(self.weight, (int, float)):
            raise TypeError(
                "weight should be type of int or float, but {} found".format(
                    type(self.weight)))


class InstanceRemoveParam(Param):
    def __init__(self,
                 service_name,
                 ip,
                 port,
                 group_name="",
                 cluster_name="",
                 ephemeral=False):
        self.ip = ip
        self.port = port
        self.service_name = service_name
        self.groupName = group_name
        self.clusterName = cluster_name
        self.ephemeral = ephemeral
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")
        if not self.ip:
            raise ParamError("ip should not be null")
        if not self.port:
            raise ParamError("port should not be null")
        if not isinstance(self.ip, str):
            raise TypeError("ip should be type of str, but {} found".format(
                type(self.ip)))
        if not isinstance(self.port, int):
            raise TypeError("port should be type of int, but {} found".format(
                type(self.port)))


class InstanceUpdateParam(Param):
    def __init__(self,
                 service_name,
                 ip,
                 port,
                 group_name,
                 cluster_name,
                 weight,
                 metadata,
                 enabled,
                 ephemeral=False):
        self.ip = ip
        self.port = port
        self.serviceName = service_name
        self.groupName = group_name
        self.weight = weight
        self.enabled = enabled
        self.metadata = metadata
        self.clusterName = cluster_name
        self.ephemeral = ephemeral
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")
        if not self.ip:
            raise ParamError("ip should not be null")
        if not self.port:
            raise ParamError("port should not be null")
        if not isinstance(self.ip, str):
            raise TypeError("ip should be type of str, but {} found".format(
                type(self.ip)))
        if not isinstance(self.port, int):
            raise TypeError("port should be type of int, but {} found".format(
                type(self.port)))
        if not isinstance(self.weight, (int, float)):
            raise TypeError(
                "weight should be type of int or float, but {} found".format(
                    type(self.weight)))
        if not isinstance(self.metadata, dict):
            raise TypeError(
                "metadata should be type of dict, but {} found".format(
                    type(self.metadata)))


class InstanceListParam(Param):
    def __init__(self,
                 service_name,
                 group_name="",
                 clusters=None,
                 healthy_only=False):
        self.serviceName = service_name
        self.groupName = group_name
        self.clusters = clusters
        self.healthyOnly = healthy_only
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class InstanceGetParam(Param):
    def __init__(self,
                 service_name,
                 ip,
                 port,
                 group_name="",
                 cluster="",
                 healthy_only=False,
                 ephemeral=False):
        self.ip = ip
        self.port = port
        self.groupName = group_name
        self.serviceName = service_name
        self.cluster = cluster
        self.healthyOnly = healthy_only
        self.ephemeral = ephemeral
        self._validate()

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")
        if not self.ip:
            raise ParamError("ip should not be null")
        if not self.port:
            raise ParamError("port should not be null")
        if not isinstance(self.ip, str):
            raise TypeError("ip should be type of str, but {} found".format(
                type(self.ip)))
        if not isinstance(self.port, int):
            raise TypeError("port should be type of int, but {} found".format(
                type(self.port)))


class BeatInfo(Param):
    def __init__(self,
                 service_name,
                 ip,
                 port,
                 weight,
                 scheduled,
                 cluster="",
                 metadata=None):
        if not metadata:
            metadata = {}
        if not isinstance(metadata, dict):
            raise TypeError(
                "metadata should not be type of dict, but {} found".format(
                    type(metadata)))
        self.ip = ip
        self.port = port
        self.weight = weight
        self.scheduled = scheduled
        self.cluster = cluster
        self.metadata = metadata
        self.serviceName = service_name


class InstanceBeatParam(Param):
    def __init__(self, beat: BeatInfo):
        if not isinstance(beat, BeatInfo):
            raise TypeError(
                "beat should not be type of BeatInfo, buf {} found".format(
                    type(beat)))
        self.beat = json.dumps(beat.json())
        self.serviceName = beat.serviceName

    def _validate(self):
        if not self.serviceName:
            raise ParamError("service_name should not be null")


class HealthUpdateParam(Param):
    def __init__(self,
                 service_name,
                 ip,
                 port,
                 healthy,
                 group_name="",
                 cluster_name=""):
        self.ip = ip
        self.port = port
        self.healthy = healthy
        self.groupName = group_name
        self.serviceName = service_name
        self.clusterName = cluster_name

    def _validate(self):
        if not self.ip:
            raise ParamError("ip should not be null")
        if not self.port:
            raise ParamError("port should not be null")
        if not self.service_name:
            raise ParamError("service_name should not be null")
        if not isinstance(self.ip, str):
            raise TypeError("ip should be type of str, but {} found".format(
                type(self.ip)))
        if not isinstance(self.port, int):
            raise TypeError("ip should be type of int, but {} found".format(
                type(self.port)))
        if not isinstance(self.healthy, bool):
            raise TypeError("healthy should be type of bool")


class ServerListParam(Param):
    def __init__(self, healthy=False):
        self.healthy = healthy
        self._validate()

    def _validate(self):
        if not isinstance(self.healthy, bool):
            raise TypeError(
                "healthy should be type of bool, but {} found".format(
                    type(self.healthy)))


class ConfigGetParam(Param):
    def __init__(self, data_id, group):
        self.group = group
        self.dataId = data_id

    def to_json(self, namespace_id):
        r = super().json()
        r["tenant"] = namespace_id
        return r


class ConfigListenParam(Param):
    def __init__(self, data_id, group, content_md5):
        self.group = group
        self.dataId = data_id
        self.contentMD5 = content_md5

    def to_json(self, namespace_id):
        s = "{dataId}^2{group}^2{content_md5}^2{tenant}^1".format(
            tenant=namespace_id,
            dataId=self.dataId,
            group=self.group,
            content_md5=self.contentMD5,
        )
        return {"Listening-Configs": s}


class ConfigPublishParam(Param):
    def __init__(self, data_id, group, content, tp=""):
        self.group = group
        self.dataId = data_id
        self.content = content
        self.type = tp

    def to_json(self, namespace_id):
        r = super().json()
        r["tenant"] = namespace_id
        return r


class ConfigRemoveParam(Param):
    def __init__(self, data_id, group):
        self.group = group
        self.dataId = data_id

    def to_json(self, namespace_id):
        r = super().json()
        r["tenant"] = namespace_id
        return r
