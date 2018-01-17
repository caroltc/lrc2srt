#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler
import settings
import os
import re

class MainHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render('index.html')

class CovertHandler(BaseHandler.BaseHandler):
    def post(self):
        filename = self.get_argument('filename', '')
        show_type = self.get_argument('type', '0')
        file_metas = self.request.files.get('file', None)
        filename = filename.replace(' ', '')+'.srt' if filename != "" else ""
        if not file_metas:
            file_contents = self.get_argument('lrc_data', None)
        else:
            file_contents = file_metas[0]['body']
            filename = file_metas[0]['filename'].replace('.lrc', '') + '.srt' if filename == "" else filename
        if not file_contents:
            self.write('convert failed! check you data!')
            return None
        lines = file_contents.split("\n")
        if len(lines) < 2:
            self.write('convert failed! no data!')
            return None
        srt_lines = []
        srt_data = ""
        for item in lines:
            pattern = re.compile(r'\[(\d\d)\:(\d\d)\.(\d\d)\]([^\[^\].]+)')
            re_datas = pattern.findall(item)
            if len(re_datas) > 0:
                for lrc_data in re_datas:
                    srt_lines.append({"time":"00:"+lrc_data[0]+":"+lrc_data[1]+","+lrc_data[2]+"0", "data":lrc_data[3].strip()})
        for i in range(len(srt_lines)):
            n = i+1
            next_time = srt_lines[n]['time'] if n < len(srt_lines) else "99:00:00,000"
            srt_data += str(n)+"\n" + srt_lines[i]['time'] + " --> " + next_time + "\n" + srt_lines[i]['data'] + "\n\n"
        if show_type == '0':
            self.write("<pre contenteditable='true'>"+srt_data+"</pre>")
            return None
        else:
            filename = 'temp.srt' if filename == "" else filename
            self.set_header ('Content-Type', 'application/octet-stream')
            self.set_header ('Content-Disposition', 'attachment; filename='+filename)
            self.write(srt_data)
            self.finish()

