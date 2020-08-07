#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 读取要创建的jobs名称
def readJobsName():
    with open('jobsName.ini', encoding='utf-8') as f:
        jobnames = [line.strip() for line in f.readlines()]
    return jobnames


def changeConfig(jobname):
    with open('jenkins_config.xml', mode='r') as f:
        cnt = f.read().replace("jenkinsProjectName", f"{jobname}")
    return cnt


# 创建新的jobs
def createNewJobs():
    jobs = readJobsName()
    for jobName in jobs:
        pathConfigxml = changeConfig(jobName)
        print(pathConfigxml)


if __name__ == '__main__':
    createNewJobs()
