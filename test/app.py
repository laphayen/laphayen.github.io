from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# MongoDB client 연결
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbjungle


# index.html 연결
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def save_memo():
    # 메모 제목
    title_receive = request.form['title_give']
    # 메모 내용
    contents_receive = request.form['contents_give']
    # 메모 아이디
    id_receive = request.form['id_give']

    # 메모 생성
    memo = {'title': title_receive, 'contents': contents_receive, 'script_randomid': id_receive}

    # mongdoDB 저장
    db.memos.insert_one(memo)

    # 자바스크립트에서 생성한 script_randomid로 검색하여 Object ID 추출후 str형태로 형변환후 피드백
    temp4id = db.memos.find_one({'script_randomid': id_receive})

    # print(str(temp4id.get('_id')))
    idfeedback = str(temp4id.get('_id'))
    db.memos.update_one({'_id': ObjectId(idfeedback)}, {'$set': {'id_copy': idfeedback}})

    return jsonify({'result': 'success'})


@app.route('/memo', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'memos': result})


@app.route('/api/delete', methods=['POST'])
def delete_memo():
    id_receive = request.form['id_give']
    db.memos.delete_one({'id_copy': id_receive})
    return jsonify({'result': 'success'})


@app.route('/api/edit', methods=['POST'])
def update_memo():
    id_receive = request.form['id_give']
    new_title = request.form['title_edit']
    new_contents = request.form['contents_edit']

    db.memos.update_one({'id_copy': id_receive}, {'$set': {'title': new_title}})
    db.memos.update_one({'id_copy': id_receive}, {'$set': {'contents': new_contents}})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)