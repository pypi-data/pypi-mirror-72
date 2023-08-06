import logging

log = logging.getLogger(__name__)

# ==============================================================================

class Target:
    def __init__(self, ip, port, metrics_path,
                 p_instance, ecs_task_id, ecs_task_name, ecs_task_version,
                 ecs_container_id, ecs_cluster_name, ec2_instance_id):
        self.ip = ip
        self.port = port
        self.metrics_path = metrics_path
        self.p_instance = p_instance
        self.ecs_task_id = ecs_task_id
        self.ecs_task_name = ecs_task_name
        self.ecs_task_version = ecs_task_version
        self.ecs_container_id = ecs_container_id
        self.ecs_cluster_name = ecs_cluster_name
        self.ec2_instance_id = ec2_instance_id

# ==============================================================================

class TaskInfo:
    def __init__(self, task):
        self.task = task
        self.task_definition = None
        self.container_instance = None
        self.ec2_instance = None

    def valid(self):
        if 'FARGATE' in self.task_definition.get('requiresCompatibilities', ''):
            return self.task_definition
        else:
            return self.task_definition and self.container_instance and self.ec2_instance

# ==============================================================================

class FlipCache():

    def __init__(self):
        self.current_cache = {}
        self.next_cache = {}
        self.hits = 0
        self.misses = 0

    def flip(self):
        """Flips cache and resets hit / miss counters."""

        self.current_cache = self.next_cache
        self.next_cache = {}
        self.hits = 0
        self.misses = 0

    def get_dict(self, keys, fetcher) -> dict:
        """
        Gets a dict with values for all given keys. If an entry is not found in 
        the cache, it is fetched with the help of the given fetcher function.

        :param keys: All keys of the dict to retrieve.
        :param fetcher: Function to be used to fetch missing entries.
        """

        missing = []
        result = {}

        # Iterate through all given keys and check if they are available in the 
        # current cache. Count both hits and misses.
        for k in set(keys):
            if k in self.current_cache:
                result[k] = self.current_cache[k]
                self.hits += 1
            else:
                missing.append(k)
                self.misses += 1

        fetched = fetcher(missing) if missing else {}
        result.update(fetched)

        self.current_cache.update(fetched)
        self.next_cache.update(result)

        return result

    def get(self, key, fetcher) -> dict:
        """
        Gets a dict with a single value for the given key. If an entry is not 
        found in the cache, it is fetched with the help of the given 
        fetcher function.

        :param key: Key of entry to retrieve.
        :param fetcher: Function to be used to fetch missing entry.
        """
        if key in self.current_cache:
            result = self.current_cache[key]
            self.hits += 1
        else:
            self.misses += 1
            result = fetcher(key)
        if result:
            self.current_cache[key] = result
            self.next_cache[key] = result
        return result
