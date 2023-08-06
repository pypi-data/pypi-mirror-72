import copy
from typing import List


class Entity(object):
    """返回值基类"""
    def json(self):
        r = copy.deepcopy(self.__dict__)
        for key, val in r.items():
            if isinstance(val, Entity):
                r[key] = val.json()
            elif isinstance(val, (list, tuple)):
                for i in range(len(val)):
                    if isinstance(val[i], Entity):
                        val[i] = val[i].json()
        return r


class PermissionEntity(Entity):
    def __init__(self, **kwargs):
        self.role = kwargs["role"]
        self.action = kwargs["action"]
        self.resource = kwargs["resource"]


class LoginResponse(Entity):
    def __init__(self, **kwargs):
        self.token_ttl = kwargs["tokenTtl"]
        self.global_admin = kwargs["globalAdmin"]
        self.access_token = kwargs["accessToken"]


class RoleListResponse(Entity):
    def __init__(self, **kwargs):
        self.page = kwargs["pageNumber"]
        self.total_page = kwargs["pagesAvailable"]
        self.total_count = kwargs["totalCount"]
        self.roles: List[str] = [item["role"] for item in kwargs["pageItems"]]


class PermissionListResponse(Entity):
    def __init__(self, **kwargs):
        self.page = kwargs["pageNumber"]
        self.total_page = kwargs["pagesAvailable"]
        self.total_count = kwargs["totalCount"]
        self.permissions: List[PermissionEntity] = [
            PermissionEntity(**item) for item in kwargs["pageItems"]
        ]


class ServiceEntity(Entity):
    """服务"""
    def __init__(self, name, group_name, namespace_id, metadata, clusters,
                 selector, protect_threshold):
        if not name:
            raise ValueError("name should not be null")
        if not group_name:
            raise ValueError("group_name should not be null")
        if not namespace_id:
            raise ValueError("namespace_id should not be null")
        if not isinstance(metadata, (dict, type(None))):
            raise TypeError(
                "metadata should be type of dict, but {} found".format(
                    type(metadata)))
        if not isinstance(clusters, (list, type(None))):
            raise TypeError(
                "clusters should be type of list, but {} found".format(
                    type(clusters)))
        if not isinstance(selector, (dict, type(None))):
            raise TypeError(
                "selector should be type of dict, but {} found".format(
                    type(selector)))
        self.name = name
        self.group_name = group_name
        self.namespace_id = namespace_id
        self.metadata = metadata if metadata else {}
        self.clusters = clusters
        self.selector = selector
        self.protect_threshold = protect_threshold

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            name=kwargs.get("name"),
            group_name=kwargs.get("groupName"),
            namespace_id=kwargs.get("namespaceId"),
            metadata=kwargs.get("metadata"),
            clusters=kwargs.get("clusters"),
            selector=kwargs.get("selector"),
            protect_threshold=kwargs.get("protectThreshold"),
        )


class ServiceListEntity(Entity):
    def __init__(self, count, doms):
        self.count = count
        self.doms = doms

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            count=kwargs.get("count"),
            doms=kwargs.get("doms"),
        )


class InstanceEntity(Entity):
    """实例"""
    def __init__(self, instance_id, service, ip, port, cluster_name, healthy,
                 metadata):
        if not instance_id:
            raise ValueError("instance_id should not be null")
        if not service:
            raise ValueError("service should not be null")
        if not ip:
            raise ValueError("ip should not be null")
        if not port:
            raise ValueError("port should not be null")
        if not cluster_name:
            raise ValueError("cluster_name should not be null")
        if not isinstance(healthy, bool):
            raise TypeError(
                "healthy should be type of bool, but {} found".format(
                    type(healthy)))
        if not isinstance(metadata, (dict, type(None))):
            raise TypeError(
                "metadata should be type of dict, but {} found".format(
                    type(metadata)))
        self.instance_id = instance_id
        self.service = service
        self.ip = ip
        self.port = port
        self.cluster_name = cluster_name
        self.healthy = healthy
        self.metadata = metadata

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            instance_id=kwargs.get("instanceId"),
            service=kwargs.get("service"),
            ip=kwargs.get("ip"),
            port=kwargs.get("port"),
            cluster_name=kwargs.get("clusterName"),
            healthy=kwargs.get("healthy"),
            metadata=kwargs.get("metadata"),
        )


