from flask import Flask, request, render_template, Response, session, redirect, url_for
app = Flask(__name__)
app.secret_key = 'LightHopeNB'  # 一定要设置！
import sqlite3
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    # 初始化 database.db
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            school TEXT NOT NULL,
            email TEXT NOT NULL,
            competition TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enterprise_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            email TEXT NOT NULL,
            problem TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            leader TEXT NOT NULL,
            email TEXT NOT NULL,
            description TEXT,
            filename TEXT
        )
    ''')

    conn.commit()
    conn.close()

    # ✅ 新增：初始化 discussion.db
    conn_discuss = sqlite3.connect('discussion.db')
    cursor_discuss = conn_discuss.cursor()

    cursor_discuss.execute('''
        CREATE TABLE IF NOT EXISTS discussions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn_discuss.commit()
    conn_discuss.close()
@app.route('/')
def home():
    return render_template('overview.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/version')
def version():
    return render_template('version.html')

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        school = request.form.get('school')
        email = request.form.get('email')
        competition = request.form.get('competition')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registrations (name, school, email, competition)
            VALUES (?, ?, ?, ?)
        ''', (name, school, email, competition))
        conn.commit()
        conn.close()

        return f'✅ 报名成功，感谢你，{name}！'
    return render_template('form.html')

@app.route('/enterprise', methods=['GET', 'POST'])
def enterprise():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_name = request.form.get('contact_name')
        email = request.form.get('email')
        problem = request.form.get('problem')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO enterprise_requests (company_name, contact_name, email, problem)
            VALUES (?, ?, ?, ?)
        ''', (company_name, contact_name, email, problem))
        conn.commit()
        conn.close()

        return f'✅ 提交成功，感谢您，{contact_name}！'
    return render_template('enterprise.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('title')
        leader = request.form.get('leader')
        email = request.form.get('email')
        description = request.form.get('description')
        file = request.files.get('file')

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO project_submissions (title, leader, email, description, filename)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, leader, email, description, filename))
        conn.commit()
        conn.close()

        return f'✅ 项目提交成功！感谢你，{leader}！'

    return render_template('submit.html')

@app.route('/cases')
def cases_home():
    return render_template('cases_home.html')

@app.route('/cases/student')
def cases_student():
    student_projects = [
        {"name": "Aissential", "description": "教育领域项目，模拟AI家教，生成习题与讲解，输入输出流程清晰。", "score": "★★★★☆ (4/5)"},
        {"name": "AutoPatch+", "description": "针对LLM幻觉问题进行优化，评估指标量化，适合作为竞赛难点题。", "score": "★★★★☆ (4/5)"},
        {"name": "Azrius Analytics", "description": "模拟AI写作助手，汇总网页数据并注释，入门门槛低，但评分较主观。", "score": "★★★☆☆ (3/5)"},
        {"name": "BayesSi", "description": "探讨摩尔定律限制下的算法突破，适合硬件竞赛提案，太技术向，不适合大多数学生。", "score": "★☆☆☆☆ (1/5)"},
        {"name": "ChainAim", "description": "多模型编排学习项目，可用多LLM组合构建可视化高冲击力demo。", "score": "★★★★★ (5/5)"},
        {"name": "CoolCpack LLC", "description": "自训练模型并展示结果，无需复杂资源，评分标准略模糊。", "score": "★★★☆☆ (3/5)"},
        {"name": "Coral", "description": "构建发音识别App，准确率可用于评分，技术适中。", "score": "★★★☆☆ (3/5)"},
        {"name": "Edifii", "description": "多LLM构建富可视化Q&A平台，大学生适合，技术适中。", "score": "★★★☆☆ (3/5)"},
        {"name": "Emilia AI", "description": "模拟AI服务员，图像/音频输入输出推荐，易于评估。", "score": "★★★★☆ (4/5)"},
        {"name": "Forkyt", "description": "餐厅推荐AI，模拟日常生活场景，无需大数据集。", "score": "★★★★★ (5/5)"},
        {"name": "Intelligent Dataworks", "description": "可构建简化的招聘平台，如自动生成面试题。", "score": "★★★☆☆ (3/5)"},
        {"name": "Miiflow", "description": "快速构建“输入→模型→输出”的AI流程，灵活度高。", "score": "★★★★☆ (4/5)"},
        {"name": "NewEcom.AI", "description": "构建AI销售代理demo，结构清晰但评分标准略弱。", "score": "★★☆☆☆ (2/5)"},
        {"name": "NVisual", "description": "训练AI识别建材缺陷，准确率和速度易评分。", "score": "★★★★★ (5/5)"},
        {"name": "SeeAir", "description": "识别住宅照片预测节能潜力，环境主题吸引学生兴趣。", "score": "★★★☆☆ (3/5)"},
        {"name": "VeriSci AI", "description": "用LLM翻译科研论文为通俗语言，锻炼prompt调优技巧。", "score": "★★★★☆ (4/5)"},
        {"name": "XStyle AI", "description": "用户+衣柜图像 → 输出搭配推荐，demo逻辑清晰。", "score": "★★★☆☆ (3/5)"}
    ]
    return render_template('cases_student.html', projects=student_projects)

