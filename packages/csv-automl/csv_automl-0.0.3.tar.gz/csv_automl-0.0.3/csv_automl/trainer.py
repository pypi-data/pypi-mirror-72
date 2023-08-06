import json
import sklearn.metrics
import time
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import DataLoader


def generate_batch(batch):
    feature = torch.tensor([entry[0] for entry in batch], dtype=torch.float32)
    label = torch.tensor([entry[1] for entry in batch], dtype=torch.float32)
    label = label.unsqueeze(1)
    return feature, label


class Trainer():
    def __init__(self, model, train_data, dev_data):
        self.train_data = train_data
        self.dev_data = dev_data
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.criterion = model.criterion()
        self.optimizer = model.optimizer()
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, 1, gamma=0.9)
        self.debug = False

    def train(self, batch_size=128):
        # Train the model
        train_loss = 0
        data = DataLoader(self.train_data, batch_size=batch_size, shuffle=True, collate_fn=generate_batch)
        y = []
        pred = []
        for i, (inputs, cls) in enumerate(data):
            y.extend(cls.tolist())
            self.optimizer.zero_grad()
            inputs, cls = inputs.to(self.device), cls.to(self.device)
            output = self.model(inputs)
            self.loss = self.criterion(output, cls)
            self.loss.backward()
            self.optimizer.step()

            pred.extend(output.cpu().tolist())
            train_loss += self.loss.item()

        # Adjust the learning rate
        self.scheduler.step()

        train_len = len(self.train_data)
        metrics = {
            'loss': train_loss / train_len
        }
        for k, v in self.model.get_metrics(y, pred).items():
            metrics[k] = v
        return metrics, y, pred
    
    def dev(self, batch_size=128):
        loss = 0
        data = DataLoader(self.dev_data, batch_size=batch_size, collate_fn=generate_batch)
        y = []
        pred = []
        for inputs, cls in data:
            y.extend(cls.tolist())
            inputs, cls = inputs.to(self.device), cls.to(self.device)

            with torch.no_grad():
                output = self.model(inputs)
                loss = self.criterion(output, cls)
                loss += loss.item()
                pred.extend(output.cpu().tolist())

        dev_len = len(self.dev_data)
        metrics = {
            'loss': loss / dev_len
        }
        for k, v in self.model.get_metrics(y, pred).items():
            metrics[k] = v
        return metrics, y, pred

    def predict(self, infer_data, batch_size=128):
        data = DataLoader(infer_data, batch_size=batch_size, collate_fn=generate_batch)
        pred = []
        for inputs, _ in data:
            inputs = inputs.to(self.device)
            with torch.no_grad():
                output = self.model(inputs)
                pred.extend(output.cpu().tolist())

        return pred

    def train_loop(self, batch_size=128, n_epochs=50):
        min_dev_loss = float('inf')
        min_dev_metrics = None
        all_dev_metrics = []
        for epoch in range(n_epochs):
            start_time = time.time()
            train_metric, train_y, train_pred = self.train(batch_size)
            dev_metric, dev_y, dev_pred = self.dev(batch_size)
            secs = int(time.time() - start_time)
            mins = secs / 60
            secs = secs % 60

            print('Epoch: %d, | time in {%d} minutes, {%d} seconds.' % (epoch + 1, mins, secs))
            print('Train loss: %.4f' % train_metric['loss'])
            print('Dev loss: %.4f' % dev_metric['loss'])
            dev_metric['epoch'] = epoch + 1
            all_dev_metrics.append(dev_metric)
            dev_loss = dev_metric['loss']
            if dev_loss < min_dev_loss:
                min_dev_loss = dev_loss
                min_dev_metrics = dev_metric
            
            for k, v in dev_metric.items():
                print('Dev %s: %.4f' % (k, v))

            if self.debug:
                for (y, pred) in zip(train_y[:10], train_pred[:10]):
                    print(y, pred)
                
                for (y, pred) in zip(dev_y[:10], dev_pred[:10]):
                    print(y, pred)

        return all_dev_metrics, min_dev_metrics
