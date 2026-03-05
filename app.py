import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="栃木JIMINIE倶楽部 PL分析システム", layout="wide")

st.title("📊 栃木JIMINIE倶楽部 自然の家みかも PL分析")
st.caption("前年比較・月次推移・AI自動総括システム")

# --- データ構造の定義 ---
categories = {
    "売上高": ["宿泊売上", "食事売上", "利用料売上", "物販売上", "業務委託売上", "手数料売上", "ｲﾍﾞﾝﾄ売上", "教育売上", "その他売上"],
    "売上原価": ["仕入高（食材）", "仕入高（物販）", "仕入高（外注費）", "仕入高（通信費）", "仕入高（ﾚﾝﾀﾙ）", "仕入高（その他）"],
    "販売管理費": ["給与　社員", "給与　ｱﾙﾊﾞｲﾄ", "法定福利費", "福利厚生費", "広告宣伝費", "水道光熱費", "修繕費", "消耗品費", "雑費"] # 一部抜粋。全項目追加可能
}

# --- サイドバー：対象月の選択 ---
st.sidebar.header("設定")
target_month = st.sidebar.selectbox("対象月を選択", [f"{i}月" for i in range(1, 13)])

# --- メインコンテンツ：データ入力 ---
st.subheader(f"📅 {target_month} 実績入力・比較")

# サンプルデータ（実際はDBやCSVから読み込み）
def create_df():
    all_items = []
    for cat, items in categories.items():
        for item in items:
            all_items.append({"大項目": cat, "勘定科目": item, "前年実績": 0, "当年実績": 0})
    return pd.DataFrame(all_items)

if 'df' not in st.session_state:
    st.session_state.df = create_df()

# 編集可能なテーブル
edited_df = st.data_editor(
    st.session_state.df,
    column_config={
        "前年実績": st.column_config.NumberColumn(format="¥%d"),
        "当年実績": st.column_config.NumberColumn(format="¥%d"),
    },
    disabled=["大項目", "勘定科目"],
    hide_index=True,
    use_container_width=True
)

# --- 計算ロジック ---
edited_df["増減"] = edited_df["当年実績"] - edited_df["前年実績"]
edited_df["増減率(%)"] = (edited_df["増減"] / edited_df["前年実績"].replace(0, np.nan) * 100).fillna(0)

# --- 集計セクション ---
st.divider()
col1, col2, col3 = st.columns(3)

sales_now = edited_df[edited_df["大項目"]=="売上高"]["当年実績"].sum()
cost_now = edited_df[edited_df["大項目"]=="売上原価"]["当年実績"].sum()
admin_now = edited_df[edited_df["大項目"]=="販売管理費"]["当年実績"].sum()
profit_now = sales_now - cost_now - admin_now

col1.metric("当期売上高合計", f"¥{sales_now:,.0f}")
col2.metric("当期営業利益", f"¥{profit_now:,.0f}")
col3.metric("原価率", f"{(cost_now/sales_now*100) if sales_now !=0 else 0:.1f}%")

# --- AI分析セクション ---
st.divider()
st.subheader("🤖 AIによる今月の総括分析")

if st.button("AI分析を実行する"):
    with st.spinner('データを解析中...'):
        # ここでGemini APIにデータを渡す処理をシミュレーション
        # 実際には edited_df を文字列にしてAPIへ送信します
        top_increase = edited_df.sort_values("増減", ascending=False).iloc[0]
        
        analysis_text = f"""
        **【今月の概況】**
        今月の売上高は前年比で改善傾向にあります。特に「{top_increase['勘定科目']}」が
        前年より¥{top_increase['増減']:,.0f}増加しており、収益の柱となっています。
        
        **【懸念点とアドバイス】**
        一方で、販売管理費における水道光熱費等の固定費推移を注視する必要があります。
        来月はｲﾍﾞﾝﾄ売上の反動減が予想されるため、消耗品費の抑制を推奨します。
        """
        st.info(analysis_text)

# --- 保存機能 ---
if st.sidebar.button("データを保存する"):
    edited_df.to_csv(f"PL_data_{target_month}.csv", index=False)
    st.sidebar.success("CSVに保存されました！")
