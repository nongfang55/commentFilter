import torch
import numpy as np
import pandas
from d2l.torch import Accumulator, accuracy
from numpy import mean
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from torch import nn
from torch.utils import data
import random
from d2l import torch as d2l
from sklearn.utils import shuffle


def get_k_fold_data(k, i, X, y):
    """获得第K折的训练数据"""
    assert k > 1
    fold_size = X.shape[0] // k
    X_train, y_train = None, None
    for j in range(k):
        idx = slice(j * fold_size, (j + 1) * fold_size)
        X_part, y_part = X[idx, :], y[idx]
        if j == i:
            X_valid, y_valid = X_part, y_part
        elif X_train is None:
            X_train, y_train = X_part, y_part
        else:
            X_train = torch.cat([X_train, X_part], 0)
            y_train = torch.cat([y_train, y_part], 0)
    return X_train, y_train, X_valid, y_valid


def get_net(feature_len):
    return nn.Sequential(nn.Linear(feature_len, 1), nn.Sigmoid())


def train(net, X_train, y_train, X_valid, y_valid, num_epochs, learning_rate, weight_decay, batch_size):
    train_ls_list, valid_ls_list = [], []
    train_precision, train_recall = [], []
    valid_precision, valid_recall = [], []
    train_auc = []
    valid_auc = []
    train_dataset = data.TensorDataset(X_train, y_train)
    train_iter = data.DataLoader(train_dataset, batch_size, shuffle=True)

    """训练"""
    loss = nn.BCELoss()  # 损失是二值交叉熵
    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate, weight_decay=weight_decay)

    for epoch in range(0, num_epochs):
        for X, y in train_iter:
            optimizer.zero_grad()
            y_hat = net(X)
            l = loss(y_hat, y)
            l.backward()
            optimizer.step()

        """一个epoch 训练完了做计算总体loss"""
        y_train_hat = net(X_train)
        train_ls = loss(y_train_hat, y_train)
        train_ls_list.append(train_ls.item())

        """计算训练 Precission 和  Recall"""
        y_train_mask = y_train_hat.ge(0.5).type(y_train.dtype)
        y_train_precision = precision_score(y_train, y_train_mask)
        y_train_recall = recall_score(y_train, y_train_mask)
        y_train_auc = roc_auc_score(y_train.detach().numpy(), y_train_hat.detach().numpy())

        train_precision.append(y_train_precision)
        train_recall.append(y_train_recall)
        train_auc.append(y_train_auc)

        """计算验证loss"""
        y_valid_hat = net(X_valid)
        valid_ls = loss(y_valid_hat, y_valid)
        valid_ls_list.append(valid_ls.item())

        """计算验证 Precission 和  Recall"""
        y_valid_mask = y_valid_hat.ge(0.5).type(y_valid.dtype)
        y_valid_precision = precision_score(y_valid, y_valid_mask)
        y_valid_recall = recall_score(y_valid, y_valid_mask)
        y_valid_auc = roc_auc_score(y_valid.detach().numpy(), y_valid_hat.detach().numpy(), average='micro')

        valid_precision.append(y_valid_precision)
        valid_recall.append(y_valid_recall)
        valid_auc.append(y_valid_auc)

        if epoch % 20 == 0:
            print(
                f'epoch :{epoch},train auc: {y_train_auc},valid precission: {y_train_precision}, valid recall: {y_train_recall}')
            print(
                f'epoch :{epoch},valid auc: {y_valid_auc},valid precission: {y_valid_precision}, valid recall: {y_valid_recall}')

    return train_ls_list, valid_ls_list, train_auc, valid_auc


def k_fold(k, features, labels, num_epochs, learning_rate, weight_decay, batch_size):
    train_l_sum, valid_l_sum, train_auc_sum, valid_auc_sum = [], [], [], []
    for i in range(k):
        print("==" * 20 + f'fold:{i}' + "==" * 20)
        X_train, y_train, X_valid, y_valid = get_k_fold_data(k, i, features, labels)

        def init_weight(m):
            if type(m) == nn.Linear or type(m) == nn.Conv2d:
                nn.init.xavier_normal_(m.weight)

        net = get_net(X_train.shape[1])
        net.apply(init_weight)

        train_ls, valid_ls, train_auc, valid_auc = train(net, X_train, y_train, X_valid, y_valid, num_epochs, learning_rate, weight_decay,
                                   batch_size)
        train_l_sum.append(train_ls[-1])
        valid_l_sum.append(valid_ls[-1])
        train_auc_sum.append(train_auc[-1])
        valid_auc_sum.append(valid_auc[-1])
    print('avg train loss:', mean(train_l_sum))
    print('avg valid loss:', mean(valid_l_sum))
    print('avg train auc:', mean(train_auc_sum))
    print('avg valid auc:', mean(valid_auc_sum))

