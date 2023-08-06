# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET

class LibSVG(object):
    def __init__(self):
        self.cell = 20
        pass

    def indent(self, elem, level=0):
        '''
        添加xml文件的换行符,增强可读性
        '''
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def create_blank_form(self):
        table = ET.Element('svg', attrib = {
            "baseProfile":"full",
            "width":"800",
            "height":"250",
            "version":"1.1",
            "viewBox":"0 0 700 250",
            "xmlns":"http://www.w3.org/2000/svg",
            "xmlns:ev":"http://www.w3.org/2001/xml-events",
            "xmlns:xlink":"http://www.w3.org/1999/xlink",
            })
        defs = ET.SubElement(table,'defs')
        all_group = ET.SubElement(table,'g', attrib = {"transform":"translate(4.5,150)"})
        # 名称组, 分区名
        name_group = ET.SubElement(all_group, 'g', attrib = {
            "transform":"rotate(-45 0,0)",
            })

        # 线条组, 表格框
        line_group = ET.SubElement(all_group, 'g', attrib = {
            "stroke":"black",
            "stroke-linecap":"round",
            "stroke-width":"1",
            "transform":"translate(0,20.0)",
            })
        ET.SubElement(line_group, 'line', attrib = {"x1":"0", "y1":"0", "x2":"640", "y2":"0"})
        ET.SubElement(line_group, 'line', attrib = {"x1":"0", "y1":"0", "x2":"0", "y2":"40"})
        ET.SubElement(line_group, 'line', attrib = {"x1":"0", "y1":"40", "x2":"640", "y2":"40"})
        ET.SubElement(line_group, 'line', attrib = {"x1":"640", "y1":"0", "x2":"640", "y2":"40"})
        for i in range(32):
            x_p = str(i*20)
            ET.SubElement(line_group, 'line', attrib = {"x1":x_p, "y1":"0", "x2":x_p, "y2":"5"})
            ET.SubElement(line_group, 'line', attrib = {"x1":x_p, "y1":"35", "x2":x_p, "y2":"40"})

        # 值组, 分区坐标,分区初始值
        value_group = ET.SubElement(all_group, 'g', attrib = {
            "text-anchor":"middle",
            })
        index_group = ET.SubElement(value_group, 'g', attrib = {"transform":"translate(20.0,16.0)"})
        reset_group = ET.SubElement(value_group, 'g', attrib = {"transform":"translate(20.0,46.0)"})
        color_group = ET.SubElement(value_group, 'g', attrib = {"transform":"translate(0,20.0)"})

        # 刻度组
        ruler_group = ET.SubElement(all_group, 'g', attrib = {
            "stroke":"black",
            "stroke-linecap":"round",
            "stroke-width":"1",
            "transform":"translate(0,60.0)",
            })
        ET.SubElement(ruler_group, 'line', attrib = {"x1":"0", "y1":"5", "x2":"640", "y2":"5"})
        for i in range(9):
            x_p = str(i*20*4)
            ET.SubElement(ruler_group, 'line', attrib = {"x1":x_p, "y1":"0", "x2":x_p, "y2":"10"})
            if i == 0:
                x_p = str(10)
                index_elem = ET.SubElement(ruler_group, 'text', attrib = {
                    "text-anchor":"middle",
                    "transform":"translate(0,17.0)",
                    "font-family":"source code pro",
                    "font-size":"12",
                    "font-weight":"normal",
                    "x":x_p,
                    })
                index_elem.text = str(31)
            else:
                x_p = str(i*20*4 - 10)
                index_elem = ET.SubElement(ruler_group, 'text', attrib = {
                    "text-anchor":"middle",
                    "transform":"translate(0,17.0)",
                    "font-family":"source code pro",
                    "font-size":"12",
                    "font-weight":"normal",
                    "x":x_p,
                    })
                index_elem.text = str(32-i*4)
        return table

    def add_line(self, table, index_range):
        scope = index_range.strip("[]").split(":")
        end = int(scope[0]) + 1
        start = int(scope[-1])
        for index in range(start, end):
            re_index = 31 - index
            if index == start:
                self._add_long_string(table, re_index + 1)
            if index == end - 1:
                self._add_long_string(table, re_index)

    def add_reset_value(self, table, index_range, value, name):
        scope = index_range.strip("[]").split(":")
        end = int(scope[0]) + 1
        start = int(scope[-1])
        if name == "reserved":
            self._add_color(table, start, end)
        else:
            self._add_index(table, start, end)
        self._add_value(table, start, end, value)

    def add_name(self, table, index_range, name):
        scope = index_range.strip("[]").split(":")
        end = int(scope[0]) + 1
        start = int(scope[-1])
        middle = int((end + start)/2)
        x_p = str(((31 - middle)*20 + 10)/1.414)
        value_elem = ET.SubElement(table[1][0], 'text', attrib = {
                "font-family":"source code pro",
                "font-size":"12",
                "font-weight":"normal",
                "x":x_p,
                "y":x_p,
                })
        if name != "reserved":
            value_elem.text = name.upper()
        else:
            value_elem.attrib['font-size'] = "12"
            value_elem.text = "(" + name + ")"

    def _add_color(self, table, start, end):
        x_p = str((31 - end + 1)*20)
        width = str((end - start)*20)
        index_elem = ET.SubElement(table[1][2][2], 'rect', attrib = {
            "fill":"black",
            "fill-opacity":"0.1",
            "height":"40",
            "width":width,
            "x":x_p,
            "y":"0",
            })

    def _add_value(self, table, start, end, value):
        if int(value, 16) == 0:
            for i in range(start, end):
                x_p = str((31 - i)*20 - 10)
                index_elem = ET.SubElement(table[1][2][1], 'text', attrib = {
                    "font-family":"source code pro",
                    "font-size":"16",
                    "font-weight":"normal",
                    "x":x_p,
                    })
                index_elem.text = str(0)
        else:
            fill_list = list(bin(int(value, 16))[2:])
            for i in range(start, end):
                x_p = str((31 - i)*20 - 10)
                index_elem = ET.SubElement(table[1][2][1], 'text', attrib = {
                    "font-family":"source code pro",
                    "font-size":"16",
                    "font-weight":"normal",
                    "x":x_p,
                    })
                if fill_list != []:
                    index_elem.text = str(fill_list.pop(-1))
                else:
                    index_elem.text = str(0)

    def _add_index(self, table, start, end):
        if end == start + 1:
            x_p = str((31 - start)*20 - 10)
            index_elem = ET.SubElement(table[1][2][0], 'text', attrib = {
                "font-family":"source code pro",
                "font-size":"12",
                "font-weight":"normal",
                "x":x_p,
                })
            index_elem.text = str(start)
        else:
            start_p = str((31 - start)*20 - 10)
            index_elem = ET.SubElement(table[1][2][0], 'text', attrib = {
                "font-family":"source code pro",
                "font-size":"12",
                "font-weight":"normal",
                "x":start_p,
                })
            index_elem.text = str(start)
            end_p = str((31 - end)*20 + 10)
            index_elem = ET.SubElement(table[1][2][0], 'text', attrib = {
                "font-family":"source code pro",
                "font-size":"12",
                "font-weight":"normal",
                "x":end_p,
                })
            index_elem.text = str(end - 1)

    def _add_long_string(self, table, index):
        x_p = str(index * 20)
        ET.SubElement(table[1][1], 'line', attrib = {"x1":x_p, "y1":"0", "x2":x_p, "y2":"40"})

    def _add_short_string(self, table, index):
        # not used
        x_p = str(index * 20)
        ET.SubElement(table[1][1], 'line', attrib = {"x1":x_p, "y1":"0", "x2":x_p, "y2":"5"})
        ET.SubElement(table[1][1], 'line', attrib = {"x1":x_p, "y1":"35", "x2":x_p, "y2":"40"})



    #def fill_form(self, table, name, index_range):
    #    scope = index_range.strip("[]").split(":")
    #    end = int(scope[0]) + 1
    #    start = int(scope[-1])
    #    for index in range(start, end):
    #        if index < 0 or index > 31:
    #            print("index out of range")
    #        x = (3 - index//8) *2 + 1
    #        y = 7 - index%8
    #        table[x][0][y].text = name
    #    return table

    def merge_form(self, table):
        data_map = self._get_data_map_by_table(table)
        new_table = self._create_form_by_data_map(data_map)
        return new_table

    def _get_data_map_by_table(self, table):
        '''
        data_map format:
        [{'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]': 'idle_cycle'}, \
                {'[16, 17, 18]': 'reserve'}, {'[19]': 'clock_gating_enable'},\
                {'[20, 21, 22, 23, 24, 25, 26]': 'reserve'}, {'[27]': 'idle_type'}, \
                {'[28, 29, 30]': 'reserve'}, {'[31]': 'en'}]
        '''
        data_map = []
        data_hash = {}
        data_range = []
        pre_data = ''
        for x, line in enumerate(table):
            if line.tag == "tbody":
                for y, data in enumerate(line[0]): 
                    now = int(((x-1)/2)*8 + y)
                    if data.text != pre_data:
                        if now - 1 >= 0 :
                            data_hash = {str(data_range):pre_data}
                            data_map.append(data_hash)
                            data_range = []
                        data_range.append(now)
                        pre_data = data.text
                    else:
                        data_range.append(now)
        data_hash = {str(data_range):pre_data}
        data_map.append(data_hash)
        #print(data_map)
        return data_map
    
    def _create_form_by_data_map(self, data_map):
        n = 0
        #table = ET.Element('table', attrib = {"width":"200px", "style":\
        #        {"word-break": "break-all", "word-wrap":"break-word"}})
        table = ET.Element('table', attrib = {"style":"TABLE-LAYOUT: fixed", "border":"1",\
                "cellspacing":"0", "cellpadding":"0", "width":"1250"})
        title = ET.SubElement(table, 'thead')
        title_tr = ET.SubElement(title, 'tr')
        data = ET.SubElement(table, 'tbody')
        data_tr = ET.SubElement(data, 'tr')
        data_th = ET.SubElement(data_tr, 'th', attrib = {"align":"center"})
        pre_col = 0
        is_return = 0
        for i in range(32):
            quotient = (i) // 8#商
            remainder = (i + 1) % 8#余数
            title_th = ET.SubElement(title_tr, 'th', attrib = {"align":"center"})
            title_th.text = "B" + str(31-i )
            if i in eval(list(data_map[n].keys())[0]):
                data_th.text = list(data_map[n].values())[0]
                colspan = i+1 - quotient*8
                data_th.set("colspan", str(colspan - pre_col))
                is_return = 0
            else:
                pre_col += colspan
                colspan = 0
                n += 1
                if is_return == 1:
                    pass
                elif is_return == 0:
                    data_th = ET.SubElement(data_tr, 'th', attrib = {"align":"center"})
                data_th.text = list(data_map[n].values())[0]
                if len(eval(list(data_map[n].keys())[0])) == 1:
                    pre_col += 1
                is_return = 0
            if remainder == 0 and i != 31:
                is_return = 1
                pre_col = 0
                colspan = 0
                title = ET.SubElement(table, 'thead')
                title_tr = ET.SubElement(title, 'tr')
                data = ET.SubElement(table, 'tbody')
                data_tr = ET.SubElement(data, 'tr')
                data_th = ET.SubElement(data_tr, 'th', attrib = {"align":"center"})
        return table

    def create_title_line(self, argv):
        table = ET.Element('table', attrib = {"border":"1"})
        #table = ET.Element('table')
        title = ET.SubElement(table, 'thead')
        title_tr = ET.SubElement(title, 'tr')
        for i in argv:
            title_th = ET.SubElement(title_tr, 'th', attrib = {"align":"center"})
            title_th.text = str(i)
        return table

    def create_body_line(self, table, argv):
        data = ET.SubElement(table, 'tbody')
        data_tr = ET.SubElement(data, 'tr')
        for i in argv:
            if len(i) >= 10:
                data_th = ET.SubElement(data_tr, 'th', attrib = {"align":"left"})
            else:
                data_th = ET.SubElement(data_tr, 'th', attrib = {"align":"center"})
            data_th.text = str(i)
        return table
    
    def md_register_name(self, name):
        data = "### " + name + "\n"
        return data

    def md_register_des(self, des):
        data = "&emsp;" + des + "\n"
        return data

    def md_register_addr(self, addr):
        data = "#### Address: " + addr + "\n"
        return data

    def svg_transform(self, table):
        #return ET.tostring(table) + "\n" + "<\br>" + "\n"
        #return str(ET.tostring(table), 'utf-8') + "\n" + "&nbsp;" + "\n"
        return str(ET.tostring(table), 'utf-8') + "\n"
        #return ET.tostring(table, encoding='UTF-8')+ "<\br>" + "\n"

if __name__ == "__main__":
    pass
    #lm = LibMarkdown()
    ##table = lm.create_blank_form2()
    #table = lm.create_blank_form()
    ##table = lm.fill_form(table, "clock_gating_enable", "[12]")
    ##table = lm.fill_form(table, "idle_type", "[4]")
    ##table = lm.fill_form(table, "en", "[0]")
    ##table = lm.fill_form(table, "idle_cycle", "[16:31]")
    #lm.fill_form(table, 'all_idle_int_en', '[31]')
    #lm.fill_form(table, 'mcu_cmd_int_en', '[16]')
    #lm.fill_form(table, 'op_cal_overflow_int_en', '[14]')
    #lm.fill_form(table, 'mac_cal_overflow_int_en', '[13]')
    #lm.fill_form(table, 'cmd_err_int_en', '[12]')
    #lm.fill_form(table, 'overtime_int_en', '[8]')
    #lm.fill_form(table, 'over_int_en', '[0]')
    #table = lm.merge_form(table)

    #print(table)
    #lm.indent(table)
    #w = ET.ElementTree(table)
    #w.write("ccc.md",'utf-8', True)
