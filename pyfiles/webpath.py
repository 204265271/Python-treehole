from flask import Flask, render_template_string, request, redirect
from sql import *
from datetime import datetime
from ABCD import reflection

app = Flask(__name__)
user_id = 114  # 这里假设用户名固定为 114，可根据实际情况修改

@app.route('/')
def index():
    return redirect('/newest_holes')


@app.route('/insert_hole', methods=['GET', 'POST'])
def insert_hole_route():
    if request.method == 'POST':
        content = request.form.get('content')
        release_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = insert_hole(release_time, user_id, content)
        return f"<h1>插入树洞结果</h1><p>新树洞的编号是 {result}</p><a href='/'>返回主页</a>"
    else:
        return """
        <h1>添加新树洞</h1>
        <form method="post">
            <label for="content">树洞内容:</label><br>
            <textarea id="content" name="content" rows="16" cols="80"></textarea><br>
            <input type="submit" value="提交">
        </form>
        <a href='/'>返回主页</a>
        """


@app.route('/insert_comment/<int:hole_id>', methods=['GET', 'POST'])
def insert_comment_route(hole_id):
    if request.method == 'POST':
        content = request.form.get('content')
        release_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = insert_comment(hole_id, release_time, user_id, content)
        return f"<h1>插入评论结果</h1><p>新评论的编号是 {result}</p><a href='/comments_for_hole/{hole_id}'>返回树洞</a>"
    else:
        return f"""
        <h1>为树洞添加新评论</h1>
        <form method="post">
            <label for="content">评论内容:</label><br>
            <textarea id="content" name="content" rows="16" cols="80"></textarea><br>
            <input type="submit" value="提交">
        </form>
        <a href='/comments_for_hole/{hole_id}'>返回树洞{hole_id}</a>
        """


@app.route('/newest_holes')
@app.route('/newest_holes/<int:k>')
def newest_holes_route():
    k, results = newest_holes(100)
    output = ""
    if results:
        output = "<div style='display: flex; flex-direction: column; gap: 20px;'>"
        for row in results:
            hole_id, release_time, username, content = row
            output += f"""
            <div style='border: 1px solid #ccc; padding: 20px; position: relative;'>
                <div style='position: absolute; top: 10px; left: 10px;'>
                    ID: {hole_id}
                    <a href="/delete_hole/{hole_id}" style="margin-left: 10px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                            <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg>
                    </a>
                </div>
                <div style='position: absolute; top: 10px; right: 10px;'>{release_time}</div>
                <p style='margin-top: 30px;'>{content}</p>
                <a href="/comments_for_hole/{hole_id}" style="position: absolute; bottom: 10px; right: 10px;">comment</a>
            </div>
            """
        output += "</div>"
    else:
        output = "没有找到树洞。"
    refresh_icon = """
    <a href="/newest_holes" style="float: right; margin-right: 20px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
            <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
        </svg>
    </a>
    """
    add_hole_icon = """
    <a href="/insert_hole" style="float: right; margin-right: 20px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
        </svg>
    </a>
    """
    return f"<h1>最新的 {k} 个树洞  {refresh_icon}{add_hole_icon}</h1>{output}<a href='/'>返回主页</a>"


@app.route('/comments_for_hole')
@app.route('/comments_for_hole/<int:hole_id>')
def comments_for_hole_route(hole_id):
    hole = query_hole(hole_id)
    if hole == None:     
        return f"<h1>树洞 {hole_id} 不存在</h1><a href='/'>返回主页</a>"
    hole_id, release_time, username, content = hole[0]
    output = f"""
                <div style='border: 1px solid #ccc; padding: 20px; position: relative;'>
                    <div style='position: absolute; top: 10px; left: 10px;'>
                        ID: {hole_id}
                        <a href="/delete_hole/{hole_id}" style="margin-left: 10px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                        </a>
                    </div>
                    <div style='position: absolute; top: 10px; right: 10px;'>{release_time}</div>
                    <p style='margin-top: 30px;'>{content}</p>
                    <a href="/insert_comment/{hole_id}" style="position: absolute; bottom: 10px; right: 10px;">Add Comment</a>
                </div>
                <br>
                """
    comments = get_comments_4_hole(hole_id)
    if comments:
            output += "<div style='display: flex; flex-direction: column; gap: 20px;'>"
            for comment in comments:
                comment_id, _, release_time, _, userNO, content = comment
                output += f"""
                <div style='border: 1px solid #ccc; padding: 20px; position: relative;'>
                    <div style='position: absolute; top: 10px; left: 10px;'>
                        ID: {comment_id}
                        <a href="/delete_comment/{comment_id}" style="margin-left: 10px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                        </a>
                    </div>
                    <div style='position: absolute; top: 10px; right: 10px;'>{release_time}</div>
                    <p style='margin-top: 30px;'>[{reflection(userNO)}]{content}</p>
                </div>
                """
            output += "</div>"
    else:
            output += f"树洞 {hole_id} 没有评论。"
    return f"<h1>树洞 {hole_id} 的所有评论</h1>{output}<a href='/comments_for_hole/{hole_id}'>刷新</a><br><a href='/'>返回主页</a>"


@app.route('/find_user_no')
def find_user_no_route():
    result = findUserNO(1, 1)
    return f"<h1>查找用户编号结果</h1><p>{result}</p><a href='/'>返回主页</a>"


@app.route('/delete_comment/<int:comment_id>')
def delete_comment_route(comment_id):
    hole_id = find_holeID_4_comment(comment_id)
    result = delete_comment(comment_id)
    return f"<h1>删除评论结果</h1><p>评论已删除</p><a href='/comments_for_hole/{hole_id}'>返回树洞</a>"


@app.route('/delete_hole')
@app.route('/delete_hole/<int:hole_id>')
def delete_hole_route(hole_id):
    delete_hole(hole_id)
    return f"<h1>删除树洞结果</h1><p>树洞 {hole_id} 及其对应的评论已删除。<p><a href='/newest_holes'>返回查看最新树洞</a>"