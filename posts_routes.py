from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint("posts", __name__, description='posts api')

    @posts_blp.route('/', methods=['GET','POST'])
    def posts():
        cursor = mysql.connection.cursor()
        #조회
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
        
        #생성
        if request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message="제목이나 글이 없습니다.")
            sql = 'INSERT INTO posts(title, content) VALUES(%s,%s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'msg':"성공적으로 글이 생성되었습니다.","제목":title,"글":content}),201
        
        #수정 및 삭제
        @posts_blp.route('/<int:id>', methods=['GET','PUT','DELETE'])
        def post(id):
            cursor = mysql.connection.cursor()
            sql = f"SELECT * FROM posts WHERE id= {id}"
            cursor.execute(sql)
            post = cursor.fetchone()
          
                
            if request.method == 'GET':
                if not post:
                    abort(404,"찾을수 없습니다.")
                return ({
                    'id' : post[0],
                    'title' : post[1],
                    'content': post[2]
                })

            elif request.method == 'PUT':
                title = request.json.get('title')
                content = request.json.get('content')

                if not title or not content:
                    abort(400, "제목이나 글을 찾을수 없습니다.")
                if not post:
                    abort(404, "글을 찾을수 없습니다.")

                sql = f"UPDATE posts SET title= {title}, content={content} WHERE id ={id}"
                cursor.execute(sql)
                mysql.connection.commit()

                return jsonify({"msg":"성공적으로 제목과 글을 업데이트 했습니다."})

            elif request.method == 'DELETE':
                if not post:
                    abort(400, "제목이나 글을 찾을수 없습니다.")

                sql = f"DELETE FROM posts WHERE id ={id}"
                cursor.excute(sql)
                mysql.connection.commit()

                return jsonify({"msg":"성공적으로 삭제하였습니다."})
