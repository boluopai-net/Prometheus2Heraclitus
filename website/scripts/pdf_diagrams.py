"""Render public SVG figures through the task-owned headless browser carrier.

Browser CSS variables and embedded fonts must be resolved before PDF embedding.
Only loopback build files are served. The exact task target is closed on exit.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import subprocess
from threading import Thread


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


class DiagramRenderer:
    def __init__(self, work):
        self.work = Path(work).resolve()
        self.server = None
        self.target = None
        self.task = 'yinyang-pdf-' + str(os.getpid())

    def call(self, arguments):
        value = json.loads(subprocess.check_output(['browser-relay', *arguments], text=True))
        if not value.get('ok'):
            raise RuntimeError('Diagram browser: ' + value.get('message', 'operation failed'))
        return value['data']

    def command(self, *arguments):
        return self.call(['task-command', '--task-key', self.task, '--target-id', self.target, '--', *arguments])

    def open(self):
        if self.target:
            return
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(self.work)))
        Thread(target=self.server.serve_forever, daemon=True).start()
        self.origin = 'http://127.0.0.1:' + str(self.server.server_port)
        (self.work / 'blank.html').write_text('<!doctype html><title>PDF figure rendering</title>')
        result = self.call(['task-open', '--task-key', self.task, '--url', self.origin + '/blank.html'])
        self.target = result['target_id']

    def render(self, source):
        source = source.resolve()
        self.open()
        svg = source.read_text()
        box = re.search(r'viewBox="([^"]+)"', svg)
        if not box:
            raise ValueError('SVG figure lacks viewBox: ' + source.name)
        _, _, width, height = map(float, box[1].split())
        width, height = round(width * 2), round(height * 2)
        page = source.with_suffix('.html')
        svg = re.sub(r'<\?xml[^>]*\?>', '', svg)
        page.write_text('<!doctype html><html data-theme="light"><meta charset="utf-8">'
                        '<style>html,body{margin:0;padding:0;background:white}body>svg{display:block;'
                        'width:100vw!important;height:100vh!important;max-height:none!important}'
                        'svg text{font-family:"PingFang SC","Helvetica Neue",sans-serif}'
                        'svg *{animation:none!important;transition:none!important}</style>' + svg + '</html>')
        self.command('set', 'viewport', str(width), str(height))
        url = self.origin + '/' + str(page.relative_to(self.work))
        self.command('eval', 'location.href=' + json.dumps(url))
        # The page-bound wait checks document identity as well as its SVG.
        self.command('wait', '--fn', 'location.href===' + json.dumps(url) + '&&!!document.querySelector("svg")')
        self.command('eval', '(async()=>{document.querySelector("svg").setAttribute("data-theme","light");await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));return {svg:!!document.querySelector("svg"),fonts:document.fonts.status};})()')
        output = source.with_suffix('.png')
        self.command('screenshot', str(output))
        return output

    def close(self):
        try:
            if self.target:
                result = self.call(['task-close', '--task-key', self.task, '--target-id', self.target])
                if not result.get('target_absent'):
                    raise RuntimeError('Diagram render target was not closed')
        finally:
            if self.server:
                self.server.shutdown()
                self.server.server_close()

