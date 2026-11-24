import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="学生成绩数据看板", page_icon="📊", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "student_scores.csv")


def load_data():
    df = pd.read_csv(DATA_FILE)
    return df


df = load_data()

exam_order = ["第一次月考", "期中考试", "第二次月考"]
subject_list = ["语文", "数学", "英语", "物理", "化学"]
class_list = sorted(df["班级"].unique().tolist())

# ==================== 页面标题 ====================
st.markdown("""
<div style="text-align:center; padding: 10px 0; margin-bottom: 10px;">
    <h1 style="color:#1f4e79; margin-bottom:5px;">📊 学生成绩数据看板</h1>
    <p style="color:#666; font-size:14px;">某中学高二年级成绩分析</p>
</div>
""", unsafe_allow_html=True)

# ==================== 模块一：数据概览区（数据卡片） ====================
st.markdown("---")
st.subheader("📌 数据概览")

total_students = df["学号"].nunique()
total_records = len(df)
overall_avg = df["成绩"].mean()
pass_count = (df["成绩"] >= 60).sum()
pass_rate = pass_count / total_records * 100
excellent_count = (df["成绩"] >= 85).sum()
excellent_rate = excellent_count / total_records * 100
max_score = df["成绩"].max()
min_score = df["成绩"].min()

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("学生总数", f"{total_students} 人")
col2.metric("数据总条数", f"{total_records} 条")
col3.metric("总平均分", f"{overall_avg:.1f}")
col4.metric("及格率", f"{pass_rate:.1f}%")
col5.metric("优秀率(≥85)", f"{excellent_rate:.1f}%")
col6.metric("最高分 / 最低分", f"{max_score} / {min_score}")

# ==================== 模块二：维度统计区 ====================
st.markdown("---")
st.subheader("📊 维度统计")

left_col, right_col = st.columns(2)

# 柱状图：各班级各科平均分
with left_col:
    st.markdown("##### 各班级各科平均分对比")
    class_subject_avg = df.groupby(["班级", "科目"])["成绩"].mean().reset_index()
    fig_bar = px.bar(
        class_subject_avg,
        x="班级",
        y="成绩",
        color="科目",
        barmode="group",
        title="各班级各科平均分",
        labels={"成绩": "平均分", "班级": "班级"},
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=40, l=50, r=20),
        yaxis_range=[0, 100]
    )
    fig_bar.update_yaxes(gridcolor="rgba(200,200,200,0.3)")
    st.plotly_chart(fig_bar, use_container_width=True)

# 饼图：成绩等级分布
with right_col:
    st.markdown("##### 成绩等级分布")

    def grade_level(score):
        if score >= 85:
            return "优秀(≥85)"
        elif score >= 70:
            return "良好(70-84)"
        elif score >= 60:
            return "及格(60-69)"
        else:
            return "不及格(<60)"

    df["等级"] = df["成绩"].apply(grade_level)
    grade_counts = df["等级"].value_counts().reset_index()
    grade_counts.columns = ["等级", "人数"]
    grade_order = ["优秀(≥85)", "良好(70-84)", "及格(60-69)", "不及格(<60)"]
    grade_counts["等级"] = pd.Categorical(grade_counts["等级"], categories=grade_order, ordered=True)
    grade_counts = grade_counts.sort_values("等级")

    fig_pie = px.pie(
        grade_counts,
        values="人数",
        names="等级",
        title="成绩等级占比",
        color="等级",
        color_discrete_map={
            "优秀(≥85)": "#2ca02c",
            "良好(70-84)": "#1f77b4",
            "及格(60-69)": "#ff7f0e",
            "不及格(<60)": "#d62728"
        }
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        margin=dict(t=60, b=40, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ==================== 模块三：趋势分析区 ====================
st.markdown("---")
st.subheader("📈 趋势分析")

trend_left, trend_right = st.columns(2)

# 折线图：各次考试各科平均分趋势
with trend_left:
    st.markdown("##### 各次考试全年级平均分趋势")
    exam_subject_avg = df.groupby(["考试", "科目"])["成绩"].mean().reset_index()
    exam_subject_avg["考试"] = pd.Categorical(exam_subject_avg["考试"], categories=exam_order, ordered=True)
    exam_subject_avg = exam_subject_avg.sort_values("考试")

    fig_line = px.line(
        exam_subject_avg,
        x="考试",
        y="成绩",
        color="科目",
        markers=True,
        title="各次考试各科平均分变化趋势",
        labels={"成绩": "平均分", "考试": "考试"},
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    )
    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=40, l=50, r=20),
        yaxis_range=[50, 90]
    )
    fig_line.update_yaxes(gridcolor="rgba(200,200,200,0.3)")
    st.plotly_chart(fig_line, use_container_width=True)

# 折线图：各班级总平均分趋势
with trend_right:
    st.markdown("##### 各班级总平均分变化趋势")
    exam_class_avg = df.groupby(["考试", "班级"])["成绩"].mean().reset_index()
    exam_class_avg["考试"] = pd.Categorical(exam_class_avg["考试"], categories=exam_order, ordered=True)
    exam_class_avg = exam_class_avg.sort_values("考试")

    fig_line2 = px.line(
        exam_class_avg,
        x="考试",
        y="成绩",
        color="班级",
        markers=True,
        title="各班级总平均分变化趋势",
        labels={"成绩": "平均分", "考试": "考试"},
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    )
    fig_line2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=40, l=50, r=20),
        yaxis_range=[50, 90]
    )
    fig_line2.update_yaxes(gridcolor="rgba(200,200,200,0.3)")
    st.plotly_chart(fig_line2, use_container_width=True)

# ==================== 模块四：明细数据区 ====================
st.markdown("---")
st.subheader("📋 明细数据")

filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    sel_class = st.selectbox("选择班级", ["全部"] + class_list)
with filter_col2:
    sel_exam = st.selectbox("选择考试", ["全部"] + exam_order)
with filter_col3:
    sel_subject = st.selectbox("选择科目", ["全部"] + subject_list)

filtered_df = df.copy()
if sel_class != "全部":
    filtered_df = filtered_df[filtered_df["班级"] == sel_class]
if sel_exam != "全部":
    filtered_df = filtered_df[filtered_df["考试"] == sel_exam]
if sel_subject != "全部":
    filtered_df = filtered_df[filtered_df["科目"] == sel_subject]

st.markdown(f"共 **{len(filtered_df)}** 条数据")
st.dataframe(
    filtered_df.reset_index(drop=True),
    use_container_width=True,
    height=350
)

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#999; font-size:12px; padding:5px;">'
    '学生成绩数据看板 | 数据来源：模拟生成 | Streamlit + Pandas + Plotly'
    '</div>',
    unsafe_allow_html=True
)