@app.route('/cases/sme')
def cases_sme():
    sme_projects = [
        {"name": "Achievers Astra AI", "description": "面向教育机构，自动化教学、个性化进度规划。", "score": "★★★★★ (5/5)"},
        {"name": "Aikreate", "description": "AI辅助新员工培训、社媒运营，适用大多数中小企业。", "score": "★★★★☆ (4/5)"},
        {"name": "Aissential", "description": "K12辅导适配良好，行业局限于教育。", "score": "★★★★☆ (4/5)"},
        {"name": "AutoPatch+", "description": "减少LLM幻觉，适合法律/医疗类SME使用。", "score": "★★★★☆ (4/5)"},
        {"name": "Azrius Analytics", "description": "写作效率提升，适用于新闻/法律咨询类公司。", "score": "★★★★☆ (4/5)"},
        {"name": "Bystro AI", "description": "生物/医疗SME数据分析助手，减少人工解读时间。", "score": "★★★★☆ (4/5)"},
        {"name": "CoolCpack", "description": "无代码文档问答平台，降低技术门槛，适合培训/研究类SME。", "score": "★★★★★ (5/5)"},
        {"name": "Coral", "description": "可用于HR训练及教师表达能力优化。", "score": "★★★☆☆ (3/5)"},
        {"name": "CustomGPT.ai", "description": "私有GPT系统，适合数据处理类中小企业。", "score": "★★★★☆ (4/5)"},
        {"name": "Devdock", "description": "提供AI模型前处理能力，适合AI开发类SME。", "score": "★★★★☆ (4/5)"},
        {"name": "Edifii", "description": "理解学习目标、制定发展路径，适合教育机构。", "score": "★★★★☆ (4/5)"},
        {"name": "Emilia AI", "description": "提升客户响应效率，适合餐饮等前台服务业。", "score": "★★★☆☆ (3/5)"},
        {"name": "Forkyt", "description": "基于偏好学习推荐，适合小型餐饮企业。", "score": "★★★☆☆ (3/5)"},
        {"name": "Go and Slay", "description": "跨境英语培训AI，节省人力成本，适合国际贸易类公司。", "score": "★★★★☆ (4/5)"},
        {"name": "Historia Health", "description": "医疗设备整合高但法律敏感性强，适合中型医疗SME。", "score": "★★★☆☆ (3/5)"},
        {"name": "Intelligent Dataworks", "description": "自动化招聘流程，适合无专门HR的小企业。", "score": "★★★★★ (5/5)"},
        {"name": "Inventic", "description": "侦测金融欺诈，适合小银行或汇款企业。", "score": "★★★★☆ (4/5)"},
        {"name": "Kuratek (Kura)", "description": "跨境支付服务，适合制造型SME。", "score": "★★★★☆ (4/5)"},
        {"name": "Lendica", "description": "信贷评估+供应链金融助手，适合制造业中小企业。", "score": "★★★★★ (5/5)"},
        {"name": "Light Hope LLC", "description": "实战型AI培训，助力企业数字化转型。", "score": "★★★★★ (5/5)"},
        {"name": "Meshify", "description": "销售助理AI，适合快节奏电商类中小企业。", "score": "★★★☆☆ (3/5)"},
        {"name": "Moxie AI", "description": "医疗问答助手，适合小型医院，需人类审核输出。", "score": "★★★☆☆ (3/5)"},
        {"name": "Nethopper.io", "description": "GPT私有化交互，适合需数据保护的法律/教育/互联网公司。", "score": "★★★☆☆ (3/5)"},
        {"name": "NewEcom.AI", "description": "电商服务助手，提升转化率，减少人工客服依赖。", "score": "★★★★☆ (4/5)"},
        {"name": "NVisual", "description": "建材缺陷自动识别，适合建筑/制造行业质检自动化。", "score": "★★★★☆ (4/5)"},
        {"name": "Preloved Guru", "description": "二手时尚推荐引擎，适合库存优化。", "score": "★★★☆☆ (3/5)"},
        {"name": "SkipLegal", "description": "自动化移民表单处理，适合移民律师事务所或跨国招聘类企业。", "score": "★★★☆☆ (3/5)"},
        {"name": "Skiply", "description": "退货流程自动化，适合小型电商公司。", "score": "★★★★☆ (4/5)"},
        {"name": "Synergetics.ai", "description": "理赔流程加速，适合小型保险机构或诊所。", "score": "★★☆☆☆ (2/5)"},
        {"name": "Vibie AI", "description": "音乐+情绪分析增强顾客体验，适用于餐厅/健身房等场所。", "score": "★★★☆☆ (3/5)"},
        {"name": "YOUnified AI", "description": "企业控制中心整合工具，提升跨部门沟通与信息流整合。", "score": "★★★☆☆ (3/5)"}
    ]
    return render_template('cases_sme.html', projects=sme_projects)

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/reading')
def reading():
    return render_template('reading.html')

