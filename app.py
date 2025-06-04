
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.title("홍합 발주서 자동 변환기 📦🧾")

# 파일 업로드
uploaded_file = st.file_uploader("주문내역 엑셀 파일을 업로드하세요 (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, dtype=str)

        # 필수 열 체크
        required_columns = ["수취인명", "수취인연락처1", "상세배송지", "상품주문번호", "판매자 내부코드1", "배송메세지"]
        if not all(col in df.columns for col in required_columns):
            st.error("필수 열이 누락되었습니다. 엑셀 파일을 확인해 주세요.")
        else:
            # 날짜
            today_str = datetime.today().strftime('%Y-%m-%d')

            # 24개 열 생성
            columns_24 = [
                "예약구분", "집하예정일", "보내는분 성명", "보내는분전화번호", "보내는분기타연락처",
                "보내는분우편번호", "보내는분주소(전체,분할)", "받는분성명", "받는분전화번호", "받는분기타연락처",
                "받는분우편번호", "받는분주소(전체,분할)", "운송장번호", "고객주문번호", "품목명", "박스수량",
                "박스타입", "기본운임", "배송메시지1", "배송메시지2", "운임구분", "베송메시지1", "배송메시지2", "운임구분"
            ]
            output_df = pd.DataFrame(index=range(len(df)), columns=columns_24)

            # 고정값 및 매핑
            output_df["보내는분 성명"] = "창원진동농협"
            output_df["보내는분전화번호"] = "055-271-2021"
            output_df["받는분성명"] = df["수취인명"]
            output_df["받는분전화번호"] = df["수취인연락처1"]
            output_df["받는분기타연락처"] = df["수취인연락처1"]
            output_df["받는분주소(전체,분할)"] = df["상세배송지"]
            output_df["고객주문번호"] = df["상품주문번호"]
            output_df["배송메시지1"] = df["배송메세지"]
            output_df["박스수량"] = "1"
            output_df["박스타입"] = "소"

            # 품목명 변환
            def convert_item(code):
                if code == "HONG_HAP_05K":
                    return "홍합 5KG"
                elif code == "HONG_HAP_03K":
                    return "홍합 3KG"
                return ""
            output_df["품목명"] = df["판매자 내부코드1"].apply(convert_item)

            # 엑셀 파일 생성
            towrite = BytesIO()
            output_df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)

            st.success("✅ 변환이 완료되었습니다. 아래에서 다운로드하세요.")
            st.download_button(
                label="📥 변환된 발주서 다운로드",
                data=towrite,
                file_name=f"{today_str}_홍합_발주서.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"⚠️ 오류가 발생했습니다: {e}")
else:
    st.info("좌측 또는 상단의 업로드 창에서 주문내역 엑셀 파일을 업로드해 주세요.")
