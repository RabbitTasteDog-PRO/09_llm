"""
비트코인(BTC) 최근 가격 데이터를 가져와 시각화하는 스크립트
데이터 출처: CoinGecko 공개 API (별도의 API 키 불필요)

[필요 라이브러리 설치 방법]
터미널에서 아래 명령어를 실행하세요:

    pip install requests pandas matplotlib

--------------------------------------------------------
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetch_bitcoin_price(days: int = 30, vs_currency: str = "usd") -> pd.DataFrame:
    """
    CoinGecko API를 통해 최근 N일간의 비트코인 가격 데이터를 가져온다.

    Parameters
    ----------
    days : int
        조회할 기간(일). 예: 7, 30, 90, 365
    vs_currency : str
        기준 통화. 예: "usd", "krw"

    Returns
    -------
    pd.DataFrame
        timestamp(datetime), price 컬럼을 가진 데이터프레임
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    data = response.json()

    # data["prices"] 형태: [[timestamp(ms), price], [timestamp(ms), price], ...]
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df


def plot_bitcoin_price(df: pd.DataFrame, vs_currency: str = "usd", days: int = 30):
    """비트코인 가격 데이터를 라인 차트로 시각화한다."""
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["price"], color="#f2a900", linewidth=1.8)

    plt.title(f"Bitcoin (BTC) Price - Last {days} Days", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel(f"Price ({vs_currency.upper()})")
    plt.grid(True, linestyle="--", alpha=0.5)

    # 날짜 축 포맷 설정
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.xticks(rotation=45)

    plt.tight_layout()

    # 이미지 파일로 저장
    output_path = "bitcoin_price_chart.png"
    plt.savefig(output_path, dpi=150)
    print(f"차트가 저장되었습니다: {output_path}")

    plt.show()


if __name__ == "__main__":
    DAYS = 30            # 조회 기간 (필요에 따라 변경: 1, 7, 30, 90, 365 등)
    VS_CURRENCY = "usd"  # 기준 통화 (예: "usd", "krw")

    print(f"최근 {DAYS}일간의 비트코인 가격 데이터를 가져오는 중...")
    df = fetch_bitcoin_price(days=DAYS, vs_currency=VS_CURRENCY)

    print(df.tail())  # 최근 데이터 미리보기

    plot_bitcoin_price(df, vs_currency=VS_CURRENCY, days=DAYS)
