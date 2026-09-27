# LLM_SETUP.md
## LLM接口配置说明
项目使用DeepSeek大模型，采用OpenAI兼容协议，无需修改代码即可切换模型。
### 环境变量配置
| 环境变量 | 说明 | 示例 |
|---|---|---|
| LLM_BASE_URL | OpenAI兼容接口地址 | https://api.deepseek.com/v1 |
| LLM_MODEL | 模型名称 | deepseek-flash |
| LLM_API_KEY | DeepSeek密钥 | （不写入代码，外部环境注入） |

### 核心约束（满足API_CONTRACT.md 7.4）
1. 切换DeepSeek仅修改环境变量，**业务代码无需改动**。
2. 完整的prompt、用户提问、模型返回内容全部可日志输出，评审方可以查看完整请求。
3. 当不存在LLM_API_KEY环境变量时，服务**正常启动，自动降级**，不会崩溃。
4. API密钥不会写入代码、不会入库，仅从环境变量读取。

### 预检操作
使用官方预检工具执行：
```bash
python eval/llm_gateway.py preflight