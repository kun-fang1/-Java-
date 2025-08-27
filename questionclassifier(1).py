# coding: utf-8
import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        #　特征词路径
        self.name_path = os.path.join(cur_dir, 'dict/name.txt')
        self.thing_path = os.path.join(cur_dir, 'dict/thing.txt')
        # self.education_path = os.path.join(cur_dir, 'dict/education.txt')
        # self.skill_path = os.path.join(cur_dir, 'dict/skill.txt')
        # self.material_path = os.path.join(cur_dir, 'dict/material.txt')

        # 加载特征词
        self.name_wds= [i.strip() for i in open(self.name_path, encoding="utf-8") if i.strip()]
        self.thing_wds= [i.strip() for i in open(self.thing_path, encoding="utf-8") if i.strip()]
        # self.education_wds= [i.strip() for i in open(self.education_path, encoding="utf-8") if i.strip()]
        # # self.skill_wds= [i.strip() for i in open(self.skill_path, encoding="utf-8") if i.strip()]
        # self.material_wds= [i.strip() for i in open(self.material_path, encoding="utf-8") if i.strip()]
        self.region_words = set(self.thing_wds + self.name_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdname_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.fu_qwds = ['父亲', '爸']
        self.zi_qwds = ['儿子', '孩子', '小孩']
        self.qi_qwds = ['妻子', '老婆']
        self.zhang_qwds = ['丈夫', '老公']
        self.shu_qwds = ['叔侄']
        self.fb_qwds = ['发布']
        self.js_qwds = ['介绍']


        self.time_qwds = ['时间', '时候']
        self.position_qwds = ['地点', '地址', '地方']
        self.event_qwds = ['经过']
        self.partake_qwds = ['参与者', '参加人', '参与人']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 知识-德育点
        if self.check_words(self.fu_qwds, question) and ('name' in types):
            question_type = 'name_fu'
            question_types.append(question_type)

        # 知识点
        if self.check_words(self.zi_qwds, question) and ('name' in types):
            question_type = 'name_zi'
            question_types.append(question_type)
        # 技能点
        if self.check_words(self.qi_qwds, question) and ('name' in types):
            question_type = 'name_qi'
            question_types.append(question_type)
        # 素材点
        if self.check_words(self.zhang_qwds, question) and ('name' in types):
            question_type = 'name_zhang'
            question_types.append(question_type)

        if self.check_words(self.shu_qwds, question) and ('name' in types):
            question_type = 'name_shu'
            question_types.append(question_type)
        # 技能点
        if self.check_words(self.fb_qwds, question) and ('name' in types):
            question_type = 'name_fb'
            question_types.append(question_type)
        # 素材点
        if self.check_words(self.js_qwds, question) and ('name' in types):
            question_type = 'name_js'
            question_types.append(question_type)

        # 素材点
        if self.check_words(self.time_qwds, question) and ('thing' in types):
            question_type = 'thing_time'
            question_types.append(question_type)

        # 素材点
        if self.check_words(self.position_qwds, question) and ('thing' in types):
            question_type = 'thing_position'
            question_types.append(question_type)

        # 素材点
        if self.check_words(self.event_qwds, question) and ('thing' in types):
            question_type = 'thing_event'
            question_types.append(question_type)

        # 素材点
        if self.check_words(self.partake_qwds, question) and ('thing' in types):
            question_type = 'thing_partake'
            question_types.append(question_type)

        if question_types == [] and 'name' in types:
            question_types = ['name_thing']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.name_wds:
                wd_dict[wd].append('name')
            if wd in self.thing_wds:
                wd_dict[wd].append('thing')


        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdname_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)