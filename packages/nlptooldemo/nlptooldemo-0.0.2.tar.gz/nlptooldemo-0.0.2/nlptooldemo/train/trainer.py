#encoding:utf-8
import os
import sys
import time
import numpy as np
import torch
from itertools import chain
from torch.autograd import Variable
from ..callback.progressbar import ProgressBar
from ..utils.utils import AverageMeter
from .train_utils import restore_checkpoint,model_device
from .metrics import Entity_Score
from .train_utils import batchify_with_label
from ..config.new_config import configs as config


class Trainer(object):
    def __init__(self,model,
                 model_name,
                 train_data,
                 val_data,
                 optimizer,
                 epochs,
                 logger,
                 evaluate,
                 num_tasks = 1,
                 device = None,
                 avg_batch_loss   = False,
                 distributed = True,
                 label_to_id      = None,
                 n_gpu            = None,
                 lr_scheduler     = None,
                 resume           = None,
                 model_checkpoint = None,
                 writer           = None,
                 verbose = 1):
        self.model            = model     
        self.model_name       = model_name      
        self.train_data       = train_data         
        self.val_data         = val_data          
        self.epochs           = epochs          
        self.optimizer        = optimizer   
        self.logger           = logger        
        self.verbose          = verbose            
        self.writer           = writer         
        self.resume           = resume           
        self.model_checkpoint = model_checkpoint 
        self.lr_scheduler     = lr_scheduler     
        self.evaluate         = evaluate         
        self.n_gpu            = n_gpu             
        self.avg_batch_loss   = avg_batch_loss     
        self.num_tasks        = num_tasks
        self.task={0:10,1:3}
        self.id_to_label      = {value:key for key, value in label_to_id.items()}
        self._reset()
        self.device = device

    def _reset(self):

        self.train_entity_score = Entity_Score(id_to_label=self.id_to_label)
        self.val_entity_score   = Entity_Score(id_to_label=self.id_to_label)

        self.batch_num         = len(self.train_data)
        self.progressbar       = ProgressBar(n_batch = self.batch_num,eval_name='acc',loss_name='loss')
        self.model,self.device = model_device(n_gpu=self.n_gpu,model = self.model,logger = self.logger)
        self.start_epoch = 1

        if self.resume:
            arch = self.model_checkpoint.arch
            resume_path = os.path.join(self.model_checkpoint.checkpoint_dir.format(arch = arch),
                                       self.model_checkpoint.best_model_name.format(arch = arch))
            self.logger.info("\nLoading checkpoint: {} ...".format(resume_path))
            resume_list = restore_checkpoint(resume_path = resume_path,model = self.model,optimizer = self.optimizer)
            self.model     = resume_list[0]
            self.optimizer = resume_list[1]
            best           = resume_list[2]
            self.start_epoch = resume_list[3]
        

            if self.model_checkpoint:
                self.model_checkpoint.best = best
            self.logger.info("\nCheckpoint '{}' (epoch {}) loaded".format(resume_path, self.start_epoch))

    def summary(self):
        model_parameters = filter(lambda p: p.requires_grad, self.model.module.parameters())

        params = sum([np.prod(p.size()) for p in model_parameters])

        self.logger.info('trainable parameters: {:4}M'.format(params / 1000 / 1000))



    def _save_info(self,epoch,val_loss):
        state = {
            'epoch': epoch,
            'arch': self.model_checkpoint.arch,
            'state_dict': self.model.module.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'val_loss': round(val_loss,4)
        }
        return state
        
    def sequence_mask(self, sequence_length, max_len, device=None):   # sequence_length :(batch_size, )
        batch_size = sequence_length.size(0)     
        seq_range = torch.arange(0, max_len).long()
        seq_range_expand = seq_range.unsqueeze(0).expand(batch_size, max_len)
        seq_range_expand = Variable(seq_range_expand)
        if sequence_length.is_cuda:
            seq_range_expand = seq_range_expand.cuda()
        seq_length_expand = (sequence_length.unsqueeze(1).expand_as(seq_range_expand))
        return seq_range_expand < seq_length_expand 

    def _valid_epoch(self):
        self.model.module.eval()
        val_losses_ner = AverageMeter()
        val_losses_cws = AverageMeter()#!
        val_acc_ner    = AverageMeter()
        val_acc_cws = AverageMeter()#!
        val_f1     = AverageMeter()
        
        

        for idx,(inputs,gaz,target,length,source) in enumerate(self.val_data):
            check = sum(source.numpy().tolist())
            if (check%self.num_tasks!=0):
                continue

            inputs = (torch.stack(inputs,dim=0)).t().cuda()

            target = (torch.stack(target,dim=0)).t().cuda()

            batch_size = inputs.size(0)

            masks = self.sequence_mask(length, config['max_length'],self.device) if ('bert' in self.model_name) else None
            train_task = self.task[check/batch_size]

            outputs = self.model(inputs, length ,out_number = train_task, masks=masks, gaz=gaz)
            mask,target = batchify_with_label(inputs = inputs,target = target,outputs = outputs)
            loss = self.model.module.crf.neg_log_likelihood_loss(outputs, mask,target,out_number = train_task) 
            if self.avg_batch_loss:
                loss /=  batch_size
            _,predicts = self.model.module.crf(outputs, mask,out_number = train_task)
                    
            acc,f1 = self.evaluate(predicts,target=target)
            if (check/batch_size==0):
                val_losses_ner.update(loss.item(),batch_size)
                val_acc_ner.update(acc.item(),batch_size)

            else:
                val_losses_cws.update(loss.item(),batch_size)
                val_acc_cws.update(acc.item(),batch_size)
            val_f1.update(f1.item(),batch_size)
            if self.device != 'cpu':
                predicts = predicts.cpu().numpy()
                target = target.cpu().numpy()
            if (check/batch_size==0):
                self.val_entity_score.update(pred_paths=predicts, label_paths=target)


        return {
            'val_loss': val_losses_ner.avg,
            'val_loss2': val_losses_cws.avg,
            'val_acc': val_acc_ner.avg,
            'val_acc2': val_acc_cws.avg,
            'val_f1': val_f1.avg
        }



    def _train_epoch(self):
        self.model.module.train()
        train_loss_ner = AverageMeter()
        train_acc_ner  = AverageMeter()
        train_f1   = AverageMeter()
        train_loss_cws = AverageMeter()
        train_acc_cws  = AverageMeter()

                
        batch_loss_ner = 0
        acc_ner=0
        acc_cws=0
        batch_loss_cws = 0 


        for idx,(inputs,gaz,target,length,source) in enumerate(self.train_data):
            check = sum(source.numpy().tolist())
            if (check%self.num_tasks!=0):
                continue

            inputs = (torch.stack(inputs,dim=0)).t().cuda()
            target = (torch.stack(target,dim=0)).t().cuda()
            batch_size = inputs.size(0)
            train_task = self.task[check/batch_size]

           # gaz = gaz.cuda()        
 
            masks = self.sequence_mask(length, config['max_length'],self.device) if ('bert' in self.model_name) else None

            outputs = self.model(inputs, length, out_number = train_task, masks = masks, gaz=gaz)

            mask, target = batchify_with_label(inputs=inputs, target=target, outputs=outputs)
            loss    = self.model.module.crf.neg_log_likelihood_loss(outputs,mask,target, out_number = train_task)
            if self.avg_batch_loss:
                loss  /= batch_size
            _,predicts = self.model.module.crf(outputs,mask,out_number = train_task)
            acc,f1 = self.evaluate(predicts,target)

            if (not 'lattice' in self.model_name):
                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()
            else:
            	assert(1+1==3)
            if (check/batch_size==0):
                train_loss_ner.update(loss.item(),batch_size)
                train_acc_ner.update(acc.item(),batch_size)
                train_f1.update(f1.item(),batch_size)
            else:
                train_loss_cws.update(loss.item(),batch_size)
                train_acc_cws.update(acc.item(),batch_size)


            if self.device != 'cpu':
                predicts = predicts.cpu().numpy()
                target   = target.cpu().numpy()
                #self.train_entity_score.update(pred_paths=predicts,label_paths=target)
        
            if (self.verbose >= 1 and (not 'lattice' in self.model_name)):
                self.progressbar.step(batch_idx=idx,
                                      loss     = loss.item(),
                                      acc      = acc.item(),
                                      f1       = f1.item(),
                                      use_time = 0)

        train_log = {
            'loss': train_loss_ner.avg,
            'acc': train_acc_ner.avg,
            'loss2': train_loss_cws.avg,
            'acc2': train_acc_cws.avg,
            'f1': train_f1.avg,
        }
        return train_log

    def train(self):
        for epoch in range(self.start_epoch,self.start_epoch+self.epochs):
            print("----------------- training start -----------------------")
            print("Epoch {i}/{epochs}......".format(i=epoch, epochs=self.start_epoch+self.epochs -1))

            train_log = self._train_epoch()
            val_log = self._valid_epoch()

            logs = dict(train_log,**val_log)

            self.val_entity_score.result()
        
            
            self.logger.info('\nEpoch: %d - loss: %.4f acc: %.4f - f1: %.4f val_loss: %.4f - val_acc: %.4f - val_f1: %.4f - val_acc2: %.4f'%(
                            epoch,logs['loss'],logs['acc'],logs['f1'],logs['val_loss'],logs['val_acc'],logs['val_f1'],logs['val_acc2'])
                             )

            if self.lr_scheduler:
                self.lr_scheduler.step(logs['loss'],epoch)


            if self.model_checkpoint:
                state = self._save_info(epoch,val_loss = logs['val_loss'])
                self.model_checkpoint.step(current=logs[self.model_checkpoint.monitor],state = state)
