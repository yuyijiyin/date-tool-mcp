# date-tool-mcp

一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的最小可用 MCP 服务示例。
它向 AI 客户端暴露一个工具 `get_today()`，让模型能够获取真实的当前日期，而不是凭空猜测。

## 功能

| 工具名 | 描述 | 返回示例 |
| --- | --- | --- |
| `get_today` | 返回当前的年月日，格式 `YYYY-MM-DD` | `2026-11-26` |

## 环境要求

- Python 3.10 或更高版本
- `mcp >= 1.28.1, < 2`

> **为什么锁定 `< 2`**：mcp 2.x 起把 `FastMCP` 改名为 `MCPServer`（`mcp.server.fastmcp` 导入会直接报错）。
> 本项目基于 1.x 的 `FastMCP` 接口，因此 `requirements.txt` 里显式排除了 2.x。
> 若你已误装 2.x，执行 `pip install "mcp>=1.28.1,<2"` 降级即可。

## 安装

```bash
git clone https://github.com/yuyijiyin/date-tool-mcp.git
cd date-tool-mcp
pip install -r requirements.txt
```

## 本地运行

```bash
python server.py
```

服务使用 **stdio** 传输，启动后不会主动输出内容，而是等待客户端通过标准输入发送 MCP 请求，因此终端看起来像"卡住了"——这是正常的。

## 在客户端中配置

### Claude Desktop

编辑配置文件 `claude_desktop_config.json`：

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "date-tool-mcp": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

> 建议把 `command` 写成 Python 的绝对路径（例如 `C:\\Python313\\python.exe`），并把 `args` 写成 `server.py` 的绝对路径，避免客户端因工作目录不同而找不到文件。

修改后完全退出并重启 Claude Desktop，在对话中提问"今天几号"，模型就会调用该工具。

### ChatMCP

直接导入仓库根目录下的 `chatmcp.yaml` 即可，其中已包含运行命令与配置模板。

### Cursor / 其他 MCP 客户端

凡是支持 stdio 传输的 MCP 客户端，配置方式都与上面的 JSON 结构一致：`command` 指向 Python 解释器，`args` 指向 `server.py`。

## 项目结构

```
date-tool-mcp/
├── server.py          # MCP 服务实现，定义工具
├── requirements.txt   # Python 依赖
├── chatmcp.yaml       # ChatMCP 客户端配置描述文件
└── README.md
```

## 工作原理

1. `FastMCP("date-tool-mcp")` 创建服务实例；
2. `@mcp.tool()` 装饰器把普通 Python 函数注册为 MCP 工具，函数名即工具名，docstring 即工具描述（会作为提示交给模型，帮助它判断何时调用）；
3. `mcp.run()` 以 stdio 传输启动服务，与客户端收发 JSON-RPC 消息；
4. 客户端把工具列表注入模型上下文，模型判断需要日期时发起调用，服务返回结果。

## 二次开发

新增工具只需再加一个被 `@mcp.tool()` 装饰的函数：

```python
@mcp.tool()
def days_between(start: str, end: str) -> int:
    """计算两个日期（YYYY-MM-DD）之间相差的天数。"""
    ...
```

## License

MIT

## 作者

[yuyijiyin](https://github.com/yuyijiyin)
