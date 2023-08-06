import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pandas as pd


class ClassificationAnalysis:
    legend = {
        'd_load': ('Data Loading', 'maroon'),
        'd_transfer': ('Data Transfer', 'yellow'),
        'zero_grads': ('Zero Gradient', 'indigo'),
        'forward': ('Forward Pass', 'green'),
        'prediction': ('Prediction', 'blue'),
        'loss': ('Loss Computation', 'magenta'),
        'backward': ('Backward Pass', 'darkcyan'),
        'optimizer': ('Optimization Algorithm', 'darkslategray')
    }
    
    @staticmethod
    def plot_confusion_matrix(confusion_mat, classes, figure_axis, title=None, cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        """

        # Compute confusion matrix
        cm = confusion_mat

        ax = figure_axis
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.grid(False)
        ax.figure.colorbar(im, ax=ax)

        if classes is not None:
            # We want to show all ticks...
            ax.set(xticks=np.arange(cm.shape[1]),
                   yticks=np.arange(cm.shape[0]),
                   # ... and label them with the respective list entries
                   xticklabels=classes, yticklabels=classes,
                   ylabel='True Label',
                   xlabel='Predicted Label')

            # Rotate the tick labels and set their alignment.
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        else:
            plt.setp( ax.get_xticklabels(), visible=False)
            plt.setp( ax.get_yticklabels(), visible=False)
            plt.setp( ax.get_xticklines(), visible=False)
            plt.setp( ax.get_yticklines(), visible=False)

        ax.set(title=title)

        # Loop over data dimensions and create text annotations.
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, cm[i, j],
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

    @staticmethod
    def plot_confusion_table_sample(figure_axis, cmap=plt.cm.Blues):
        cm = np.array([[1, 0.5],
                       [0.5, 1]])

        labels = [['TP', 'FP'],
                  ['FN', 'TN']]

        ax=figure_axis
        ax.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.grid(False)
        plt.setp( ax.get_xticklabels(), visible=False)
        plt.setp( ax.get_yticklabels(), visible=False)
        plt.setp( ax.get_xticklines(), visible=False)
        plt.setp( ax.get_yticklines(), visible=False)

        # Loop over data dimensions and create text annotations.
        thresh = cm.max() / 2.

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, labels[i][j],
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

    @staticmethod
    def line_plot(y_train, y_val, metric):

        print('\n')
        if metric == 'Loss':
            print('Training {} Min: {:0.3f} in epoch {}, Max: {:0.3f}, Current: {:0.3f}'.format(
                metric, min(y_train), np.array(y_train).argmin(), max(y_train), y_train[-1]))
            print('Validation {} Min: {:0.3f} in epoch {}, Max: {:0.3f}, Current: {:0.3f}'.format(
                metric, min(y_val), np.array(y_val).argmin(), max(y_val), y_val[-1]))

        else:
            print('Training {} Min: {:0.3f}, Max: {:0.3f} in epoch {}, Current: {:0.3f}'.format(
                  metric, min(y_train), max(y_train), np.array(y_train).argmax(), y_train[-1]))
            print('Validation {} Min: {:0.3f}, Max: {:0.3f} in epoch {}, Current: {:0.3f}'.format(
                  metric, min(y_val), max(y_val), np.array(y_val).argmax(), y_val[-1]))
        plt.figure(figsize=(9,5))
        plt.plot(y_train, label='Training')
        plt.plot(y_val, label='Validation')
        plt.xlabel('Epoch')
        plt.ylabel(metric)
        plt.ylim([0, max([1] + y_train + y_val)])
        plt.title(metric)
        plt.grid(True)
        plt.legend()
        plt.show()
        
    @staticmethod
    def steps_timing_visualization(steps_timing, not_included = []):
        total = list()
        average = list()
        colors = list()
        legends = list()
        valid_steps= dict()
        plt.figure(figsize=(8,6))
        plt.xlabel('Iteration number')
        plt.ylabel('Time [Sec]')
        plt.grid(True)

        for key in steps_timing:
            if key in not_included:
                continue
                
            if len(steps_timing[key]) > 0:
                total.append(sum(steps_timing[key]))
                average.append(sum(steps_timing[key]) / len(steps_timing[key]))
                colors.append(ClassificationAnalysis.legend[key][1])
                legends.append(ClassificationAnalysis.legend[key][0])
                valid_steps[key] = steps_timing[key]
                plt.plot(steps_timing[key], label=ClassificationAnalysis.legend[key][0], color=ClassificationAnalysis.legend[key][1])
        plt.legend() 
        plt.show()
        
        plt.figure(figsize=(8,6))
        plt.xlabel('phases')
        plt.ylabel('Total time [Sec]')
        plt.grid(True)
        y_values = np.arange(len(valid_steps))
        for i in range(len(total)):
            plt.bar(y_values[i], total[i], color = colors[i], label = legends[i])
        plt.xticks(y_values, valid_steps, rotation='vertical')
        plt.legend()
        plt.show()
        
        plt.figure(figsize=(8,6))
        plt.xlabel('phases')
        plt.ylabel('Average time per batch [Sec]')
        plt.grid(True)
        y_values = np.arange(len(valid_steps))
        for i in range(len(average)):
            plt.bar(y_values[i], average[i], color = colors[i], label = legends[i])
        plt.xticks(y_values, valid_steps, rotation='vertical')
        plt.legend()
        plt.show()
        
    @staticmethod
    def misclassification(model, dataset):
        y_pred = model['best_params']['epoch_data']['y_pred_validation']
        for i in range(len(y_pred)):
            imgage, class_label = dataset.validation_dataset.imgs[i]
            if class_label != y_pred[i]:
                img = Image.open(imgage)
                plt.figure(figsize=(10, 10))
                plt.imshow(img)
                plt.grid(False)
                plt.title('Actual : {} , Prediction : {} \n image : {}'.format(dataset.classes_names[class_label], 
                                                                               dataset.classes_names[y_pred[i]], 
                                                                               imgage)) 
    
    @staticmethod
    def show_overall_metrics(overall_metrics, required_metrics = ['Accuracy', 'Recall', 'Precision', 'F1_score', 'Specificity', 'Cohen_Kappa']):
              
        overall_metrics = pd.Series(
                {m: overall_metrics[m] for m in required_metrics
                                       if m in overall_metrics.keys()})
        
        # Show overall metrics
        fig = plt.figure(figsize=(10, 5))
        ax = plt.subplot(1,2,1)
        overall_metrics.plot.bar()
        plt.title('Overall Metrics')
        plt.grid(True)
        plt.ylim((0,1.5))
        
        ax = plt.subplot(1,2,2)
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = overall_metrics.values.reshape((len(overall_metrics),1)), 
                     colLabels = ['Values'], 
                     rowLabels = overall_metrics.index,
                     loc = 'center',
                     colWidths = [0.2]
                    )
        table.scale(2, 2)
        table.set_fontsize(12)
        plt.show()
        
    @staticmethod
    def show_classes_metrics(classes_metrics, classes_labels, required_metrics = [ 'Recall', 'Precision', 'F1_score', 'Specificity', 'Cohen_Kappa']):
        
        classes_metrics = pd.DataFrame(
            {m: classes_metrics[m] for m in required_metrics
                                   if m in classes_metrics.keys()})
        classes_metrics.index = classes_labels
        
        # Data table
        ax = plt.subplot(1, 1, 1)
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = classes_metrics.values, 
                     colLabels = classes_metrics.columns, 
                     rowLabels = classes_metrics.index,
                     loc = 'center',
                     colWidths = [0.2]*len(classes_metrics.columns))
        
        table.scale(2, 2)
        table.set_fontsize(15)
        plt.grid(True)
        plt.show()
        
        # Compare between metrics
        classes_metrics.plot.bar()
        plt.title('Metrics Comparison')
        plt.grid(True)
        plt.legend(loc=0)
        plt.ylim((0,1.5))
        plt.show()
        
        # Compare between classes
        classes_metrics.T.plot.bar()
        plt.title('Classes Comparison')
        plt.grid(True)
        plt.ylim((0,1.5))
        plt.show()
    
    @staticmethod
    def show_roc_curve(number_of_classes, fpr, tpr, roc_auc):
        # Plot all ROC curves
        plt.figure(figsize=(7, 5))
        
        lw = 2
        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        if number_of_classes == 2:
            plt.plot(fpr, tpr,
                 label = 'ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc),
                 color = 'crimson', linestyle = ':', linewidth = 4)
        else:
            
            # Micro average ROC
            plt.plot(fpr["micro"], self.tpr["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)
        
            # Macro average ROC
            plt.plot(fpr["macro"], tpr["macro"],
                 label='macro-average ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc["macro"]),
                 color = 'navy', linestyle = ':', linewidth = 4)
        
            # Classes ROC
            for i in range(number_of_classes):
                plt.plot(fpr[i], tpr[i],  lw=lw,
                 label='ROC curve of ({0}) (area = {1:0.2f})'
                 ''.format(classes_labels[i], roc_auc[i]))

            
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves')
        plt.legend(loc="lower right")
        plt.show()
    
