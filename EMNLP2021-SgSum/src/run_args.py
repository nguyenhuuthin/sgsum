#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""All args for running all models"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from utils.args import ArgumentGroup

# yapf: disable
parser = argparse.ArgumentParser(__doc__)
model_g = ArgumentGroup(parser, "model", "model configuration and paths.")
model_g.add_arg("model_name", str, "seq2seq", "type of model to run",
                choices=["seq2seq", "graphsum", "roberta_graphsum", "ernie_graphsum", "ernie_seq2seq", "multigraphsum"])
model_g.add_arg("config_path", str, None, "Path to the json file for transformer seq2seq model config.")
model_g.add_arg("init_checkpoint", str, None, "Init checkpoint to resume training from.")
model_g.add_arg("init_pretraining_params", str, None,
                "Init pre-training params which preforms fine-tuning from. If the "
                "arg 'init_checkpoint' has been set, this argument wouldn't be valid.")
model_g.add_arg("checkpoints", str, "checkpoints", "Path to save checkpoints.")
model_g.add_arg("weight_sharing", bool, True, "If set, share weights between word embedding and masked lm.")

run_type_g = ArgumentGroup(parser, "run_type", "running type options.")
run_type_g.add_arg("use_cuda", bool, True, "If set, use GPU for training.")
run_type_g.add_arg("is_distributed", bool, False, "If set, then start distributed training.")
run_type_g.add_arg("use_fast_executor", bool, False, "If set, use fast parallel executor (in experiment).")
run_type_g.add_arg("num_iteration_per_drop_scope", int, 10, "Iteration intervals to drop scope.")
run_type_g.add_arg("do_train", bool, True, "Whether to perform training.")
run_type_g.add_arg("do_val", bool, True, "Whether to perform evaluation on dev data set.")
run_type_g.add_arg("do_test", bool, True, "Whether to perform evaluation on test data set.")
run_type_g.add_arg("use_multi_gpu_test", bool, False, "Whether to perform evaluation using multiple gpu cards")
run_type_g.add_arg("metrics", bool, True, "Whether to perform evaluation on test data set.")
run_type_g.add_arg("stream_job", str, None, "if not None, then stream finetuning task by job id.")

log_g = ArgumentGroup(parser, "logging", "logging related.")
log_g.add_arg("skip_steps", int, 100, "The steps interval to print loss.")
log_g.add_arg("verbose", bool, False, "Whether to output verbose log.")
log_g.add_arg("log_file", str, "log/graphsum.log", "Path to save log.")

train_g = ArgumentGroup(parser, "training", "training options.")
train_g.add_arg("epoch", int, 100, "Number of epoches for fine-tuning.")
train_g.add_arg("label_smooth_eps", float, 0.1, "label smooth epsilion.")
train_g.add_arg("learning_rate", float, 2.0, "Learning rate used to train with warmup.")
train_g.add_arg("lr_scheduler", str, "linear_warmup_decay",
                "scheduler of learning rate.", choices=['linear_warmup_decay', 'noam_decay'])
train_g.add_arg("weight_decay", float, 0.01, "Weight decay rate for L2 regularizer.")
train_g.add_arg("warmup_proportion", float, 0.1,
                "Proportion of training steps to perform linear learning rate warmup for.")
train_g.add_arg("warmup_steps", int, 4000, "The training steps to perform linear learning rate warmup.")
train_g.add_arg("eps", float, 1e-8, "epsilon for Adam optimizer")
train_g.add_arg("beta1", float, default=0.9, help="for Adam optimizer")
train_g.add_arg("beta2", float, default=0.998, help="for Adam optimizer")
train_g.add_arg("save_steps", int, 10000, "The steps interval to save checkpoints.")
train_g.add_arg("validation_steps", int, 10000, "The steps interval to evaluate model performance.")
train_g.add_arg("use_fp16", bool, False, "Whether to use fp16 mixed precision training.")
train_g.add_arg("use_dynamic_loss_scaling", bool, False, "Whether to use dynamic loss scaling.")
train_g.add_arg("init_loss_scaling", float, 1.0,
                "Loss scaling factor for mixed precision training, only valid when use_fp16 is enabled.")
train_g.add_arg("incr_every_n_steps", int, 100, "Increases loss scaling every n consecutive.")
train_g.add_arg("decr_every_n_nan_or_inf", int, 2,
                "Decreases loss scaling every n accumulated steps with nan or inf gradients.")
