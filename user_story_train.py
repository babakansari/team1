# pip install jira
from jira import JIRA
import pandas as pd
from pandas import ExcelWriter
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from joblib import dump, load

pd.options.mode.chained_assignment = None

warnings.filterwarnings('ignore')


file_name = 'Team1JiraReportMain.xlsx'
sheetname = 'User Story Prediction'
target = 'Points'

def get_story_points_data(username, password):
    auth_jira = JIRA(server='https://intelex.atlassian.net', auth=(username, password))

    # my top 5 issues due by the end of the week, ordered by priority
    oh_crap = auth_jira.search_issues(
        '"Tech Team"="Team 1" AND Sprint is not EMPTY AND "Story Points" is not EMPTY and labels is not EMPTY order by priority desc',
        maxResults=3000)
    print("User " + username + " is logged in")
    print("Reading from Jira...")
    pd.options.mode.chained_assignment = None  # default='warn'
    labels_df = pd.DataFrame(columns=['Labels'])
    story_df = pd.DataFrame(columns=['Index', 'Key', 'Summary', 'Points', 'Labels'])

    i = 0
    r = 0
    for issue in oh_crap:
        hasMlTag = False
        for label in issue.fields.labels:
            if 'ML-' in label:
                labels_df.loc[i] = [label]
                hasMlTag = True
            i = i + 1
        if hasMlTag:
            story_df.loc[i] = [r, issue.key, issue.fields.summary, issue.fields.customfield_10049, None]
            story_df.at[i, 'Labels'] = issue.fields.labels
            r = r + 1
    print("Number of records read: ", r)

    labels_df = labels_df.drop_duplicates()
    labels_df = labels_df.set_index('Labels').T

    combine_df = pd.concat([story_df, labels_df], ignore_index=False)

    for index, row in combine_df.iterrows():
        for label in row['Labels']:
            if label in labels_df.columns:
                combine_df.loc[index, label] = 1

    df = combine_df.drop(columns=['Labels'])
    df.fillna(0, inplace=True)

    writer = ExcelWriter(file_name)
    df.to_excel(writer, sheetname)
    writer.save()
    return df

def search_best_parameters(model, X_tr, y_tr, X_te, parameters):
    classifier = OneVsRestClassifier(model)

    gs = GridSearchCV(classifier, parameters, cv=4)  # Using R^2 (coefficient of determination)
    gs.fit(X_tr, y_tr).decision_function(X_te)

    model_params = {}
    for param in gs.best_params_:
        model_param = param.replace("estimator__", "")
        model_params[model_param] = gs.best_params_[param]
    print(type(model).__name__, ': ', model_params, 'with score:', gs.best_score_)
    return gs

def train_test_stories(data, test_size):
    train_set, test_set = train_test_split(data, test_size=test_size, random_state=42)
    print(len(train_set), "train +", len(test_set), "test")

    features = list(train_set.columns)
    features = [f for f in features if f != target and f != 'Index' and f != 'Key' and f != 'Summary']

    # Split data into train and test sets
    X_tr = train_set[features]

    X_te = test_set[features]

    # Encode points using one hot encoder
    points_tr = train_set[[target]]

    cat_encoder = OneHotEncoder(sparse=False)

    points_tr_fit = cat_encoder.fit(points_tr)

    points_tr_cat = points_tr_fit.transform(points_tr)

    points_te = test_set[[target]]
    points_te_cat = cat_encoder.fit_transform(points_te)

    points_te_cat
    y_tr = points_tr_cat
    y_te = points_te_cat

    return X_tr, y_tr, X_te, y_te

def _save_model(data):
    prediction_df = data.copy()
    prediction_df = prediction_df.drop(columns=['Index', 'Key', 'Points', 'Summary']).iloc[0:0]
    return prediction_df

def save_trained_models(df):
    print('------------< Train >------------------')
    X_tr, y_tr, X_te, y_te = train_test_stories(df, 0.40)

    grid = {
        'estimator__C': [0.1, 10, 100, 1000],
        'estimator__solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
        'estimator__multi_class': ['ovr', 'multinomial']
    }
    logistic = LogisticRegression()
    logistic_classifier = search_best_parameters(logistic, X_tr, y_tr, X_te, grid)
    #logistic = LogisticRegression(**best_params)
    dump(logistic_classifier, 'logistic.classifier')

    grid={
        'estimator__C': [ 0.1, 1, 10, 100, 100],
        #'estimator__gamma': [ 0.1,1, 10],
        'estimator__kernel': [ 'linear', 'poly', 'rbf']
    }
    svc = SVC(probability=True)
    svc_classifier = search_best_parameters(svc, X_tr, y_tr, X_te, grid)
    #self.svc = SVC(probability=True, **best_params)
    dump(svc_classifier, 'svc.classifier')

    grid = {
        'estimator__C': [0.1, 5, 10, 15],
        'estimator__multi_class': ['ovr', 'crammer_singer'],
    }
    linearSVC = LinearSVC()
    linearSVC_classifier = search_best_parameters(linearSVC, X_tr, y_tr, X_te, grid)
    #self.linearSVC = LinearSVC(**best_params)
    dump(linearSVC_classifier, 'linearSVC.classifier')

    adaBoost = AdaBoostClassifier(logistic)
    adaBoost_classifier = search_best_parameters(adaBoost, X_tr, y_tr, X_te, {})
    #adaBoost_classifier.fit(X_tr, y_tr).decision_function(X_te)
    dump(adaBoost_classifier, 'adaBoost.classifier')

    model = _save_model(df)
    dump(model, 'data.model')


def load_trained_model(self):
    self.logistic_classifier = load('logistic.classifier')
    self.svc_classifier = load('svc.classifier')
    self.linearSVC_classifier = load('linearSVC.classifier')
    self.adaBoost_classifier = load('adaBoost.classifier')
    self.model = load('data.model')