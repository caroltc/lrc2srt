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
        filename = filename+'.srt' if filename != "" else ""
        if not file_metas:
            file_contents = self.get_argument('lrc_data', None)
        else:
            file_contents = file_metas[0]['body']
            filename = file_metas[0]['filename'].replace('.lrc', '') + '.srt' if filename == "" else filename
        if not file_contents:
            self.write('convert failed! check you data!')
            return None
        lrc_ti_pattern = re.compile(r'\[ti:(.*)\]')
        lrc_ti_datas = lrc_ti_pattern.findall(file_contents)
        lrc_ti = 'temp'
        if len(lrc_ti_datas) > 0:
            lrc_ti = lrc_ti_datas[0]
        break_pattern = re.compile(r'[^\].]\[')
        data_breaks = break_pattern.findall(file_contents)
        # print data_breaks
        if len(data_breaks) > 0:
            for break_tag in data_breaks:
                if break_tag != "\n[":
                    new_break_tag = break_tag.replace('[', "\n[")
                    file_contents = file_contents.replace(break_tag, new_break_tag)
        lines = file_contents.split("\n")
        if len(lines) < 2:
            self.write('convert failed! no data!')
            return None
        srt_lines = []
        srt_data = ""
        for item in lines:
            data_pattern = re.compile(r'\[(\d\d)\:(\d\d)\.?(\d\d)?\]([^\[^\].]+)')
            re_datas = data_pattern.findall(item)
            lrc_item_data = None
            if len(re_datas) > 0:
                lrc_item_data = re_datas[0][3]
            time_pattern = re.compile(r'\[(\d\d)\:(\d\d)\.?(\d\d)?\]{1,10}')
            time_datas = time_pattern.findall(item)
            if lrc_item_data and len(time_datas) > 0:
                for time_data in time_datas:
                    mtime = '0' if time_data[2] == '' else time_data[2]
                    time_index = int(time_data[0].zfill(2)+time_data[1].zfill(2)+mtime.zfill(3))
                    srt_lines.append({"time":"00:"+time_data[0]+":"+time_data[1]+","+mtime+"0", "data":lrc_item_data.strip(), "time_index":time_index})
            srt_lines = sorted(srt_lines, key=lambda lrcline: lrcline["time_index"])
        for i in range(len(srt_lines)):
            n = i+1
            next_time = srt_lines[n]['time'] if n < len(srt_lines) else "99:00:00,000"
            srt_data += str(n)+"\n" + srt_lines[i]['time'] + " --> " + next_time + "\n" + srt_lines[i]['data'] + "\n\n"
        if show_type == '0':
            self.write("<pre contenteditable='true'>"+srt_data+"</pre>")
            return None
        else:
            filename = lrc_ti+'.srt' if filename == "" else filename.replace(' ', '-')
            self.set_header ('Content-Type', 'application/octet-stream')
            self.set_header ('Content-Disposition', 'attachment; filename='+filename)
            self.write(srt_data)
            self.finish()

