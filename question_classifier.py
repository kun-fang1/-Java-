# coding: utf-8
import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        #　特征词路径
        self.chapter_path = os.path.join(cur_dir, 'dict/chapter.txt')
        self.knowledge_path = os.path.join(cur_dir, 'dict/knowledge.txt')
        self.education_path = os.path.join(cur_dir, 'dict/education.txt')
        self.skill_path = os.path.join(cur_dir, 'dict/skill.txt')
        self.material_path = os.path.join(cur_dir, 'dict/material.txt')

        # 加载特征词
        self.chapter_wds= [i.strip() for i in open(self.chapter_path, encoding="utf-8") if i.strip()]
        self.knowledge_wds= [i.strip() for i in open(self.knowledge_path, encoding="utf-8") if i.strip()]
        self.education_wds= [i.strip() for i in open(self.education_path, encoding="utf-8") if i.strip()]
        # self.skill_wds= [i.strip() for i in open(self.skill_path, encoding="utf-8") if i.strip()]
        self.material_wds= [i.strip() for i in open(self.material_path, encoding="utf-8") if i.strip()]
        self.region_words = set(self.knowledge_wds + self.chapter_wds + self.education_wds + self.material_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdchapter_dict = self.build_wdtype_dict()
        # 问句疑问词
        # self.chapter_qwds = ['']
        self.education_qwds = ['德育','思政元素']
        self.knowledge_qwds = ['知识', '教学内容']
        self.skill_qwds = ['技能','教学目标']
        self.material_qwds = ['素材','案例']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        entity_dict = self.check_medical(question)
        if not entity_dict:
            return {}
        data['args'] = entity_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in entity_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 知识-德育点
        if self.check_words(self.education_qwds, question) and ('knowledge' in types):
            question_type = 'knowledge_education'
            question_types.append(question_type)

        # 知识点
        if self.check_words(self.knowledge_qwds, question) and ('chapter' in types):
            question_type = 'chapter_knowledge'
            question_types.append(question_type)
        # 技能点
        if self.check_words(self.skill_qwds, question) and ('chapter' in types):
            question_type = 'chapter_skill'
            question_types.append(question_type)
        # 素材点
        if self.check_words(self.material_qwds, question) and ('chapter' in types):
            question_type = 'chapter_material'
            question_types.append(question_type)

        if question_types == [] and 'chapter' in types:
            question_types = ['chapter_knowledge']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.chapter_wds:
                wd_dict[wd].append('chapter')
            if wd in self.knowledge_wds:
                wd_dict[wd].append('knowledge')
            if wd in self.education_wds:
                wd_dict[wd].append('education')

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
        final_dict = {i:self.wdchapter_dict.get(i) for i in final_wds}

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