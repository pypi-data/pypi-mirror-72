#encoding:utf-8
from os import path
import multiprocessing
import os

BASE_DIR = 'nlptooldemo'
RE = {
'pretrained_model_path' :os.path.join(BASE_DIR, '../../bert/pretrained_models/bert-base-chinese'),
'train_file' : os.path.join(BASE_DIR, 'dataset/REdataset/train_small.jsonl'),
'validation_file' : os.path.join(BASE_DIR, 'dataset/REdataset/val_small.jsonl'),
'output_dir' : os.path.join(BASE_DIR, 'dataset/REdataset/saved_models'),
'tagset_file' : os.path.join(BASE_DIR, 'dataset/REdataset/relation.txt'),
'max_len':128,
'ner_source': path.sep.join([BASE_DIR, 'output/result/predict_result.txt']),
'checkpoint':path.sep.join([BASE_DIR,'output/RE_checkpoint/re-best.pth']),
'result':path.sep.join([BASE_DIR,'output/re.txt']),
'dataset':os.path.join(BASE_DIR,'dataset')
}
configs = {
    'all_data_path': [path.sep.join([BASE_DIR,'dataset/raw/msra_source_train.txt']),path.sep.join([BASE_DIR,'dataset/raw/pku_cws_source.txt']),path.sep.join([BASE_DIR,'dataset/raw/msr_cws_source.txt']) ],  
    'pretrained_path':path.sep.join([BASE_DIR, 
                                            'output/checkpoints/roberta.zip']),# for word embedding
    'test_file_path': path.sep.join([BASE_DIR,'dataset/processed/test.json']),   
    'embedding_weight_path': path.sep.join([BASE_DIR, 
                                            'output/embedding/sgns300']), # for character embedding
    'embedding_dict_path': path.sep.join([BASE_DIR, 
                                            'output/embedding/sgns300']),# for word embedding
    'vocab_path': path.sep.join([BASE_DIR,'dataset/processed/vocab.pkl']), 
    'rev_vocab_path': path.sep.join([BASE_DIR,'dataset/processed/rev_vocab.pkl']), 

    'log_dir': path.sep.join([BASE_DIR, 'output/log']), 
    'writer_dir': path.sep.join([BASE_DIR, 'output/TSboard']),
    'figure_dir': path.sep.join([BASE_DIR, 'output/figure']),
    'checkpoint_dir': path.sep.join([BASE_DIR, 'output/checkpoints/bilstm_crf']),
    'embedding_dir': path.sep.join([BASE_DIR, 'output/embedding']),

    'valid_size': 0.1, 
    'min_freq': 1,   
    'max_length': 80,  
    'max_features': 100000, 
    'embedding_dim':300, 

    'batch_size': 32,  
    'epochs': 100,    
    'start_epoch': 1,
    'learning_rate': 3e-5, #for bert
    'weight_decay': 5e-4, 
    'n_gpus': [0], 
    'x_var':'source', 
    'y_var':'target', 
    'num_workers': multiprocessing.cpu_count(), 
    'seed': 2018, 
    'lr_patience': 5, 
    'mode': 'min',    
    'monitor': 'val_loss',  
    'early_patience': 10,   
    'save_best_only':True, 
    'best_model_name': '{arch}-best-re.pth', 
    'epoch_model_name': '{arch}-{epoch}-{val_loss}.pth', 
    'save_checkpoint_freq': 10,

    'multi-task':
    [

  {    'label_to_id': {
  
        "B_PER": 1,  
        "I_PER": 2,
        "B_LOC": 3, 
        "I_LOC": 4,
        "B_ORG": 5,  
        "I_ORG": 6,
        "B_T":7,
        "I_T":8,
        "O": 9 

  },
    'num_tag':10,
    'raw_train_path': path.sep.join([BASE_DIR,'dataset/raw/boson_ner_source.txt']),  
    'raw_target_path': path.sep.join([BASE_DIR,'dataset/raw/boson_ner_target.txt']), 
    'raw_test_path': path.sep.join([BASE_DIR,'dataset/raw/test.txt']),       
    'test_file_path': path.sep.join([BASE_DIR,'dataset/processed/test.json']),   
    'result_path': path.sep.join([BASE_DIR, 'output/result/predict_result.txt']),
    'x_var':'source', 
    'y_var':'target',
    'train_file_path': path.sep.join([BASE_DIR,'dataset/processed/train.json']), 
    'valid_file_path': path.sep.join([BASE_DIR,'dataset/processed/valid.json']),
    'name':"NER"
    }

    ],
    'seed':2018,
    'resume':False,
    'model':{'name':'bert_lstm'
    },
    
    'models': {
    'bert_lstm':{'hidden_size': 200,
                              'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':True},
    'roberta_lstm':{'hidden_size': 200,
                              'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':True},
    'lattice_lstm':{'hidden_size': 200,
                             'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':True},
    'cnn_crf':{'hidden_size': 200,
                             'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':True},
    'bilstm':{'hidden_size': 200,
                             'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':False},
    'bilstm_crf':{'hidden_size': 200,
                         'bi_tag': True,
                             'dropout_p':0.5,
                             'dropout_emb':0.0,
                             'num_layer': 1,
                             'use_cuda':True,
                             'crf':True}
              }
}
