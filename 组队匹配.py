import streamlit as st
import json
import os
from datetime import datetime

# ========== 数据存储（JSON文件） ==========
DATA_FILE = "users.json"


def load_users():
    """从JSON文件读取用户数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_users(users):
    """保存用户数据到JSON文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def add_user(name, skills, goal, hours, contact):
    """添加新用户"""
    users = load_users()
    users.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "skills": ", ".join(skills),
        "goal": goal,
        "hours": hours,
        "contact": contact
    })
    save_users(users)
    return True


def ai_match(my_skills, all_users):
    """简单的匹配逻辑"""
    if not all_users:
        return "暂无其他用户数据"

    my_set = set(my_skills)

    scores = []
    for u in all_users:
        if "skills" not in u:
            continue
        user_skills = set(s.strip() for s in u["skills"].split(","))
        common = len(my_set & user_skills)
        scores.append((u, common))

    scores.sort(key=lambda x: x[1], reverse=True)

    result = "### 🎯 AI推荐结果\n\n"
    for i, (user, score) in enumerate(scores[:3]):
        if score > 0:
            result += "**{}. {}**（匹配度 {} 个共同技能）\n".format(i + 1, user['name'], score)
            result += "- 技能：{}\n".format(user['skills'])
            result += "- 目标：{}\n".format(user['goal'])
            result += "- 时间：{}小时/周\n".format(user['hours'])
            result += "- 联系方式：{}\n\n".format(user['contact'])

    if result == "### 🎯 AI推荐结果\n\n":
        result = "暂时没有找到匹配的队友，邀请更多同学来填写吧~"

    return result


# ========== Streamlit界面 ==========
st.set_page_config(page_title="竞赛组队匹配器", page_icon="🤝")

st.title("🤝 竞赛组队匹配器")
st.markdown("> AI智能匹配，帮你找到最合适的竞赛队友")
st.markdown("---")
st.info("👈 **点开左侧侧边栏**,填写你的信息后即可开始匹配")

with st.sidebar:
    st.header("📝 我的信息")
    name = st.text_input("昵称")
    skills = st.multiselect("技能", ["Python", "Java", "C/C++", "前端", "设计", "文案", "数据分析", "AI/ML", "演讲", "数学建模"])
    goal = st.selectbox("参赛目标", ["拿国奖", "拿省奖", "学技术", "认识朋友"])
    hours = st.slider("每周可投入时间（小时）", 0, 20, 5)
    contact = st.text_input("联系方式（微信号/QQ）", placeholder="方便队友联系你")

    if st.button("✅ 提交信息", type="primary"):
        if name and skills:
            add_user(name, skills, goal, hours, contact)
            st.success("✅ {}，你的信息已保存！".format(name))
            st.balloons()
        else:
            st.error("请填写昵称和技能")

tab1, tab2 = st.tabs(["📊 查看队友", "🔍 AI匹配"])

with tab1:
    st.subheader("📋 当前队友列表")
    users = load_users()
    if users:
        for u in users:
            with st.expander("👤 {}".format(u['name'])):
                st.write("**技能**：{}".format(u['skills']))
                st.write("**目标**：{}".format(u['goal']))
                st.write("**时间**：{}小时/周".format(u['hours']))
                st.write("**联系方式**：{}".format(u['contact']))
                st.write("**提交时间**：{}".format(u['timestamp']))
    else:
        st.info("暂无用户数据，请在左侧填写信息成为第一个用户~")

with tab2:
    st.subheader("🤖 AI智能匹配")
    st.markdown("根据你需要的技能，推荐最合适的队友")

    my_skills = st.multiselect("你的技能",
                               ["Python", "Java", "C/C++", "前端", "设计", "文案", "数据分析", "AI/ML", "演讲", "数学建模"])

    if st.button("开始匹配", type="primary"):
        if not my_skills:
            st.warning("请先选择你需要的技能")
        else:
            users = load_users()
            if users:
                with st.spinner("AI正在分析中..."):
                    result = ai_match(my_skills, users)
                st.markdown(result)
            else:
                st.warning("暂无用户数据，请先在左侧填写信息")

users = load_users()
st.markdown("---")
st.caption("📊 当前共有 {} 位同学在寻找队友".format(len(users)))