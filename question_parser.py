# coding: utf-8
class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'knowledge_education':
                sql = self.sql_transfer(question_type, entity_dict.get('knowledge'))

            elif question_type == 'chapter_knowledge':
                sql = self.sql_transfer(question_type, entity_dict.get('chapter'))
                
            elif question_type == 'chapter_skill':
                sql = self.sql_transfer(question_type, entity_dict.get('chapter'))

            elif question_type == 'chapter_material':
                sql = self.sql_transfer(question_type, entity_dict.get('chapter'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        if question_type == 'knowledge_education':
            sql = ["MATCH (m:Knowledge)-[r:德育点]->(n:Education) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'chapter_knowledge':
            sql = ["MATCH (m:Chapter)-[r:知识点]->(n:Knowledge) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'chapter_skill':
            sql = ["MATCH (m:Chapter)-[r:技能点]->(n:Skill) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'chapter_material':
            sql = ["MATCH (m:Chapter)-[r:教学素材]->(n:Material) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
