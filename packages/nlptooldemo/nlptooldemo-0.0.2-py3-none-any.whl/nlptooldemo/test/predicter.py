#encoding:utf-8
import torch
from torch.autograd import Variable
from tqdm import tqdm
from .predict_utils import get_entity, get_word
from ..train.train_utils import restore_checkpoint,model_device
from ..train.trainer import batchify_with_label
from ..config.new_config import configs as config

class Predicter(object):
    def __init__(self,
                 model,
                 model_name,
                 test_data,
                 logger,
                 label_to_id,
                 checkpoint_path,
                 n_gpu = 0,
                 distributed = True):
        self.model           = model
        self.model_name      = model_name
        self.test_data       = test_data
        self.logger          = logger
        self.checkpoint_path = checkpoint_path
        self.n_gpu           = n_gpu
        self.task={0:10,1:3}
        self.id2name = {0:"NER",1:"CWS"}
        self.id_to_label      = {value:key for key, value in label_to_id.items()}

    def sequence_mask(self, sequence_length, max_len): 
        batch_size = sequence_length.size(0)            
        seq_range = torch.arange(0, max_len).long()
        seq_range_expand = seq_range.unsqueeze(0).expand(batch_size, max_len)
        seq_range_expand = Variable(seq_range_expand)
        if sequence_length.is_cuda:
            seq_range_expand = seq_range_expand.cuda()
        seq_length_expand = (sequence_length.unsqueeze(1).expand_as(seq_range_expand))
        return seq_range_expand < seq_length_expand 
        


    def _predict_batch(self,inputs,gaz,length, task_number, task):
        with torch.no_grad():
            masks = self.sequence_mask(length, config['max_length']) if ('bert' in self.model_name) else None
            outputs = self.model(inputs, length,task_number,masks, gaz)
            mask, _ = batchify_with_label(inputs=inputs, outputs=outputs,is_train_mode=False)
            _,predicts = self.model.crf(outputs, mask, out_number = task_number)

            batch_result = []
            for index,(text,path) in enumerate(zip(inputs,predicts)):
                try:
                    path = path.cpu().numpy()
                except:
                    pass
                result = get_entity(path = path,tag_map=self.id_to_label) if (task=='NER') else get_word(path=path)
                batch_result.append(result)
            return batch_result

    def predict(self):
        self.model.eval()
        predictions = []
        taskDict = {}
        for idx,(inputs,gaz,target,length,source) in enumerate(self.test_data):
            check = sum(source.numpy().tolist())
            if (check%len(self.task.keys())!=0):
                continue
            inputs = (torch.stack(inputs,dim=0)).t().cuda()
            length = length.cuda()
            batch_size = inputs.size(0)
            cur_task = self.task[check/batch_size]
            cur_name = self.id2name[check/batch_size]


            y_pred_batch = self._predict_batch(inputs = inputs,length = length, gaz = gaz, task_number = cur_task, task=cur_name)
            if (check/batch_size in taskDict.keys()):
                predictions[taskDict[check/batch_size]].extend(y_pred_batch)
            else:
                d = len(taskDict.keys())
                taskDict[check/batch_size]=d
                predictions.append([])
                predictions[taskDict[check/batch_size]].extend(y_pred_batch)
        return predictions