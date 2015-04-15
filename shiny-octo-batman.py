# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, render_template, url_for
from docker import Client

app = Flask(__name__)
cli = Client(base_url='unix:///var/run/docker.sock')


@app.route("/")
def index():
	base_info = cli.info()
	return render_template('index.html', base_info=base_info)

@app.route("/container/")
@app.route("/container/<cn>")
def show(cn=None):
	if cn is None:
		'''
		show all exist containers
		'''
		containers = showContainers("all")
		return render_template('list.html', list=containers)

	else:
		detail_container = cli.inspect_container(container=cn)

		return render_template('detail.html', detail=detail_container)


@app.route("/running/")
def showRunnning():
	containers = showContainers()
	return render_template('live.html', list=containers)


@app.route("/stop/", methods=['POST'])
def terminateContainer():
	container_name = request.form['Name'].strip("/")
	cli.stop(container=container_name)
	return redirect(url_for('showRunnning'))


@app.route("/start/", methods=['POST'])
def startContainer():
	container_name = request.form['Name'].strip("/")
	cli.start(container=container_name)
	return redirect(url_for('showRunnning'))


@app.route("/delete/", methods=['POST'])
def destroy():
	container_name = request.form['Name'].strip("/")
	cli.remove_container(container=container_name)
	return redirect(url_for('showRunnning'))


def showContainers(x=None):
	if x == "all":
		containers = cli.containers(all=True)
	else:
		containers = cli.containers()

	container_list = []
	container_list = [{
		'name' : container['Names'][0].strip("/"),
		'status' : container['Status'],
		'image' : container['Image'],
		'port' : container['Ports']
	} for container in containers ]



	return container_list


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=8834)