train_g.add_arg("incr_ratio", float, 2.0,
                "The multiplier to use when increasing the loss scaling.")
train_g.add_arg("decr_ratio", float, 0.8,
                "The less-than-one-multiplier to use when decreasing.")
train_g.add_arg("grad_norm", float, 2.0, "The max norm of graident.")
train_g.add_arg("beam_size", int, 5, "for seq2seq task.")
train_g.add_arg("do_dec", bool, False, "for seq2seq task.")
train_g.add_arg("report_rouge", bool, False, "calculate rouge scores.")
train_g.add_arg("report_orcale", bool, False, "calculate orcale rouge scores.")
train_g.add_arg("evaluate_blue", bool, False, "calculate blue scores.")
train_g.add_arg("len_penalty", float, default=0.6, help="length penalty during decoding.")
train_g.add_arg("max_out_len", int, 300, "max length of decoding.")
train_g.add_arg("min_out_len", int, 200, "min length of decoding.")
train_g.add_arg("block_trigram", bool, False, "remove repeated trigrams in summary.")

data_g = ArgumentGroup(parser, "data", "Data paths, vocab paths and data processing options")
data_g.add_arg("train_set", str, None, "Path to training data.")
data_g.add_arg("test_set", str, None, "Path to test data.")
data_g.add_arg("dev_set", str, None, "Path to validation data.")
data_g.add_arg("vocab_path", str, None, "Vocabulary path.")
data_g.add_arg("max_tgt_len", int, 300, "the number of tokens in target summaries.")
data_g.add_arg("batch_size", int, 4096, "Total examples' number in batch for training. see also --in_tokens.")
data_g.add_arg("in_tokens", bool, False,
               "If set, the batch size will be the maximum number of tokens in one batch. "
               "Otherwise, it will be the maximum number of examples in one batch.")
data_g.add_arg("do_lower_case", bool, True,
               "Whether to lower case the input text. Should be True for uncased models and False for cased models.")
data_g.add_arg("random_seed", int, 0, "Random seed.")
data_g.add_arg("decode_path", str, "", "path to decode")

transformer_g = ArgumentGroup(parser, "transformer args", "transformer options.")
transformer_g.add_arg("max_seq_len", int, 512, "Number of words of the longest seqence.")

graphsum_g = ArgumentGroup(parser, "graphsum args", "graphsum options.")
graphsum_g.add_arg("pos_win", float, 2.0, "the parameter in graph attention.")
graphsum_g.add_arg("max_para_len", int, 512, "Number of words in longest paragraph.")
graphsum_g.add_arg("max_para_num", int, 100, "Number of paragraphs of the longest documents.")
graphsum_g.add_arg("max_doc_num", int, 20, "Number of docs of the multi-doc articles.")
graphsum_g.add_arg("graph_type", str, "similarity", "type of graph",
                   choices=["similarity", "topic", "discourse"])
# for rank opt
graphsum_g.add_arg("candidate_summary_num", int, 10, "Number of candidate summary in ranking opt")
graphsum_g.add_arg("candidate_sentence_num", int, 5, "Number of candidate sentence")
graphsum_g.add_arg("selected_sentence_num", int, 3, "Number of selected sentence in predict summary")

# for roberta
roberta_graphsum_g = ArgumentGroup(parser, "roberta args", "roberta options.")
roberta_graphsum_g.add_arg("roberta_vocab_file", str, 'roberta_config/vocab.txt', "roberta vocab")
roberta_graphsum_g.add_arg("encoder_json_file", str, 'roberta_config/encoder.json', 'bpt map')
roberta_graphsum_g.add_arg("vocab_bpe_file", str, 'roberta_config/vocab.bpe', "vocab bpe")
roberta_graphsum_g.add_arg("use_interval", bool, False, "whether model interval")
roberta_graphsum_g.add_arg("roberta_config_path", str, "roberta_config/roberta_config.json",
                           "The file to save roberta configuration.")

# for ernie
ernie_graphsum_g = ArgumentGroup(parser, "ernie args", "ernie options.")
ernie_graphsum_g.add_arg("ernie_vocab_file", str, 'ernie_config/vocab.txt', "ernie vocab")
ernie_graphsum_g.add_arg("ernie_config_path", str, "ernie_config/ernie_config.json",
                         "The file to save ernie configuration.")
# yapf: enable
