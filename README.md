# Chatroom聊天室系統
一個模擬 LINE / IG 私訊功能的聊天室系統，具備 JWT 登入驗證、即時通訊（Socket.IO）、好友管理與檔案上傳功能，採用 FastAPI + MySQL + Vue 架構開發。

## 🧰 使用技術

| 分類 | 技術 | 說明 |
|------|------|------|
| **前端** | Vue.js | 使用第三方模板並進行自訂調整 |
| **後端框架** | FastAPI | 提供 RESTful API 與 WebSocket 支援 |
|  | Socket.IO | 處理即時通訊（聊天室訊息） |
|  | Uvicorn | ASGI server，負責啟動與管理應用 |
| **資料庫** | MySQL | 作為主要資料儲存後端 |
| **ORM** | SQLAlchemy | 負責資料模型與資料庫互動 |
| **認證機制** | JWT | 採用 JSON Web Token 實現使用者驗證與授權 |
| **架構模式** | MVC | 採用 Model-View-Controller 模式管理專案結構 |

## ✨ 主要功能

- 使用者註冊 / 登入（JWT 驗證機制）
- 好友系統（搜尋、加好友、好友列表）
- 一對一即時聊天（Socket.IO）
- 上傳圖片 / 檔案
- 編輯個人資料（暱稱、大頭貼、個人狀態）

## 🗂️ API 文件

### 🔐 認證 Auth
| Method | Endpoint | 說明 |
|------|------|------|
| POST | `/auth/register` | 使用者註冊 |
| POST | `/auth/token` | 使用者登入，取得 Access Token |
| POST | `/auth/logout` | 使用者登出 |
| GET  | `/auth/users/me/` | 取得當前使用者資訊 |

### 👤 使用者 Users

| Method | Endpoint | 說明 |
|------|------|------|
| GET    | `/user/me` | 取得當前使用者資料 |
| GET    | `/user/{user_id}` | 以 ID 取得使用者資料 |
| PATCH  | `/user/{user_id}` | 更新使用者資料 |
| DELETE | `/user/{user_id}` | 刪除使用者資料 |

### 👥 好友 Friends
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET    | `/friends/` | 取得好友列表 |
| DELETE | `/friends/` | 刪除好友 |
| POST   | `/friends/request` | 傳送好友請求 |
| GET    | `/friends/requests/pending` | 取得收到的好友請求 |
| GET    | `/friends/requests/sent` | 取得已傳送的好友請求 |
| POST   | `/friends/requests/accepted` | 接受好友請求 |
| DELETE | `/friends/requests/reject` | 拒絕好友請求 |
| GET    | `/friends/search` | 透過 email 搜尋使用者 |

### 💬 聊天室 Chatrooms
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET  | `/chatrooms/` | 取得聊天室列表 |
| POST | `/chatrooms/` | 建立新的聊天室 |
| GET  | `/chatrooms/{chatroom_id}` | 取得單一聊天室資料 |
| GET  | `/chatrooms/{chatroom_id}/messages` | 取得聊天室訊息 |
| POST | `/chatrooms/{chatroom_id}/message` | 傳送訊息至聊天室 |

