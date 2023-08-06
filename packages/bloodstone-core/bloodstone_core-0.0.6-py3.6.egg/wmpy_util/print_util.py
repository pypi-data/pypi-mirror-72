# ---------------- Console 打印作图 --------------
blank = [chr(183)]  ##此处为空格格式;Windows控制台下可改为chr(12288) ;linux系统中可改为chr(32)【chr(32)==' ' ;chr(183)=='·' ;chr(12288)=='　'】
blank = [chr(12288)]
blank = [chr(32)]
tabs = ['']


class TreeNode:
    __all_dict__ = dict()
    count = 0

    def __new__(cls, id, *args, **kwargs):
        """
        实现基于id的单例
        :param id: 此处id不一定要是数字可以为字符串
        :param args:
        :param kwargs:
        :return:
        """
        if id in TreeNode.__all_dict__:
            return TreeNode.__all_dict__[id]
        else:
            obj = super(TreeNode, cls).__new__(cls)
            obj.id = id
            obj.children = []
            obj.father = None
            obj.number_id = TreeNode.count
            TreeNode.count += 1
            TreeNode.__all_dict__[id] = obj
            return obj

    def __init__(self, id):
        """
        树节点类，继承该类可以轻松实现树状图的绘制
        需要手动往children list中插入节点
        或者调用set_parent设置父节点，可以自动实现关联
        重写__str__方法，以便打印节点的详情
        :param id 节点的唯一id
        """
        pass

    def get_children(self):
        """
        获得所有子节点
        :return:
        """
        return self.children

    def get_parent(self):
        """
        获得父节点
        :return:
        """
        return self.father

    def set_father_by_id(self, fid):
        """
        通过id设置父节点
        :param fid:
        :return:
        """
        f_node = TreeNode.get_node_by_id(fid)
        f_node.add_child(self)

    def __set_father(self, father):
        """

        :param father:
        :return:
        """
        if self.father is not None and not self.father == father:
            raise ValueError("TreeNode cannot have two diff fathers f1=%s  f2=%s" % (str(self.father), str(father)))
        else:
            self.father = father

    def add_child(self, child):
        """
        添加一个子节点
        :param child:
        :return:
        """
        if child not in self.children:
            self.children.append(child)
            child.__set_father(self)

    def add_child_by_id(self, cid):
        """
        通过id设置子节点
        :param cid:
        :return:
        """
        child = TreeNode.get_node_by_id(cid)
        self.add_child(child)

    @staticmethod
    def get_node_by_id(tid):
        """
        通过唯一id获得树节点，如果id不存在则返回null
        :param tid:
        :return:
        """
        if tid in TreeNode.__all_dict__:
            node = TreeNode.__all_dict__[tid]
        else:
            node = None
        return node

    def get_tree_structure(self):
        """
        得到指定的树形结构表示
        :return:
        """
        _result = list()
        _info = str(self)
        _children = self.get_children()
        # 限制描述文字的最大长度为20
        if len(_info) > 20:
            _info = _info[0:10] + "..."
        _result.append(_info)
        if _children is not None and len(_children) > 0:
            _child_infos = list()
            for child in _children:
                _child_infos += child.get_tree_structure()
            _result.append(_child_infos)
        return _result

    def plot_tree(self):
        """
        绘制树形图
        :return:
        """
        print("-" * 20)
        structure = self.get_tree_structure()
        # print(structure)
        print("-" * 5)
        plot_tree(structure)

    def plot_tree2(self, tab=""):
        """
        绘制树形图方法2, better!
        :return:
        """
        size = 2
        child_len = len(self.children)
        s = '─' * size
        if child_len > 0:
            s += '┬'
        else:
            s += '─'
        s += '─' * size
        print(s, end="")
        print(str(self))
        tab = tab + blank[0] * size
        for index, child in enumerate(self.children):
            # 最后一个子节点特殊处理
            if index + 1 == child_len:
                pre = '└'
            else:
                pre = '├'
            print(tab + pre, end="")
            if index + 1 == child_len:
                tab += blank[0]
            else:
                tab += '│'
            child.plot_tree2(tab=tab)
            tab = tab[:-1]

    def delete(self):
        """
        删除该节点
        :return:
        """
        if self.id in TreeNode.__all_dict__:
            TreeNode.__all_dict__.pop(self.id)

    def __str__(self):
        return str(self.id)


def plot_tree(lst):
    lst_len = len(lst)
    if lst_len == 0:
        print('─' * 3)
    else:
        for i, j in enumerate(lst):
            if i != 0:
                print(tabs[0], end='')
            if lst_len == 1:
                s = '─' * 3
            elif i == 0:
                s = '┬' + '─' * 2
            elif i + 1 == lst_len:
                s = '└' + '─' * 2
            else:
                s = '├' + '─' * 2
            print(s, end='')
            if isinstance(j, list) or isinstance(j, tuple):
                if i + 1 == lst_len:
                    tabs[0] += blank[0] * 3
                else:
                    tabs[0] += '│' + blank[0] * 2
                plot_tree(j)
            else:
                print(j)
    tabs[0] = tabs[0][:-3]


