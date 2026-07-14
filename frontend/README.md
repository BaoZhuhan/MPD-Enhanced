# MPD Enhanced Frontend

面向 MPD-Enhanced 后端的音乐相似性分析界面。

## 本地运行

```bash
npm install
npm run dev
```

未设置后端地址时，上传音频后会进入演示模式，并返回一份与 `schemas.py` 字段一致的示例报告。

## 连接后端

在 `frontend/.env.local` 中设置：

```bash
VITE_API_URL=https://your-server.example.com/api/analyze
```

前端通过 `multipart/form-data` 发送 `POST` 请求，文件字段名为 `audio`。接口应返回 README 中的结构：

```json
{
  "success": true,
  "data": {
    "matches": [],
    "judgment": [],
    "analysis": "...",
    "risk_level": "Low | Medium | High"
  }
}
```

前端同时兼容 `schemas.py` 中较早的 `llm_judgment` 与 `llm_analysis` 字段名。