@app.route('/discussion', methods=['GET', 'POST'])
def discussion():
    conn = sqlite3.connect('discussion.db')
    cursor = conn.cursor()

    # 提交评论或回复
    if request.method == 'POST':
        content = request.form.get('content')
        parent_id = request.form.get('parent_id')

        if parent_id == '':
            parent_id = None

        # 如果是主评论（没有父ID），就取用户输入的名字
        if parent_id is None:
            name = request.form.get('username')
        else:
            name = '匿名回复者'

        cursor.execute('''
            INSERT INTO discussions (parent_id, name, content)
            VALUES (?, ?, ?)
        ''', (parent_id, name, content))
        conn.commit()
        return redirect(url_for('discussion'))

    # 获取所有评论
    cursor.execute('SELECT id, parent_id, name, content, timestamp FROM discussions ORDER BY timestamp ASC')
    rows = cursor.fetchall()

    all_comments = []
    for row in rows:
        comment = {
            'id': row[0],
            'parent_id': row[1],
            'name': row[2],
            'content': row[3],
            'timestamp': row[4]
        }
        all_comments.append(comment)

    conn.close()
    return render_template('discussion.html', comments=all_comments)

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")
    registrations = cursor.fetchall()

    cursor.execute("SELECT * FROM enterprise_requests")
    enterprise_requests = cursor.fetchall()

    cursor.execute("SELECT * FROM project_submissions")
    project_submissions = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        registrations=registrations,
        enterprise_requests=enterprise_requests,
        project_submissions=project_submissions
    )

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'LighthopeNasdaq':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error='❌ 用户名或密码错误')
    return render_template('admin_login.html')

from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    init_db()
    app.run(host='127.0.0.1', port=5050, debug=True)
# Added a test line on 2025/6/14
