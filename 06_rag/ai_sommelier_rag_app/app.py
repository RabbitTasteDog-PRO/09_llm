# import streamlit as st
# import subprocess
# import sys

# st.title("RAG Application")

# if st.button("Run reg.py"):
#   try:
#     result = subprocess.run(
#       [sys.executable, "reg.py"],
#       capture_output=True,
#       text=True,
#       timeout=30
#     )
#     st.success("✅ Execution completed")
#     if result.stdout:
#       st.text_area("Output:", result.stdout, height=300)
#     if result.stderr:
#       st.error("Errors:")
#       st.text_area("Error details:", result.stderr, height=200)
#   except subprocess.TimeoutExpired:
#     st.error("❌ Execution timeout")
#   except Exception as e:
#     st.error(f"❌ Error: {str(e)}")

"""
Streamlit으로 실행하는 파일
[참고사항]
Streamlit은 사용자가 화면(위젯)을 조작하게되면
해당 파일(app.py)을 다시 실행한다
"""

# 파이썬 터미널에 오류를 출력할수있는 lib
import logging
from langsmith import expect
import streamlit as st
from rag import (
    # 사용자 정의 예외
    SommelierConfigurationError,
    # 이미지 와인추천 제안
    ai_sommelier_rag,
    # 이미지 검사
    validate_public_image_url,
)

import streamlit as st

# 개발자가 보기 위한 로그를 출력하는 객체 생성
logger = logging.getLogger(__name__)

# 브라우저 탭의 정보들
st.set_page_config(
    # 제목
    page_title="AI Wine Sommelier",
    # 아아콘
    page_icon="🍷",
    # 레이아웃
    layout="centered",
)

# 페이지 제목
st.title("🍷 AI Wine Sommelier")
# 화면에 보이는 글자
st.write("음식 이미지 URL을 입력하면 Wine Magazine 리뷰를 검색해 추천한다")
# 설명
st.info(
    "공개 HTTPS 이미지 URL만 사용한다. 제출한 URL은 음식 분석을 위해 OpenAI에 전달된다."
)

# st.form()은 여려 입력을 하나로 묶어서 제출할 수 있게게 하는 역할
with st.form(
    #
    key="image_url_form",
    # clear_on_submit : submit 이후 텍스트 클리어 여부
    clear_on_submit=False,
):
    image_url_input = st.text_input(
        "음식 이미지 URL",
        # 힌트
        placeholder="https://example.com/food.jpg",
        # 최대 문자열 길이
        max_chars=2048,
        help="로그인 없이 직접 접근 가능한 HTTPS 이미지 주소 입력",
    )
    # st.form_submit_button() : 해당 form의 모든 입력을 제출하는 역할
    submitted = st.form_submit_button(
        # 버튼 이름
        "와인추천받기",
        # 버튼이 보여질 스타일
        type="primary",
    )
if submitted:
    try:
        image_url = validate_public_image_url(image_url_input or "")
    except ValueError as e:
        st.warning(f"❌ Error: {str(e)}")
    else:
        st.image(
            image_url, caption="분석할 음식 이미지", use_container_width=True, width=520
        )

    st.subheader("AI Sommelier - 와인 추천")
    try:
        with st.spinner("음식과 관련된 와인 리뷰를 분석중입니다..."):
            st.write_stream(ai_sommelier_rag(image_url))
    # 설정 오류
    except SommelierConfigurationError as e:
        st.warning(f"❌ Error: {str(e)}")
    except Exception as e:
        logger.exception("AI sommelier Rag 실행 실패")
        st.error(f"추천 기능 수행 중 오류 발생\n오류타입:{type(e).__name__}")

        st.caption("API KEY 확인")
        st.caption("모델 접근 권한 확인")
        st.caption("Pinecone 인덱스, 차원수, namespace 확인")


# if submitted:
#     try:
#         # 입력을 먼저 검증해 잘못된 URL은 API 요청 전에 사용자에게 알린다.
#         image_url = validate_public_image_url(image_url_input)
#         st.image(image_url, caption="분석할 음식 이미지", use_container_width=True)

#         # 최종 추천은 chunk 단위로 생성되므로 화면에도 순서대로 출력한다.
#         st.subheader("와인 추천")
#         with st.spinner("음식 풍미와 와인 리뷰를 분석하고 있습니다..."):
#             recommendation = st.write_stream(ai_sommelier_rag(image_url))

#         # 이후 기능(다운로드·대화 이력 등)에서 재사용할 수 있도록 저장한다.
#         st.session_state["last_recommendation"] = recommendation

#     except SommelierConfigurationError as error:
#         st.error(f"설정 오류: {error}")
#     except ValueError as error:
#         st.warning(str(error))
#     except Exception:
#         # 상세 오류는 서버 로그에만 남기고, 화면에는 API key 등 민감 정보가 나오지 않게 한다.
#         logger.exception("AI sommelier recommendation failed")
#         st.error("추천을 생성하지 못했습니다. 이미지 URL과 API 설정을 확인한 뒤 다시 시도한다.")
