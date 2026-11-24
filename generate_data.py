import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

names_male = ["张伟", "王强", "李磊", "刘洋", "陈明", "杨帆", "赵鑫", "黄志远", "周杰", "吴昊",
              "徐浩", "孙鹏", "马超", "朱俊", "胡涛", "郭靖", "林峰", "何勇", "高翔", "罗辉"]
names_female = ["王芳", "李娜", "张敏", "刘婷", "陈静", "杨雪", "赵倩", "黄丽", "周颖", "吴娟",
                "徐琳", "孙莉", "苗苗", "朱颖", "胡悦", "郭蓉", "林玲", "何欣", "高雅", "罗茜"]

classes = ["高二2025班", "高二2026班", "高二2027班", "高二2028班"]
subjects = ["语文", "数学", "英语", "物理", "化学"]
exams = ["第一次月考", "期中考试", "第二次月考"]

students = []
sid = 20230001
for cls in classes:
    for _ in range(12):
        is_male = random.random() > 0.45
        if is_male:
            name = random.choice(names_male)
            gender = "男"
        else:
            name = random.choice(names_female)
            gender = "女"
        students.append({"学号": f"{sid}", "姓名": name, "性别": gender, "班级": cls})
        sid += 1

rows = []
for stu in students:
    base_ability = np.random.normal(72, 10)
    for exam in exams:
        exam_shift = {"第一次月考": -3, "期中考试": 0, "第二次月考": 4}[exam]
        for subj in subjects:
            subj_bonus = {"语文": 2, "数学": -1, "英语": 1, "物理": -2, "化学": 0}[subj]
            score = base_ability + exam_shift + subj_bonus + np.random.normal(0, 6)
            score = int(np.clip(round(score), 15, 100))
            rows.append({
                "学号": stu["学号"],
                "姓名": stu["姓名"],
                "性别": stu["性别"],
                "班级": stu["班级"],
                "考试": exam,
                "科目": subj,
                "成绩": score
            })

df = pd.DataFrame(rows)
df.to_csv("student_scores.csv", index=False, encoding="utf-8-sig")
print(f"数据生成完成，共 {len(df)} 条记录，{len(students)} 名学生")
print(f"班级分布：{df['班级'].value_counts().to_dict()}")
print(f"考试次数：{df['考试'].unique().tolist()}")
print(f"科目：{df['科目'].unique().tolist()}")
