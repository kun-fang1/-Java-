# coding: utf-8

import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/思政元素数据.json')
        self.g = Graph('http://localhost:7474', auth = ('neo4j', '123456'))

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        knowledge = []  # 知识点
        chapter = []  # 章节
        education = []  # 德育点
        skill = []  # 技能点
        material = []  # 素材
        dagang = []  # 大纲
        chapter_info = []

        # 构建节点实体关系

        rels_knowledge = []
        rels_education = []
        rels_skill = []
        rels_material = []
        rels_dagang = []

        count = 0
        with open(self.data_path, 'r', encoding='utf-8') as f:
            # file_dict = {}
            count += 1
            print(count)
            content = f.readlines()
            for data in content:
                chapter_dict = {}
                data_json = json.loads(data)
                a = data_json['章节']
                chapter_dict['章节标题'] = data_json['章节标题']
                chapter_dict['章节'] = a
                chapter_info.append(chapter_dict)
                chapter.append(a)

                b = data_json['课程知识点']
                knowledge.append(b)
                rels_knowledge.append([a, b])

                c = data_json['德育点']
                education.append(c)
                rels_education.append([b, c])

                d = data_json['技能点']
                skill.append(d)
                rels_skill.append([a, d])

                e = data_json['课程思政教学素材']
                material.append(e)
                rels_material.append([a, e])

                f = data_json['教学大纲']
                dagang.append(f)
                rels_dagang.append([f, a])
            # chapter_infos.append(chapter_dict)
        chapter_infos = []
        for i in range(0, len(chapter_info)):
            if chapter_info[i] not in chapter_info[i + 1:]:
                chapter_infos.append(chapter_info[i])
        print(chapter_infos)

        return set(knowledge), set(chapter), set(education), set(skill), set(material), set(dagang), chapter_infos, rels_knowledge, rels_education, rels_skill, rels_material, rels_dagang

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱章节的节点'''
    def create_chapter_nodes(self, names_infos):
        count = 0
        for names_dict in names_infos:
            # if 'StudentNo' in names_dict:
            node = Node("Chapter", name=names_dict['章节'], **names_dict)
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Knowledge, Chapter, Education, Skill, Material, Dagang, chapter_infos, rels_knowledge, rels_education, rels_skill, rels_material, rels_dagang = self.read_nodes()
        # self.create_node(file_infos)
        self.create_chapter_nodes(chapter_infos)
        self.create_node('Knowledge', Knowledge)
        print(len(Knowledge))
        self.create_node('Education', Education)
        print(len(Education))
        self.create_node('Skill', Skill)
        print(len(Skill))
        self.create_node('Material', Material)
        print(len(Material))
        self.create_node('Dagang', Dagang)
        print(len(Material))
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        Knowledge, Chapter, Education, Skill, Material, Dagang, chapter_infos, rels_knowledge, rels_education, rels_skill, rels_material, rels_dagang = self.read_nodes()
        self.create_relationship('Chapter', 'Knowledge', rels_knowledge, '知识点', '知识点')
        self.create_relationship('Knowledge', 'Education', rels_education, '德育点', '德育点')
        self.create_relationship('Chapter', 'Skill', rels_skill, '技能点', '技能点')
        self.create_relationship('Chapter', 'Material', rels_material, '教学素材', '教学素材')
        self.create_relationship('Dagang', 'Chapter', rels_dagang, '包含章节', '包含章节')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_file, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_file, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_file, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Knowledge, Chapter, Education, Skill, Material, Dagang, chapter_infos, rels_knowledge, rels_education, rels_skill, rels_material, rels_dagang = self.read_nodes()
        f_knowledge = open('knowledge.txt', 'w+', encoding='utf-8')
        f_chapter = open('chapter.txt', 'w+', encoding='utf-8')
        f_education = open('education.txt', 'w+', encoding='utf-8')
        f_skill = open('education.txt', 'w+', encoding='utf-8')
        f_material = open('material.txt', 'w+', encoding='utf-8')

        f_knowledge.write('\n'.join(list(Knowledge)))
        f_chapter.write('\n'.join(list(Chapter)))
        f_education.write('\n'.join(list(Education)))
        f_skill.write('\n'.join(list(Skill)))
        f_material.write('\n'.join(list(Material)))
        f_knowledge.close()
        f_chapter.close()
        f_education.close()
        f_skill.close()
        f_material.close()
        return


if __name__ == '__main__':
    handler = MedicalGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()
    # handler.export_data()
    
