"""
NVIDIA Driver 560.35.03 Bug Mitigation Module.

Prevents kernel NULL pointer dereference crashes triggered by specific CUDA
memory management operations (pinned memory, nv_alloc_system_pages).

Import this module FIRST — before any other module that initializes CUDA.
"""

import os

# ── Phase 0: Set environment variables BEFORE torch/cuda import ──

# 1. Use expandable segments allocator — avoids fragmented pinned allocations
#    that trigger the nv_alloc_system_pages bug path
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

# 2. Lazy CUDA module loading — reduces driver interaction at startup
os.environ.setdefault("CUDA_MODULE_LOADING", "LAZY")

# 3. Avoid caching allocator which can hold stale pinned-memory references
#    across model reloads
_alloc_conf = os.environ["PYTORCH_CUDA_ALLOC_CONF"]
if "backend:native" not in _alloc_conf:
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = _alloc_conf + ",backend:native"


# ── Phase 1: Monkey-patch pin_memory defaults (after torch is importable) ──

def _patch_pin_memory():
    """Disable pin_memory by default in DataLoader to avoid nv_alloc bug path."""
    try:
        import torch.utils.data
        _orig_init = torch.utils.data.DataLoader.__init__

        def _safe_init(self, *args, **kwargs):
            if "pin_memory" not in kwargs:
                kwargs["pin_memory"] = False
            elif kwargs["pin_memory"] is True:
                print("[Safety] pin_memory=True detected — forcing False "
                      "to avoid NVIDIA driver 560.35.03 bug")
                kwargs["pin_memory"] = False
            _orig_init(self, *args, **kwargs)

        torch.utils.data.DataLoader.__init__ = _safe_init
        print("[Safety] DataLoader pin_memory default → False")
    except Exception as e:
        print(f"[Safety] Failed to patch DataLoader: {e}")


# ── Phase 2: GPU memory safety ──

def limit_gpu_memory(fraction=0.8):
    """
    Limit per-process GPU memory to avoid triggering driver OOM paths.

    Call before loading any models. Default 80% leaves headroom for
    driver-internal allocations (nv_alloc_system_pages).
    """
    try:
        import torch
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                total = torch.cuda.get_device_properties(i).total_memory
                limit = int(total * fraction)
                torch.cuda.set_per_process_memory_fraction(fraction, i)
                print(f"[Safety] GPU {i} memory limit: "
                      f"{limit // (1024**3)}GB / "
                      f"{total // (1024**3)}GB ({fraction*100:.0f}%)")
    except Exception as e:
        print(f"[Safety] Failed to set memory limit: {e}")


def sync_cuda():
    """
    Flush CUDA operations after each heavy model inference.
    Prevents accumulation of async driver commands that can
    trigger the nv_get_kern_phys_address crash.
    """
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.synchronize()
    except Exception:
        pass


# ── Phase 3: Auto-apply patches on import ──

_patch_pin_memory()
