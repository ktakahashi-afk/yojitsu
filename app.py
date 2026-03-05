import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="栃木JIMINIE倶楽部 多機能PL分析", layout="wide")
st.title("📊 栃木JIMINIE倶楽部 経営分析ダッシュボード")

# タブの作成
tab1, tab2, tab3 = st.tabs(["💰 PL決算・比較", "🏨 宿泊統計・属性", "👥 人件費算出"])

# --- Tab 1: PL分析 (以前の機能) ---
with tab1:
    st.subheader("月次決算入力")
    # ここに以前のPL入力ロジックが入ります（簡略化して表示）
    st.info("以前のPL入力・比較画面です。")

# --- Tab 2: 宿泊統計・属性 ---
with tab2:
    st.header("🏨 宿泊ターゲット分析")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("宿泊目標管理")
        target = st.number_input("年間/月間 目標数", value=1000)
        actual = st.number_input("実績数", value=850)
        st.metric("達成率", f"{actual/target*100:.1f}%", f"{actual-target}")
        
    with c2:
        st.subheader("居住地・属性比率")
        # データの仮入力
        data = pd.DataFrame({
            "区分": ["県内(栃木)", "県外(近隣)", "県外(遠方)", "団体/学校"],
            "人数": [400, 250, 100, 250]
        })
        fig = px.pie(data, values='人数', names='区分', hole=0.3)
        st.plotly_chart(fig)

# --- Tab 3: 人件費算出 ---
with tab3:
    st.header("👥 人件費シミュレーション")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("アルバイト・パート")
        hr_wage = st.number_input("平均時給(円)", value=1000)
        total_hrs = st.number_input("総労働時間(h)", value=500)
        part_time_cost = hr_wage * total_hrs
        st.metric("算出したバイト代", f"¥{part_time_cost:,.0f}")

    with col_b:
        st.subheader("正社員・諸手当")
        salary = st.number_input("基本給合計", value=1000000)
        ins = st.number_input("法定福利費(目安15%)", value=int(salary * 0.15))
        st.metric("正社員コスト合計", f"¥{salary + ins:,.0f}")
