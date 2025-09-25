from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint("posts", __name__, description='posts api')

    @posts_blp.route('/', methods=['GET','POST'])
    def posts():
        cursor = mysql.connection.cursor()
        if request.method == 'GET':
            sql = "SELECT * FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            post_list =[]

            for post in posts:
                post_list.append({
                    'id' : post[0],
                    'title' : post[1],
                    'content': post[2]
                })
            return jsonify(post_list)
        
        if request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message="제목이나 글이 없습니다.")
            sql = 'INSERT INTO posts(title, content) VALUES(%s,%s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'msg':"성공적으로 글이 생성되었습니다.","제목":title,"글":content}),201