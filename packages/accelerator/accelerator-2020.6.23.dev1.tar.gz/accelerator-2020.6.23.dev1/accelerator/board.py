############################################################################
#                                                                          #
# Copyright (c) 2020 Carl Drougge                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#  http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
#                                                                          #
############################################################################

import bottle
import json
import os
import tarfile
import itertools
import operator

from accelerator.job import Job
from accelerator.dataset import Dataset

def get_job(jobid):
	if jobid.endswith('-LATEST'):
		base = jobid.rsplit('-', 1)[0]
		jobid = os.readlink(Job(base + '-0').path[:-2] + '-LATEST')
	return Job(jobid)

def main(argv, cfg):
	prog = argv.pop(0)
	if '-h' in argv or '--help' in argv or len(argv) not in (0, 1):
		print('usage: %s [port]' % (prog,))
		print('runs a web server on port (default 8520)')
		print('for displaying results (result_directory)')
		return
	port = int(argv[0]) if argv else 8520

	@bottle.get('/')
	@bottle.view('main')
	def main_page():
		return dict(
			project=os.path.split(cfg.project_directory)[1],
			workdirs=cfg.workdirs,
		)

	@bottle.get('/results')
	def results():
		res = {}
		for fn in os.listdir(cfg.result_directory):
			if fn.endswith('_'):
				continue
			ffn = os.path.join(cfg.result_directory, fn)
			try:
				jobid = os.readlink(ffn).split('/')[-2]
				res[fn] = dict(
					jobid=jobid,
					ts=os.lstat(ffn).st_mtime,
					size=os.stat(ffn).st_size,
				)
			except OSError:
				continue
		bottle.response.content_type = 'application/json; charset=UTF-8'
		bottle.response.set_header('Cache-Control', 'no-cache')
		return json.dumps(res)

	@bottle.get('/results/<name>')
	def file(name):
		return bottle.static_file(name, root=cfg.result_directory)

	@bottle.get('/job/<jobid>/method.tar.gz/')
	@bottle.get('/job/<jobid>/method.tar.gz/<name:path>')
	def job_method(jobid, name=None):
		job = get_job(jobid)
		with tarfile.open(job.filename('method.tar.gz'), 'r:gz') as tar:
			if name:
				info = tar.getmember(name)
			else:
				members = [info for info in tar.getmembers() if info.isfile()]
				if len(members) == 1 and not name:
					info = members[0]
				else:
					return bottle.template('job_method_list', members=members, job=job)
			bottle.response.content_type = 'text/plain; charset=UTF-8'
			return tar.extractfile(info).read()

	@bottle.get('/job/<jobid>/<name:path>')
	def job_file(jobid, name):
		job = get_job(jobid)
		return bottle.static_file(name, root=job.path)

	@bottle.get('/job/<jobid>')
	@bottle.get('/job/<jobid>/')
	@bottle.view('job')
	def job(jobid):
		job = get_job(jobid)
		try:
			prefix = job.path + '/'
			files = [fn[len(prefix):] for fn in job.files() if fn.startswith(prefix)]
		except OSError:
			# This happens for jobs that didn't finish.
			files = []
		subjobs = [Job(jobid) for jobid in job.post.subjobs]
		return dict(
			job=job,
			output=os.path.exists(job.filename('OUTPUT')),
			datasets=job.datasets,
			params=job.params,
			subjobs=subjobs,
			files=files,
		)

	@bottle.get('/dataset/<dsid:path>')
	def dataset(dsid):
		ds = Dataset(dsid.rstrip('/'))
		q = bottle.request.query
		if q.column:
			lines = int(q.lines or 10)
			it = ds.iterate(None, q.column)
			it = itertools.islice(it, lines)
			t = ds.columns[q.column].type
			if t in ('datetime', 'date', 'time',):
				it = map(str, it)
			elif t in ('bytes', 'pickle',):
				it = map(repr, it)
			res = list(it)
			bottle.response.content_type = 'application/json; charset=UTF-8'
			return json.dumps(res)
		else:
			return bottle.template('dataset', ds=ds)

	@bottle.get('/workdir/<name>')
	@bottle.view('workdir')
	def workdir(name):
		path = cfg.workdirs[name]
		prefix = name + '-'
		jobs = []
		for jid in os.listdir(path):
			if jid.startswith(prefix):
				try:
					jobs.append(Job(jid))
				except Exception:
					pass
		jobs.sort(key=operator.attrgetter('number'))
		return dict(name=name, jobs=jobs)

	bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__), 'board')]
	bottle.run(port=port, reloader=True)
