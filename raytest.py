import ray

ray.init()
resources = ray.available_resources()
print("Available Resources:", resources)
