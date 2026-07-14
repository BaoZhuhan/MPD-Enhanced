#!/bin/bash
# MPD-Enhanced 运行脚本
# 用法: bash run.sh <audio_file.mp3/wav>

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 激活 conda 环境
source /opt/anaconda3/bin/activate mpd

# 配置 hf-mirror（可选，加快 HuggingFace 模型下载）
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_XET=1

# 运行推理
if [ $# -eq 0 ]; then
    echo "用法: bash run.sh <audio_file>"
    echo ""
    echo "示例:"
    echo "  bash run.sh song.mp3"
    echo "  bash run.sh ml_models/Beat-Transformer/test_audio/*.mp3"
    exit 1
fi

python3 inference.py "$@"
