import torch
import ray

print(f"PyTorch GPU: {torch.cuda.get_device_name(0)}")
ray.init()
print(f"Ray resources: {ray.cluster_resources()}")
