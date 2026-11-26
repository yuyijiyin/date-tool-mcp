"""date-tool-mcp —— 一个最小的 MCP 服务示例。

作用：通过 MCP 协议向支持 MCP 的 AI 客户端（如 Claude Desktop、ChatMCP）
暴露一个工具 get_today()，返回当前日期。

运行方式：python server.py（使用 stdio 传输，供客户端以子进程方式调用）
"""

from datetime import datetime

from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务实例，名字会展示在客户端里
mcp = FastMCP("date-tool-mcp")


@mcp.tool()
def get_today() -> str:
    """返回当前的年月日，格式 YYYY-MM-DD。"""
    # datetime.now() 取本机当前时间，strftime 格式化为 YYYY-MM-DD
    return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    # 默认使用 stdio 传输：客户端启动本进程，通过标准输入输出通信
    mcp.run()
