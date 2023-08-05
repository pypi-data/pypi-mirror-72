# mtnlpmodel

基于 TensorFlow 的多任务NLP算法（目前包含 `命名实体识别(NER)` 和 `子功能点分类（Sub-func Classification）`，更多算法正在持续添加中）。

## 特色
* 通用的序列标注：能够解决通用的序列标注问题：分词、词性标注和实体识别仅仅是特例。
* Tag schema free: 你可以选择你想用的任何 Tagset。依赖于 [tokenizer_tools](https://github.com/howl-anderson/tokenizer_tools) 提供的编码、解码功能
* 基于 TensorFlow Keras: 便于功能扩展和快速验证。

## 功能
```
* 文本分类： 我要听七里香。=> ( label：听音乐 )
* 实体识别： 我要听七里香。=> ( 我要听**七里香**<歌名>。)
```
## 内容结构
### 代码结构
```
mtnlpmodel
├── server/                      // server:inference->用于模型推理; evaluation->用于模型评估     
├── train.py                     // 模型训练入口
├── core.py                      // 模型构造，包括从零训练和finetuning
└── utils/                       // 与模型训练相关的内容
    ├── io_utils.py              // 读取数据和保存模型相关组件
    ├── loss_func_util.py        // 一些损失函数
    ├── lrset_util.py            // 学习率修改组件
    ├── input_process_util.py    // 输入数据预处理组件
    ├── model_util.py            // 一些layer和模块
    ├── optimizer_util.py        // 处理模型保存、统计等任务的组件
    └── triplet_loss_util        // triplet_loss相关组件，目前未启用

```
### 安装
```
pip install mtnlp_model
```
### Train
* train.py：融合模型训练入口（包括：1.从头训练 'random_initial'；
                                 2.fine-tuning 'load weights'）。
```
python -m mtnlpmodel.train.py  #启动多输入模型训练
```
### 可视化训练
```
tensorboard --logdir=./results/summary_log_dir
```