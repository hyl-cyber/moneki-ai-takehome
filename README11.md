# Moneki.ai 连锁餐饮经营看板 & 混合问答AI助手
## 项目简介
本项目为连锁餐饮门店经营数据看板 + RAG混合问答助手。
系统支持两类查询：
1. 文档查询：查阅公司制度、口径手册、通知文档（知识库md/txt/html）
2. 数据查询：从SQLite POS业务库读取营业额、销量等经营指标
3. 混合问答：同时读取数据库数据 + 引用知识库文档，给出带引用的答案

> 系统固定基准日期：2026-09-01

## 技术选型
- 后端：Python + FastAPI
- 检索：自研BM25检索引擎，无LangChain/Chroma，轻量化RAG
- 规划器：Planner意图路由模块，区分文档查询/数据查询/混合查询
- 数据库：SQLite(pos.db)，存储门店POS销售数据
- 前端看板：Streamlit（经营指标看板+AI问答对话框）
- LLM：DeepSeek，使用OpenAI兼容接口，环境变量配置，不硬编码密钥

## 项目目录说明
moneki-ai-takehome/
├── data/ # POS 原始数据 pos.db/csv
├── knowledge_base/ # 35 份企业内部知识库文档
├── starter/ # RAG 问答服务主体代码
├── eval/ # 评测脚本与公开题库
└── docs/ # API 契约文档

## 快速启动（干净环境复现）
### 前置依赖
Python3.12

1. 创建虚拟环境并安装依赖
`cd starter
python3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt`
2. 重建清洗数据表、构建检索索引
`make rebuild`
3. 启动后端问答服务
`make run`
服务地址：http://127.0.0.1:8001
4. 启动 Streamlit 经营看板
`streamlit run dashboard.py`
5. 执行评测脚本（根目录新开终端）
`python eval/run_eval.py --base-url http://localhost:8001 --questions eval/public_questions.jsonl`

**架构说明**
架构简述（面试口述，可手绘图：用户→Streamlit 看板→FastAPI 服务→Planner 意图规划器）
1. Planner：意图识别，判断问题类型（doc 仅文档 /data 仅数据库 /hybrid 混合）
2. 开关 enable_hybrid：布尔开关，关闭时强制全部问题走文档检索，禁用 SQL 查询；开启启用混合问答
3. Retriever：BM25 文档检索，内置打分、元数据过滤、降噪权重
4. 数据层：SQLite pos 数据库，严格按照知识库口径做数据清洗、指标计算
5. LLM 网关：OpenAI 兼容协议调用 DeepSeek，无密钥时自动降级，不影响服务启动

**口径与歧义取舍**
1. 营业额口径：严格参考知识库口径手册，退款订单不计入营业额，脏数据按文档规则过滤
2. 文档新旧冲突：优先采用生效时间靠后的文档；历史回溯类问题，使用当时生效版本
3. 数据 / 文档数字冲突：按知识库口径手册的冲突处理规则执行
4. 无来源信息：如实返回不知道，禁止编造数字、编造文档引用

**功能清单**
✅ 第一关：指标 API /api/metrics/summary / /api/metrics/daily + Streamlit 数据看板（日期门店筛选、营业额趋势、Top 商品、数据质量统计）
✅ 第二关：修复原有 RAG 检索缺陷，增加意图路由开关，区分文档 / 数据查询
✅ 第三关：混合问答链路，支持数据证据 data_evidence、文档引用 citations，支持多轮会话追问
🟡 待优化：年月时间解析（yyyy-MM 简写解析 bug，写在 DEBUG_LOG）