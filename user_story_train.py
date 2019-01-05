# pip install jira
from jira import JIRA
import pandas as pd
from pandas import ExcelWriter
import warnings

pd.options.mode.chained_assignment = None

warnings.filterwarnings('ignore')


file_name = 'Team1JiraReportMain.xlsx'
sheetname = 'User Story Prediction'


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