### 📁 上傳 Uploads
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/upload/upload-avatar` | 上傳使用者頭像 |
| POST | `/upload/upload-message-file` | 上傳聊天室檔案 |


## 🗃️ 資料庫設計

### 📌 users – 使用者資料表
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| user_id | INT (PK) | 使用者唯一 ID，自動遞增 |
| username | VARCHAR(32) | 使用者名稱，需唯一 |
| email | VARCHAR(256) | 使用者 Email，可選填，需唯一 |
| hashed_password | VARCHAR(256) | 加密後的密碼 |
| nickname | VARCHAR(32) | 顯示暱稱 |
| avatar_url | VARCHAR(256) | 頭像圖片 URL |
| status | VARCHAR(256) | 使用者狀態文字 |
| created_at | TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | 更新時間（自動更新） |

### 📌 friends – 好友關係表
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| user_id | INT (PK, FK) | 發出請求者的使用者 ID |
| friend_id | INT (PK, FK) | 被加為好友的使用者 ID |
| status | VARCHAR(32) | 關係狀態（`pending` / `accepted` / `rejected` / `deleted`） |
| created_at | TIMESTAMP | 發起請求時間 |

📎 使用組合主鍵 (user_id, friend_id) 並加上雙向外鍵關聯 ON DELETE CASCADE。

### 📌 chatrooms – 聊天室資料表
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| chatroom_id | BINARY(16) (PK) | 聊天室唯一識別碼（UUID 格式） |
| chatroom_name | VARCHAR(32) | 聊天室名稱 |
| created_at | TIMESTAMP | 建立時間 |

### 📌 participants – 聊天室參與者表
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| chatroom_id | BINARY(16) (PK, FK) | 對應聊天室 |
| user_id | INT (PK, FK) | 參與的使用者 ID |

>📎 用來建立使用者與聊天室的多對多關聯。

### 📌 messages – 聊天訊息表
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| message_id | INT (PK) | 訊息唯一 ID，自動遞增 |
| chatroom_id | BINARY(16) (FK) | 所屬聊天室 |
| sender_id | INT (FK) | 發送者的使用者 ID |
| content | TEXT | 訊息內容（文字） |
| message_type | ENUM | 訊息類型（`text` / `image` / `audio` / `file` / `video`） |
| media_url | VARCHAR(255) | 若為媒體訊息，對應檔案 URL |
| read_status | ENUM | 訊息狀態（`unread` / `delivered` / `read`） |
| timestamp | TIMESTAMP | 發送時間 |
---

### 💡 設計說明
>1. 使用 UUID (BINARY 16) 為聊天室主鍵。
>2. 所有關聯表皆使用 ON DELETE CASCADE 確保資料完整性。
>3. 好友關係用 status 控制流程，支援好友請求機制。


## 🗂️ 專案結構（後端）

```
.
├── backend
|   ├── main.py                  # 專案入口，啟動 FastAPI 應用
|   ├── app/                     # 核心應用邏輯（後端架構）
|   │   ├── controllers/         # API 控制器，處理路由請求邏輯
|   │   ├── db/                  # 資料庫連線與初始化
|   │   │   └── context.py       # DB 連線設定與初始化函式
|   │   ├── models/              # 資料結構與定義
|   │   │   ├── db.py            # SQLAlchemy 模型
|   │   │   └── dto.py           # Pydantic 資料傳輸物件 (DTO)
|   │   ├── repos/               # 資料操作層（Repository Pattern）
|   │   ├── services/            # 商業邏輯與處理（Service Layer）
|   │   └── sockets/             # Socket.IO 實作與事件處理
|   ├── static/                  # 上傳檔案與靜態資源（如頭像、媒體）
|   ├── utils/                   # 共用工具函式
|   ├── constants.py             # 放置全域常數，便於統一管理與重複使用
|   ├── log_config.py            # 設定 logging 格式與等級，統一控制專案的日誌輸出行為
|   ├── Dockerfile               
|   └── init_db.py            
├── frontend/                    # 前端 Vue.js 專案
└── docker-compose.yml
```
📌 採用 MVC + 分層架構：

>Model：models/ 定義 DB 與 DTO
>
>View/Controller：controllers/ 定義 API 路由
>
>Service：services/ 管理邏輯流程
>
>Repository：repos/ 封裝資料操作邏輯
>
>Socket：sockets/ 處理即時聊天室功能


## 📌 專案特色與挑戰

- 自行設計資料庫架構與資料關聯（使用 MySQL）
- 後端 RESTful API 設計與實作
- 使用 JWT 實作登入驗證與身分驗證機制
- 整合 Socket.IO 處理前後端即時訊息傳遞、連線管理與錯誤處理


## 🔮 未來規劃

- 部署至 AWS（使用 EC2、RDS、S3 儲存上傳檔案）
- 使用 Docker 建立開發與生產環境一致性
- 使用 Nginx 作為反向代理伺服器


## 🧑‍💻 開發者資訊

此專案由本人獨立開發完成，主要負責項目如下：

- 後端架構設計與實作（FastAPI + Socket.IO）
- 資料庫設計與測試（MySQL）
- 前端架構調整與串接（基於公開模板進行客製化）