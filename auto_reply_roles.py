# encoding: utf-8
"""自动回复的规则"""
import json
import os

base_dir = os.path.dirname(os.path.realpath(__file__))
white_path = os.path.join(base_dir, 'white.json')


class Role():
    name_dic = dict()
    with open(white_path, 'r', encoding='utf-8')as f :
        name_dic = json.loads(f.read(), encoding='utf-8')

    def save_json(self, name_dic) :
        with open(white_path, 'w', encoding='utf-8')as f :
            json.dump(name_dic, f, ensure_ascii=False, indent=4)

    def add_name(cls, name) :
        if name not in Role().name_dic:
            Role().name_dic[name] = 1
            cls.save_json(Role().name_dic)

    def del_name(cls, name) :
        if name in Role().name_dic:
            del Role().name_dic[name]
            cls.save_json(Role().name_dic)

    def in_white_names(cls, name):
        if name in Role().name_dic:
            return True
        return False

if __name__ =='__main__':
    Role().add_name('林林')
    print(Role().in_white_names('林林'))

