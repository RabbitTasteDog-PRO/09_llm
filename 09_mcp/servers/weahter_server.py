from mcp.server import MCPServer
import os

import requests
from dotenv import find_dotenv, load_dotenv
from mcp.server import MCPServer

# "weather_tools"라는 이름을 갖는 MCPServer 인스턴스를 생성
# - Host(AI 클라이언트 == GPT, claude code, Codex, pycharm등 ) 연결 시
#   노출되는 Tools, Resource, Prompt를 등록하고 관리하는 역할
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path, override=False)
mcp = MCPServer("weather-tools")


@mcp.tool()
def current_weather(city: str) -> dict[str, str | float | int]:
    """도시 이름으로 OpenWeatherMap의 현재 날씨를 조회한다."""
    if not city.strip():
        raise ValueError("city에는 비어 있지 않은 도시 이름이 필요하다.")

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY 환경 변수가 필요하다.")

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city.strip(),
                "appid": api_key,
                "units": "metric",
                "lang": "kr",
            },
            timeout=10,
            allow_redirects=False,
        )
        if not 200 <= response.status_code < 300:
            raise ValueError("unexpected weather API status")

        payload = response.json()
        result = {
            "city": payload["name"],
            "temperature_c": payload["main"]["temp"],
            "humidity_percent": payload["main"]["humidity"],
            "description": payload["weather"][0]["description"],
        }
    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        # 공급자 오류 URL에는 API key가 포함될 수 있으므로 외부 예외 원문을 노출하지 않는다.
        raise RuntimeError("날씨 API 요청에 실패했다.") from None

    return result


if __name__ == "__main__":

    try:
        mcp.run(
            transport="streamable-http",
            # 서버 host 주소
            host="127.0.0.1",
            # 웹 요청 시 프로그램 구분 번호
            port=8000,
            streamable_http_path="/mcp",
        )

    except KeyboardInterrupt:
        # SDK가 출력하는 메세지 숨기기
        pass
    except Exception as e:
        print(f"Error occurred: {e}")
