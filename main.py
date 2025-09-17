import paramiko
import traceback
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("云服务器自由操作助手")

# 服务器配置
HOST = "175.178.252.31"
USERNAME = "root"
PORT = 22

# -------------------------------
# 通用 SSH 执行函数
# -------------------------------
def ssh_execute(command: str, pem_path: str) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=HOST, port=PORT, username=USERNAME, key_filename=pem_path, timeout=10)
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        client.close()
        return f"✅ 命令执行完成\nstdout:\n{out}\nstderr:\n{err}"
    except Exception as e:
        tb = traceback.format_exc()
        return f"❌ 命令执行失败: {e}\n{tb}"

# -------------------------------
# 工具：测试连接
# -------------------------------
@mcp.tool()
def test_server_connection(pem_path: str) -> str:
    """
    使用 PEM 私钥测试连接服务器并返回系统信息
    """
    command = "whoami && uname -a && docker --version || echo 'docker not installed'"
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：执行任意 Linux 命令
# -------------------------------
@mcp.tool()
def run_remote_command(command: str, pem_path: str) -> str:
    """
    执行任意 Linux 命令
    """
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：读取远程文件
# -------------------------------
@mcp.tool()
def read_file(file_path: str, pem_path: str) -> str:
    """
    读取远程服务器文件内容
    """
    command = f"cat {file_path}"
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：写入文件（覆盖）
# -------------------------------
@mcp.tool()
def write_file(file_path: str, content: str, pem_path: str) -> str:
    """
    写入内容到远程文件（覆盖模式）
    """
    safe_content = content.replace('"', '\\"')
    command = f'echo "{safe_content}" > {file_path}'
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：追加文件
# -------------------------------
@mcp.tool()
def append_file(file_path: str, content: str, pem_path: str) -> str:
    """
    追加内容到远程文件
    """
    safe_content = content.replace('"', '\\"')
    command = f'echo "{safe_content}" >> {file_path}'
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：创建目录
# -------------------------------
@mcp.tool()
def make_directory(dir_path: str, pem_path: str) -> str:
    """
    创建远程目录
    """
    command = f"mkdir -p {dir_path}"
    return ssh_execute(command, pem_path)

# -------------------------------
# 工具：删除文件或目录
# -------------------------------
@mcp.tool()
def remove_path(path: str, pem_path: str) -> str:
    """
    删除远程文件或目录
    """
    command = f"rm -rf {path}"
    return ssh_execute(command, pem_path)

# -------------------------------
# 启动 MCP
# -------------------------------
if __name__ == "__main__":
    print("mcp 正在运行中（自由操作助手）")
    mcp.run()