def exp_plot_tree():
    """
    测试画树形图
    :return:
    """
    Linux = 'Fedora', ['Debian', ['Ubuntu', ['Kubuntu', 'Xubuntu', 'Edubuntu']], ['KNOPPIX']], [
        ['Puppy Linux']], 'Open SUSE', 'Gentoo', 'Slackware', ['abc', 'def']
    Android = 'Android 1.5 Cupcake', 'Android 1.6  Donut ', 'Android 2.2/2.2 Froyo', 'Android 2.3 Gingerbread', \
              'Android 3.0 Honeycomb', 'Android 4.0 Ice Cream Sandwich'
    OS = [['Unix', [['Free BSD', 'Mac OS']], [Linux]], ['Dos', ['MS-DOS']], 'Windows'], \
         [], ['iOS', Android, 'Symbian', 'BlackBerry OS', 'WebOS', []]
    print('OS')
    plot_tree(Linux)


#   格式：\033[显示方式;前景色;背景色m
#   说明:
#
#   前景色            背景色            颜色
#   ---------------------------------------
#     30                40              黑色
#     31                41              红色
#     32                42              绿色
#     33                43              黃色
#     34                44              蓝色
#     35                45              紫红色
#     36                46              青蓝色
#     37                47              白色
#
#   显示方式           意义
#   -------------------------
#      0           终端默认设置
#      1             高亮显示
#      4            使用下划线
#      5              闪烁
#      7             反白显示
#      8              不可见
#
#   例子：
#   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
#   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]
color_black = 'black'  # 黑色
color_red = 'red'  # 红色
color_green = 'green'  # 绿色
color_yellow = 'yellow'  # 黄色
color_blue = 'blue'  # 蓝色
color_purple = 'purple'  # 紫红色
color_cyan = 'cyan'  # 青蓝色
color_white = 'white'  # 白色

mode_normal = 'normal'  # 终端默认设置
mode_bold = 'bold'  # 高亮显示
mode_underline = 'underline'  # 使用下划线
mode_blink = 'blink'  # 闪烁
mode_invert = 'invert'  # 反白显示
mode_hide = 'hide'  # 不可见

STYLE = {
    'fore':
        {  # 前景色
            'black': 30,  # 黑色
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple': 35,  # 紫红色
            'cyan': 36,  # 青蓝色
            'white': 37,  # 白色
        },

    'back':
        {  # 背景
            'black': 40,  # 黑色
            'red': 41,  # 红色
            'green': 42,  # 绿色
            'yellow': 43,  # 黄色
            'blue': 44,  # 蓝色
            'purple': 45,  # 紫红色
            'cyan': 46,  # 青蓝色
            'white': 47,  # 白色
        },

    'mode':
        {  # 显示模式
            'normal': 0,  # 终端默认设置
            'bold': 1,  # 高亮显示
            'underline': 4,  # 使用下划线
            'blink': 5,  # 闪烁
            'invert': 7,  # 反白显示
            'hide': 8,  # 不可见
        },

    'default':
        {
            'end': 0,
        },
}


def UseStyle(string, mode='', font_color='', back_color=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''

    font_color = '%s' % STYLE['fore'][font_color] if font_color in STYLE['fore'] else ''

    back_color = '%s' % STYLE['back'][back_color] if back_color in STYLE['back'] else ''

    style = ';'.join([s for s in [mode, font_color, back_color] if s])

    style = '\033[%sm' % style if style else ''

    end = '\033[%sm' % STYLE['default']['end'] if style else ''

    text = '%s%s%s' % (style, string, end)

    return text


import re

patterns = re.compile(r"\033\[[0-9;]*m(.*?)\033\[[0-9;]*m")


def de_color(text):
    """
    在线上环境去除彩色文字影响
    :param text:
    :return:
    """
    try:
        ret = patterns.sub(r"\1", text)
        text = ret
    except Exception as error:
        pass
    return text


def test_de_color():
    import logging
    import json
    logger = logging.getLogger("django_logger")
    tag1 = UseStyle('12.32', font_color='black', back_color='white')
    tag2 = UseStyle('45.67', font_color='black', back_color='yellow')
    text = "some word " + tag1 + "other word " + tag2 + "third word"
    logger.error("Before: %s" % json.dumps(text))
    ret = de_color(text)
    logger.error("After: %s" % json.dumps(ret))


def TestColor():
    print(UseStyle('正常显示'))
    print('')

    print("测试显示模式")
    print(UseStyle('高亮', mode='bold'), )
    print(UseStyle('下划线', mode='underline'), )
    print(UseStyle('闪烁', mode='blink'), )
    print(UseStyle('反白', mode='invert'), )
    print(UseStyle('不可见', mode='hide'))
    print('')

    print("测试前景色")
    print(UseStyle('黑色', font_color='black'), )
    print(UseStyle('红色', font_color='red'), )
    print(UseStyle('绿色', font_color='green'), )
    print(UseStyle('黄色', font_color='yellow'), )
    print(UseStyle('蓝色', font_color='blue'), )
    print(UseStyle('紫红色', font_color='purple'), )
    print(UseStyle('青蓝色', font_color='cyan'), )
    print(UseStyle('白色', font_color='white'))
    print('')

    print("测试背景色")
    print(UseStyle('黑色', font_color='black', back_color=color_black), )
    print(UseStyle('红色', font_color='black', back_color='red'), )
    print(UseStyle('绿色', font_color='black', back_color='green'), )
    print(UseStyle('黄色', font_color='black', back_color='yellow'), )
    print(UseStyle('蓝色', font_color='black', back_color='blue'), )
    print(UseStyle('紫红色', font_color='black', back_color='purple'), )
    print(UseStyle('青蓝色', font_color='black', back_color='cyan'), )
    print(UseStyle('白色', font_color='black', back_color='white'))
    print('')


if __name__ == '__main__':
    test_de_color()
    # exp_plot_tree()
    # TestColor()