class HostEntity(Entity):
    def __init__(self, ip, port, weight, instance_id, valid, metadata):
        self.ip = ip
        self.port = port
        self.weight = weight
        self.valid = valid
        self.metadata = metadata
        self.instanceId = instance_id

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            ip=kwargs.get("ip"),
            port=kwargs.get("port"),
            weight=kwargs.get("weight"),
            instance_id=kwargs.get("instanceId"),
            valid=kwargs.get("valid"),
            metadata=kwargs.get("metadata"),
        )


class InstanceListEntity(Entity):
    def __init__(self, dom, env, hosts: List[HostEntity], checksum, clusters,
                 cache_millis, last_ref_time, use_specified_url):
        self.dom = dom
        self.env = env
        self.hosts = hosts
        self.checksum = checksum
        self.clusters = clusters
        self.cache_millis = cache_millis
        self.last_ref_time = last_ref_time
        self.use_specified_url = use_specified_url

    @classmethod
    def loads(cls, **kwargs):
        hosts = kwargs.get("hosts")
        hosts = [HostEntity.loads(**host) for host in hosts] if hosts else []
        return cls(
            dom=kwargs.get("dom"),
            env=kwargs.get("env"),
            hosts=hosts,
            checksum=kwargs.get("checksum"),
            clusters=kwargs.get("clusters"),
            cache_millis=kwargs.get("cacheMillis"),
            last_ref_time=kwargs.get("lastRefTime"),
            use_specified_url=kwargs.get("useSpecifiedURL"),
        )


class ServerEntity(Entity):
    def __init__(self, ip, port, key, site, weight, alive, ad_weight,
                 last_ref_time, last_ref_time_str):
        self.ip = ip
        self.port = port
        self.key = key
        self.site = site
        self.weight = weight
        self.alive = alive
        self.ad_weight = ad_weight
        self.last_ref_time = last_ref_time
        self.last_ref_time_str = last_ref_time_str

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            ip=kwargs.get("ip"),
            port=kwargs.get("port"),
            key=kwargs.get("key"),
            site=kwargs.get("site"),
            weight=kwargs.get("weight"),
            alive=kwargs.get("alive"),
            ad_weight=kwargs.get("adWeight"),
            last_ref_time=kwargs.get("lastRefTime"),
            last_ref_time_str=kwargs.get("lastRefTimeStr"),
        )


class LeaderEntity(Entity):
    def __init__(self, ip, state, term, vote_for, leader_due_ms,
                 heartbeat_due_ms):
        self.ip = ip
        self.state = state
        self.term = term
        self.vote_for = vote_for
        self.leader_due_ms = leader_due_ms
        self.heartbeat_due_ms = heartbeat_due_ms

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            ip=kwargs.get("ip"),
            state=kwargs.get("state"),
            term=kwargs.get("term"),
            vote_for=kwargs.get("voteFor"),
            leader_due_ms=kwargs.get("leaderDueMs"),
            heartbeat_due_ms=kwargs.get("heartbeatDueMs"),
        )


class MetricsEntity(Entity):
    def __init__(self, service_count, instance_count, load, mem, cpu, status,
                 responsible_service_count, responsible_instance_count):
        self.mem = mem
        self.cpu = cpu
        self.load = load
        self.status = status
        self.service_count = service_count
        self.instance_count = instance_count
        self.responsible_service_count = responsible_service_count
        self.responsible_instance_count = responsible_instance_count

    @classmethod
    def loads(cls, **kwargs):
        return cls(
            service_count=kwargs["serviceCount"],
            instance_count=kwargs["instanceCount"],
            load=kwargs["load"],
            mem=kwargs["mem"],
            cpu=kwargs["cpu"],
            status=kwargs["status"],
            responsible_service_count=kwargs["responsibleServiceCount"],
            responsible_instance_count=kwargs["responsibleInstanceCount"],
        )
