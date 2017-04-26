from flask import Flask, render_template
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
# from flask_socketio import SocketIO, emit, disconnect
from RandomForest_word2vec import *
app = Flask(__name__)
app.secret_key = '!@#$%^&*()'
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True


@app.route('/api_sim',methods=['GET', 'POST'])
def get_sim_dict():
	print(request.method)
	if request.method == 'POST':
		search_type = request.form['search_type']
		sentence = request.form['sentence']

	else:
		search_type = request.args.get('search_type')
		sentence = request.args.get("sentence")
	print(search_type)
	print(sentence)

	document_ret_dict = impl_sim(search_type, sentence)
	return jsonify(document_ret_dict)

if __name__ == '__main__':##
	print("begin flask service")
	# socketio.run(app, debug=True)
	app.run(host='0.0.0.0')
