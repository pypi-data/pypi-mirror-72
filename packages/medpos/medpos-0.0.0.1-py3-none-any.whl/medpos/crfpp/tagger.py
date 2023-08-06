import os
import time
import codecs
import optparse 
import pickle

import numpy as np
import pandas as pd

from .crftools import get_sent_strfeats, crf_test
from .evals import read_target_seq, extractSET
from .nlptext_lite.sentence import Sentence





def medpos_tagger(sent, 
                  model = None, 
                  Channel_Settings = None, 
                  get_seq = False, 
                  get_entities = True, 
                  name = '1'):
    
    '''
        basically from crf_test
        sent: a sentence, could be without annotation
    '''

    current_dir_old = os.path.abspath(os.path.dirname(__file__))
    current_dir, _ = os.path.split(current_dir_old)
    model = 'model/MedPos/char/T_b-n1t1-f1_m-n1t1-f1_r-n1t1-f1_P-bio_E-bio'
    model = os.path.join(current_dir, model)
    # print(model)

    sent = Sentence(sentence=[i.replace(' ', '@') for i in sent], tokenLevel= 'char')
    # model = model + '_' + str(cross_idx)
    if not Channel_Settings:
        with open(model + '/para.p', 'rb') as f:
            Channel_Settings = pickle.load(f)
    # 1. get sentence feats
    # hopefully, the model_config is included in model_path
    # if not os.path.exists():

    feats_data_path   = os.path.join(current_dir, name + '_tagger_feats.txt') 
    results_data_path = os.path.join(current_dir, name + '_tagger_results.txt') 
    model_path = model + '/model'
    # print(feats_data_path)

    # get Channel_Settings
    # get use sent strfeats or sent vecfeats settings
    df = get_sent_strfeats(sent, Channel_Settings, train = False)
    # print(df)
    df.to_csv(feats_data_path, sep = '\t', encoding = 'utf=8', header = False, index = False )
    # 2. save the sentence feats to a file
    
    # 3. tag a sentence
    crf_test(feats_data_path, model_path, results_data_path)

    # 4. read and parse the result to pred_SSET
    # get a tag_seq
    # list of tuple (score, result)

    tag_seq  = read_target_seq(results_data_path)
    if get_seq: 
        return tag_seq
    else:
        pred_SET = extractSET(tag_seq)
        return pred_SET

