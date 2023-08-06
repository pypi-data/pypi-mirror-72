#encoding:utf-8
import json
from collections import defaultdict

def format_result(result,words,name):
    '''
    形式调整
    :param result:
    :param words:
    :return:
    '''
    entities = defaultdict(list)
    entities['text'] = "".join(words)
    if len(result) == 0:
        entities['info'] = result
    else:
        for record in result:
            begin = record['begin']
            end  = record['end']
            if (name == 'CWS'):
                record['type'] = 'word'
            entities['info'].append({
                'start':begin+1,
                'end':end+1,
                'word': "".join(words[begin:end + 1]),
                'type':record['type']
            })
    return entities

def get_entity(path,tag_map):
    results = []
    record = {}
    for index,tag_id in enumerate(path):
        
        if tag_id == 0: # 0是我们的pad label
            continue
        tag = tag_map[tag_id]
        if tag.startswith("B_"):
            if record.get('end'):
                if (record['type']=='T'):
                    continue
                results.append(record)
            record = {}
            record['begin'] = index
            record['type'] = tag.split('_')[1]
        elif tag.startswith('I_') and record.get('begin') != None:
            tag_type = tag.split('_')[1]
            if tag_type == record['type']:
                record['end'] = index
        else:
            if record.get('end'):
                if (record['type']=='T'):
                    continue
                results.append(record)
            record = {}
    return results
def get_word(path):

    results = []
    record = {}

    for index,tag_id in enumerate(path):
        
        if tag_id == 0: # 0是我们的pad label
            continue
        if tag_id == 1:
            if (record.get('begin')):
                record['end']=index-1
                results.append(record)
                record={}
            record['begin'] = index
        elif tag_id == 2:
            pass
        else:
            if (record.get('begin')):
                record['end']=index-1
                results.append(record)
                record={}
            results.append({'begin':index,'end':index})

    if (record.get('begin')):
        record['end']=len(path)-1
        results.append(record)
        record={}


    return results

def test_write(data,filename,raw_text_path, name):
    '''
    将test结果保存到文本中，这里是以json格式写入
    :param data:
    :param filename:
    :param raw_text_path:
    :return:
    '''
    with open(raw_text_path,'r') as fr,open(filename,'w',encoding='utf-8') as fw:
        for text,result in zip(fr.readlines(),data):
            words = text.strip()
            words = words.split(' ')
            record = format_result(result,words,name)

            
            encode_json = json.dump(record,fw,ensure_ascii=False)
            print('\n',end='',file=fw)
            #data = encode_json.encode('utf-8').decode('utf-8')
            #print(json.loads(encode_json))
            #print(data, file=fw)
