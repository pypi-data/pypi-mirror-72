#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import cairosvg
from getopt import getopt
try:
    from JsonToMarkdown import preprocess
    from JsonToMarkdown import libsvg
    from JsonToMarkdown import libmd
except ImportError:
    import preprocess
    import libsvg
    import libmd


class TranslateJson(object):
    def __init__(self, js_file, output_md, output_gitbook):
        self.js_file = js_file
        self.output_md = output_md
        self.output_gitbook = output_gitbook

        self.gitbookpath = ''
        self.markdownpath = ''
        self.data = ''
        self.pre_leval = 0
        self.history_addrr = 0
        self.history_offset = 0
        self.history_base = -1
        self.history_group = {}
        self.pre_group = ''
        self.all_reg_data = ''

    def get_dpath(self, in_dict, pre_path = ''):
        path_list = []
        for k in in_dict:
            l1_path = os.path.join(pre_path, k)
            if isinstance(in_dict[k], list):
                for n,v in enumerate(in_dict[k]):
                    l2_path = os.path.join(l1_path, str(n))
                    if k == "registers":
                        if "Attribute" not in v or v["Attribute"] != "GROUP":
                            path_list.append(l2_path.strip("/"))
                    if k == "group_reg":
                        if "group_reg" not in v:
                            path_list.append(l2_path.strip("/"))
                    path_list.extend(self.get_dpath(v, l2_path))
        return path_list
    
    def get_delem(self, in_dict, dpath, key = ''):
        path = dpath.strip('/').split('/')
        msg = ''
        for i in path:
            if i.isdigit():
                msg += "["  + i + "]"
            else:
                msg += "[\'"  + i + "\']"
        if key != '':
            msg += "[\'"  + key + "\']"
        return eval("in_dict" + msg)
    
    def get_group_path(self, in_path):
        tmp = []
        for n,v in enumerate(in_path.split("/")):
            if v == "group_reg":
                tmp.append(n)
        path = []
        if tmp != []:
            for i in tmp:
                path.append("/".join(in_path.split("/")[:i]))
        return path 
    
    def enter_group(self, dpath):
        #print("enter group")
        leval = 0
        group_path = self.get_group_path(dpath)
        for i in group_path:
            leval += 1 
            if i not in self.history_group:
                if 'Offset' in self.get_delem(self.js_dict, i):
                    group_step = int(self.get_delem(self.js_dict, i, key='Offset'), 16)
                    self.history_addrr += group_step
                    if leval >= 2:
                        self.history_offset = self.history_addrr
                    else:
                        self.history_offset = self.history_base + group_step
                elif 'Step' in self.get_delem(self.js_dict, i):
                    group_step = int(self.get_delem(self.js_dict, i, key='Step'), 16)
                    self.history_addrr += group_step
                    self.history_offset = self.history_addrr
                if 'depth' in self.get_delem(self.js_dict, i):
                    depth = self.get_delem(self.js_dict, i, key = 'depth')
                else:
                    depth = 1
                self.history_group[i] = {'depth':depth, 'num': 1, 'start': self.history_offset}
    
    def exit_group(self, dpath):
        #print("exit group")
        self.pre_group_list = self.get_group_path(self.pre_group + "/group_reg")
        now_group_list = self.get_group_path(dpath)
        self.exit_group_list = []
        self.enter_group_list = []
        for i in now_group_list:
            if i in self.pre_group_list:
                self.pre_group_list.remove(i)
            else:
                self.enter_group_list.append(i)
        self.exit_group_list = self.pre_group_list
        elen = len(self.exit_group_list)
        exit_step = 0
        next_num = 0 
        for i in range(elen):
            index = elen - i -1
            path = self.exit_group_list[index]
            if i == 0:
                next_num = self.history_group[path]['depth'] * self.history_group[path]['num']
            else:
                next_num = self.history_group[path]['depth'] * \
                        (self.history_group[path]['num'] + next_num -1)
        self.history_addrr = self.history_group[path]['start'] + next_num * (0x0004)
        self.history_offset = self.history_addrr
    
        if len(self.enter_group_list) > 0:
            self.enter_group(dpath)
    
    
    def get_addr(self, dpath):
        base_changed = 0
        block_path = dpath.split("registers")[0]
        base_addr = int(self.get_delem(self.js_dict, block_path, key='base_addr'), 16)
        if self.history_base == 0:
            self.history_base = base_addr
            self.history_offset = base_addr
            self.history_addrr = base_addr
        if self.history_base != base_addr:
            base_changed = 1
            self.history_base = base_addr
            self.history_offset = base_addr
            self.history_addrr = base_addr
    
        group_path_list = self.get_group_path(dpath)
        for i in group_path_list:
            if i in self.history_group:
                self.history_group[i]['num'] +=1
        if group_path_list != []:
            group_path = group_path_list[-1]
        else:
            group_path = ''
        if base_changed:
            self.pre_group = group_path
        else:
            if group_path != self.pre_group:
                if self.pre_group == '':
                    self.enter_group(dpath)
                else:
                    if group_path.find(self.pre_group) >= 0:
                        self.enter_group(dpath)
                    else:
                        self.exit_group(dpath)
                self.pre_group = group_path
        if 'Step' in self.get_delem(self.js_dict, dpath):
            offset_addr = self.get_delem(self.js_dict, dpath, key='Step')
            offset_addr = int(offset_addr,16)
            now_addr =  self.history_addrr + offset_addr
            self.history_addrr = now_addr
            return hex(now_addr)
        if 'Offset' in self.get_delem(self.js_dict, dpath):
            offset_addr = self.get_delem(self.js_dict, dpath, key='Offset')
            offset_addr = int(offset_addr,16)
            now_addr =  self.history_offset + offset_addr
            self.history_addrr = now_addr
            return hex(now_addr)
    
    def find_group_path(self, group, root_path):
        group_list = []
        group_list.append(root_path)
        for i in range(len(group['group_reg'])):
            path = root_path + "/group_reg/" + str(i)
            if 'group_reg' in group['group_reg'][i]:
                group_list.extend(self.find_group_path(group['group_reg'][i], path))
        return group_list
    
    def get_group_dict(self, dpath):
        group_dict = {}
        group = self.get_delem(self.js_dict, dpath)
        if 'depth' in group:
            depth = group['depth']
        else:
            depth = 1
        group_dict[dpath] = {"depth":depth, "num":0}
        for i in group['group_reg']:
            group_dict[dpath]['num'] += 1
        return group_dict
    
    def create_groupmsg(self):
        group_msg = {
                'step':'',
                'range':'',
                'group':[],
                }
        return group_msg
    
    def get_groupmsg(self, dpath):
        msg_list = ["N","J","M","k","Z","I","D"]
        group_path_list = self.get_group_path(dpath)
        group_path = group_path_list[0]
        group_end = group_path_list[-1]
        group = self.get_delem(self.js_dict, group_path)
        group_list = self.find_group_path(group, group_path)
        for n, path in enumerate(group_list):
            if path == group_end:
                end = n
        group_dict = {}
        for i in group_list:
            group_dict.update(self.get_group_dict(i))
        #print(group_dict)
        step_msg = ''
        scope_msg = ''
        total_msg = ''
        for j in range(len(group_list)):
            elen = len(group_list[j:])
            next_num = 0 
            for i in range(elen):
                index = elen - i -1
                path = group_list[j + index]
                if index == 0:
                    if next_num == 0:
                        next_num = group_dict[path]['num']
                    else:
                        next_num = (group_dict[path]['num'] + next_num -1)
                elif i == 0:
                    next_num = group_dict[path]['depth'] * group_dict[path]['num']
                else:
                    next_num = group_dict[path]['depth'] * \
                            (group_dict[path]['num'] + next_num -1)
            step = next_num * (0x0004)
            step_msg += "+" + msg_list[j] + "*" + hex(step)
            if total_msg == '':
                group_msg = self.create_groupmsg()
                total_msg = group_msg
            else:
                group_msg['group'].append(self.create_groupmsg())
                group_msg = group_msg['group'][0]
            group_msg['step'] = step
            group_msg['range'] = group_dict[path]['depth']
            scope_msg += " " + msg_list[j] + "的范围为0~" + str(group_dict[path]['depth']-1)
            if j == end:
                break
        #print(step_msg)
        #print(scope_msg)
        return step_msg, scope_msg, total_msg
    
    
    def get_reserve_fields(self, fields):
        re_map = [[0,31]]
        re_fields = []
        for f in fields:
            index_range = f['range']
            scope = index_range.strip("[]").split(":")
            end = int(scope[0])
            start = int(scope[-1])
            for r in re_map:
                if r[0] <= start and r[-1] >= end:
                    re_map.remove(r)
                    if r[0] != start:
                        re_map.append([r[0], start - 1])
                    if r[-1] != end:
                        re_map.append([end + 1, r[-1]])
        #print(re_map)
        for r in re_map:
            frange = "[" + str(r[-1]) + ":" + str(r[0]) + "]"
            re_fields.append({
                "name": "reserved",
                "range": frange,
                "reset_value": "0",
                })
        #print(re_fields)
        return re_fields
    
    
    def show_group(self, lm, group, name, des, st_addr):
        for i in range(int(group['range'])):
            new_name = name + "||" + str(i)
            new_addr = st_addr + i * group['step']
            if group['group'] != []:
                for g in group['group']:
                    self.show_group(lm, g, new_name, des, new_addr)
            else:
                self.all_reg_data += lm.md_create_body_line([new_name, hex(new_addr), des], self.output_md)
    
    def create_md3(self, dpath, lm):
        ls = libsvg.LibSVG()
        #print(dpath)
    
        is_group = 0
        register = self.get_delem(self.js_dict, dpath)
        name = self.get_delem(self.js_dict, dpath, key = 'RegName' )
        name = name.upper()
        addr = self.get_addr(dpath)
        if dpath.find("group_reg") >= 0:
            is_group = 1
            addr_msg, scope_msg, group_msg = self.get_groupmsg(dpath)
            #group_list = self.get_group_path(dpath)
            #for i in group_list:
            #    gname = self.get_delem(self.js_dict, i, key="RegName")
            #    gname = gname.upper()
            #    name = gname + "@" + name
            addr = str(addr) + addr_msg + ")</br>(" + scope_msg
        #print(name, "(" + addr + ")")
    
        #if name.endswith("reserved"):
        if name.endswith("RESERVED"):
            return -1
    
        des = self.get_delem(self.js_dict, dpath, key = 'Description')
        if is_group:
            st_addr = int(addr.split("+")[0], 16)
            self.show_group(lm, group_msg, name ,des, st_addr)
        else:
            st_addr = addr
            self.all_reg_data += lm.md_create_body_line([name, st_addr, des], self.output_md)
        fields = self.get_delem(self.js_dict, dpath, key = 'Fields')
        reserve_fields = self.get_reserve_fields(fields)
        fields.extend(reserve_fields)
        table = ls.create_blank_form()
        for f in fields:
            ls.add_line(table, f['range'])
        for f in fields:
            ls.add_reset_value(table, f['range'], f['reset_value'], f['name'])
        for f in fields:
            ls.add_name(table, f['range'], f['name'])
        #ls.write_down(table)
        ls.indent(table)
        svg_data = ls.svg_transform(table)
        svg_name = name + ".svg"
        with open(svg_name, "w") as fd:
            fd.write(svg_data)
        png_name = name + ".png"
        cairosvg.svg2png(url=svg_name, write_to = png_name)
        os.system("rm " + svg_name)
    
        #register_data = "![](" + svg_name + ")\n<br>"
        register_data = "![](" + png_name + ")\n<br>"
        for f in fields:
            if f['name'] != 'reserved':
                line = self.add_description(f['name'],f['description'])
                register_data += line + "\n<br>"
    
    
        #table_title = 'Register:' + name.split("@")[-1] + ' ('  + addr + ')'
        table_title = 'Register:' + name + ' ('  + addr + ')'
        #print(table_title)
        #register_data = "## " + '<center>' + table_title + '</center>\n\n' +\
        register_data = "## " + name + "\n" + '<center>' + table_title + '</center>\n\n' +\
            '\n' + '&nbsp;' + '\n'+ register_data
        if self.output_md:
            os.system("mv " + png_name + " " + self.markdownpath)
            self.data += register_data +'\n' + '<div STYLE="page-break-after: always;"></div>' + '\n'
        if self.output_gitbook:
            os.system("mv " + png_name + " " + self.gitbookpath)
            register_data += '\n' + '<div STYLE="page-break-after: always;"></div>' + '\n'
            file_path = os.path.join(self.gitbookpath, name + '.md')
            with open(file_path, 'w') as fd:
                fd.write(register_data)
    
    def add_description(self, name, des):
        dess = des.split(";")
        msg = ''
        if len(dess) == 1:
            line = "**" + name.upper() + "**:&emsp;" + des.strip(" ")
        else:
            for i in dess:
                msg += "<br>&emsp;" + i.strip(" ")
            line = "**" + name.upper() + "**:" + msg
        return line

    def main(self):
        file_msg = os.path.basename(self.js_file).split(".json")[0]
        pp = preprocess.PreProcess()
        self.js_dict = pp.start(self.js_file)
        self.js_dpath = self.get_dpath(self.js_dict)
        lm = libmd.LibMarkdown()
        self.all_reg_data = lm.md_create_title_line(['名称', '地址', '描述'])
        if self.output_gitbook:
            self.gitbookpath = "./_json_output/gitbook/" + file_msg
            if not os.path.exists(self.gitbookpath):
                os.system("mkdir -p " + self.gitbookpath)
            readme = os.path.join(self.gitbookpath, 'README.md')
            summery = os.path.join(self.gitbookpath, 'SUMMARY.md')
            if not os.path.exists(readme):
                with open(readme, 'w') as fd:
                    fd.write("   ")
            with open(summery, 'w') as fd:
                fd.write('# Summary \n\n')
                fd.write('* [寄存器介绍](all_register.md)\n')
                for i in range(int(len(self.js_dpath))):
                    name = self.get_delem(self.js_dict, self.js_dpath[i], key = 'RegName' )
                    name = name.upper()
                    if name.lower() != "reserved":
                        dpath = self.js_dpath[i]
                        if dpath.find("group_reg") >= 0:
                            is_group = 1
                            #group_list = self.get_group_path(dpath)
                            #for g in group_list:
                            #    gname = self.get_delem(self.js_dict, g, key="RegName")
                            #    gname = gname.upper()
                            #    name = gname + "@" + name
                        fd.write('  * [' + name + ']('+ name + '.md)\n')
                        self.create_md3(self.js_dpath[i], lm)
                with open(os.path.join(self.gitbookpath, 'all_register.md'), 'w') as fc:
                    fc.write("## 寄存器列表\n" + self.all_reg_data)
            print("\n\tcreate " + self.gitbookpath +" success") 
        if self.output_md:
            self.markdownpath = "./_json_output/" + file_msg
            if not os.path.exists(self.markdownpath):
                os.system("mkdir -p " + self.markdownpath)
            md_file = os.path.join(self.markdownpath, \
                    os.path.basename(self.js_file).split(".json")[0] + ".md")
            for i in self.js_dpath:
                self.create_md3(i, lm)
            self.data = "## 寄存器列表\n" + self.all_reg_data + self.data
            with open(md_file, 'w') as fd:
                fd.write(self.data)
            print("\n\tcreate " + md_file + " success") 


def usage():
    """
    Usage:
        jsontomd -f json_file (-g)
      exp
        jsontomd -f npu_register.json

    parameters:
        -f : 指定json文件
        -g : 加-g ,生成gitbook目录, 不加-g 生成单个markdown文件
    """
    print(usage.__doc__)

def main():
    if len(sys.argv) <= 1:
            usage()
            sys.exit()
    opts,args = getopt(sys.argv[1:],"f:gh")
    js_file = "demo.json"
    output_md = 1
    output_gitbook = 0
    for k,v in opts:
        if k == "-f":
            js_file = v
        if k == "-g":
            output_gitbook = 1
            output_md = 0
        if k == "-h":
            usage()
            sys.exit()
    #print("opts:", opts, "args", args)
    tj = TranslateJson(js_file, output_md, output_gitbook)
    tj.main()

if __name__ == "__main__":
    main()
