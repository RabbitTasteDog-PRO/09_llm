"""두 수를 더하는 Tool을 제공하는 MCP Server"""

from mcp.server import MCPServer

# "math_tools"라는 이름을 갖는 MCPServer 인스턴스를 생성
# - Host(AI 클라이언트 == GPT, claude code, Codex, pycharm등 ) 연결 시
#   노출되는 Tools, Resource, Prompt를 등록하고 관리하는 역할
mcp = MCPServer("math_tools")

print("hello world")


# 해당 함수를 MCP Tool 규격으로 자동 변환
# () 내 "도구명"을 적지 않으면 함수명이 도구명이 된다
@mcp.tool()
def add(a: float, b: float) -> float:
    """두 숫자 a와b를 받아 두 수를 더한 후 곱하기 10 이후 반환한다"""
    return (a + b) * 10

@mcp.tool()
def minus(a: float, b: float) -> float:
    """두 숫자 a와b를 받아 두 수를 뺀 뒤  제곻 이후 반환한다"""
    return (a - b) ** 2


if __name__ == "__main__":

    try:
        mcp.run(
            transport="streamable-http",
            # 서버 host 주소
            host="127.0.0.1",
            # 웹 요청 시 프로그램 구분 번호
            port=8001,
            streamable_http_path="/mcp",
        )

    except KeyboardInterrupt:
        # SDK가 출력하는 메세지 숨기기
        pass
    except Exception as e:
        print(f"Error occurred: {e}")
