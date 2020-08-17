from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from warnings import filterwarnings
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression as LR

# A
def cross_validation_error(X, y, model, folder):
    sum_train_error = 0
    sum_val_error = 0
    kf = KFold(n_splits=folder)
    for train_index, test_index in kf.split(X):
        X_train, X_val = X[train_index], X[test_index]
        y_train, y_val = y[train_index], y[test_index]
        fit_model = model.fit(X_train, y_train)
        X_train_pred = fit_model.predict(X_train)
        X_val_pred = fit_model.predict(X_val)
        sum_train_error += 1 - accuracy_score(X_train_pred, y_train)
        sum_val_error += 1 - accuracy_score(X_val_pred, y_val)
    avg_train_error = sum_train_error / folder
    avg_val_error = sum_val_error / folder
    return [avg_train_error, avg_val_error]


# B
def Logistic_Regression_results(X_train, y_train, X_test, y_test):
    results_dict = {}
    lamda = [10 ** (-4), 10 ** (-2), 1, 10 ** 2, 10 ** 4]
    for i in lamda:
        #print(i)
        #model = LR(C=1 / i, multi_class='ovr', penalty='l2', solver='liblinear')
        model = LR(C=float(1 / i),multi_class='ovr', penalty='l2')
        val = cross_validation_error(X_train, y_train, model, 5)
        fit_model = model.fit(X_train, y_train)
        test_pred = fit_model.predict(X_test)
        # print(test_pred,y_test,accuracy_score(test_pred , y_test))
        results_dict['LogReg_lam_' + str(i)] = [val[0], val[1], 1 - accuracy_score(test_pred, y_test)]
    return results_dict


# C
def l_iris():
    iris = load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)
    filterwarnings('ignore')
    return X_train, X_test, y_train, y_test

# D
X_train, X_test, y_train, y_test = l_iris()
res_dict = Logistic_Regression_results(X_train, y_train, X_test, y_test)
print(res_dict)
train_errors, val_errors, test_errors = [], [], []
for model in res_dict.values():
    print(res_dict)
    train_errors.append(round(model[0], 2))
    val_errors.append(round(model[1], 2))
    test_errors.append(round(model[2], 2))

x = np.arange(len(train_errors))
width = 0.25
fig, ax = plt.subplots()
rects1 = ax.bar(x - width, train_errors, width, label='Train Error')
rects2 = ax.bar(x, val_errors, width, label='Validation Error')
rects3 = ax.bar(x + width, test_errors, width, label='Test Error')

for i in range(len(train_errors)):
    plt.text(x =x[i]-0.38, y =train_errors[i]+0.01, s = np.around(train_errors[i] ,decimals=4), size = 6)
    plt.text(x=x[i]-0.1 , y=val_errors[i] + 0.01, s=np.around(val_errors[i], decimals=4), size=6)
    plt.text(x=x[i]+0.15, y=test_errors[i] + 0.01, s=np.around(test_errors[i], decimals=4), size=6)

ax.set_ylabel('Errors')
ax.set_title('Errors by different models')
ax.set_xticks(x)
ax.set_xticklabels(tuple(res_dict.keys()), fontsize=7)
ax.legend()

fig.tight_layout()
plt.show()