if __name__ == "__main__":
    """读入手动标注的数据"""
    data_path = r'../../data/chrome/chromium_conversations_annotations.csv'
    rawData = pandas.read_csv(data_path)
    """打乱"""
    rawData = shuffle(rawData)
    print(rawData)

    """保留需要的行数"""
    featureColumns = ['pdensity', 'max_politeness', 'min_formality', 'max_formality']
    # featureColumns = ['yngve', 'frazier', 'pdensity', 'cdensity', 'pct_neg_tokens','pct_neu_tokens',
    #                   'pct_pos_tokens', 'pct_nne_tokens', 'min_politeness','max_politeness',
    #                   'min_formality', 'max_formality', 'num_tokens', 'num_sentences',
    #                   'has_doxastic', 'has_epistemic','has_conditional','has_investigative','has_uncertainty']
    # featureColumns = ['yngve', 'frazier', 'pdensity', 'cdensity', 'pct_neg_tokens','pct_neu_tokens',
    #                   'pct_pos_tokens', 'pct_nne_tokens', 'min_politeness','max_politeness',
    #                   'min_formality', 'max_formality', 'num_tokens', 'num_sentences']
    labelColumn = ['comment_type']
    features = rawData[featureColumns].copy(deep=True)
    labels = rawData[labelColumn].copy(deep=True)
    """修改标签"""
    labels[labelColumn[0]] = labels[labelColumn[0]].apply(lambda x: 1 if x == 'acted-upon' else 0)
    print(features)
    print(labels)

    """feature 归一化"""
    features[features.columns] = features[features.columns].apply(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    """我们尝试做个分桶试试"""
    for col in features.columns:
        for i in range(0, 10):
            features[f'{col}_{i}'] = features[col].apply(lambda x: 1 if (0.1 * i <= x < 0.1 * (i + 1)) else 0)

    """特征交叉"""
    for i in range(0, featureColumns.__len__()):
        for j in range(i + 1, featureColumns.__len__()):
            col_i = featureColumns[i]
            col_j = featureColumns[j]
            for m in range(0, 10):
                for n in range(0, 10):
                    features[f'{col_i}_{col_j}_{m}_{n}'] = \
                        features.apply(lambda x: x[f'{col_i}_{m}'] * x[f'{col_j}_{n}'], axis=1)

    # """特征交叉"""
    # for i in range(0, featureColumns.__len__()):
    #     for j in range(i + 1, featureColumns.__len__()):
    #         col_i = featureColumns[i]
    #         col_j = featureColumns[j]
    #         for m in range(0, 10):
    #             features[f'{col_i}_{col_j}_{m}'] = \
    #                 features.apply(lambda x: 1 if ( 0.1 * i <= x[f'{col_i}'] * x[f'{col_j}'] < 0.1 * (i + 1)) else 0, axis=1)

    features = torch.Tensor(features.values)
    features = features[:, featureColumns.__len__():]
    labels = torch.Tensor(labels.values)

    num_epochs = 100
    lr = 0.1
    batch_size = 128
    weight_decay = 0
    k_fold(k=10, features=features, labels=labels.reshape(-1, 1), num_epochs=num_epochs,
           learning_rate=lr, weight_decay=weight_decay, batch_size=batch_size)

    # train_X = features[:border]
    # train_y = labels[:border]
    # test_X = features[border:]
    # test_y = labels[border:]
    #
    # train_dataset = data.TensorDataset(train_X, train_y)
    # train_iter = data.DataLoader(train_dataset, batch_size, shuffle=True)
    # test_dataset = data.TensorDataset(test_X, test_y)
    # test_iter = data.DataLoader(test_dataset)

    # """加载模型"""
    # feature_len = featureColumns.__len__()
    # net = nn.Sequential(nn.Linear(feature_len, 1), nn.Sigmoid())
    #
    # """训练"""
    # loss = nn.BCELoss()  # 损失是二值交叉熵
    # lr = 0.1
    # trainer = torch.optim.SGD(net.parameters(), lr=lr)
    # p = 0.5
    #
    # net.train()
    # num_epochs = 10
    # for epoch in range(num_epochs):
    #     metric = Accumulator(3)
    #     for X, y in train_iter:
    #         y_hat = net(X)
    #         l = loss(y_hat, y)
    #         trainer.zero_grad()
    #         l.backward()
    #         trainer.step()
    #
    #         mask = y_hat.ge(p).type(y.dtype)
    #         acc_count = float((mask == y).type(y.dtype).sum())
    #         metric.add(float(l) * len(y), acc_count, y.numel())
    #     print(f'epoch:{epoch} ,loss: {metric[0] / metric[2]}, acc: {metric[1] / metric[2]}')
