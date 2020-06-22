#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


def f1():
    import pandas as pd

    def fun(row):
        return (row['投诉日期'] - row['cdate']).days

    p_df = pd.read_excel('./a.xlsx')
    pd_df = pd.read_excel('./ad.xlsx')
    print(p_df.head())
    print(pd_df.head())

    m_df = pd.merge(p_df, pd_df, how='left', left_on='手机号', right_on='mobile')
    m_df['手机号'] = m_df['手机号'].astype('str')
    m_df['mobile'] = m_df['mobile'].astype('str')

    m_df['delta'] = m_df.apply(fun, axis=1)

    nm_df = m_df[m_df['delta'] >= 0]
    tmp_s = nm_df.groupby(['手机号', '投诉日期']).delta.min()

    tmp_df = pd.DataFrame({
        '手机号': [i[0] for i in tmp_s.index],
        '投诉日期': [i[1] for i in tmp_s.index],
        'delta': tmp_s.values,
    })

    ret = pd.merge(nm_df, tmp_df, how='inner', on=['手机号', '投诉日期', 'delta'])
    ret.drop_duplicates().to_excel('ret.xlsx')


def f2():
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(-3, 3, 50)
    y1 = 2 * x + 1
    y2 = x ** 2

    plt.figure()

    # 设置打印出线的名字 label
    l1 = plt.plot(x, y2, label='up')
    l2 = plt.plot(x, y1, color='red', linewidth=2.0, linestyle='--', label='down')

    # 设置 x y 轴坐标范围
    plt.xlim((-1,2))
    plt.ylim((-2,3))

    # 设置 x y 轴名称
    plt.xlabel('I pattern x')
    plt.ylabel('I pattern y')

    # 设置 x y 轴刻度明细
    x_ticks = np.linspace(-1, 2, 5)
    plt.xticks(x_ticks)
    # 设置显示格式
    plt.yticks([-2, -1.8, -1, 1.2, 3],
               [r'$really\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$really\ good$'])

    # gca = get current axis
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

    plt.show()


def f3():
    import pandas as pd
    # from openpyxl import load_workbook

    p_df = pd.read_excel('./a.xlsx')
    # pd_df = pd.read_excel('./ad.xlsx')

    writer = pd.ExcelWriter('./test.xlsx', engin='openpyxl')
    # book = load_workbook(writer.path)
    # writer.book = book
    p_df.to_excel(excel_writer=writer, sheet_name="info1")
    p_df.to_excel(excel_writer=writer, sheet_name="info2", index=False)
    writer.save()
    writer.close()


def f4():
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier

    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)

    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    y_ret = knn.predict(X_test)
    print(y_ret)
    print(y_test)


def f5():
    from sklearn import datasets
    from sklearn import preprocessing
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import matplotlib.pyplot as plt

    loaded_data = datasets.load_boston()
    data_X = loaded_data.data

    # data_X = preprocessing.scale(data_X)
    data_y = loaded_data.target
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, test_size=0.3)

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_ret = lr.predict(X_test)
    lr.score(X_test, y_test)
    # print(y_ret)
    # print(y_test)

    # plt.figure()
    # ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=2)
    # ax1.plot(X_test, y_ret)
    # ax1.set_title('predict')
    #
    # ax2 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=2)
    # ax2.plot(X_test, y_test)
    # ax2.set_title('origin')
    #
    # plt.show()


def f6():
    import numpy as np
    import pandas as pd

    data = {
        'Team': [
            'Riders', 'Riders', 'Devils', 'Devils', 'Kings',
            'kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals',
            'Riders'
        ],
        'Rank': [1, 2, 2, 3, 3, 4, 1, 1, 2, 4, 1, 2],
        'Year': [
            2014, 2015, 2014, 2015, 2014, 2015, 2016, 2017, 2016, 2014,
            2015, 2017
        ],
        'Points': [876, 789, 863, 673, 741, 812, 756, 788, 694, 701, 804, 690]
    }

    df = pd.DataFrame(data)

    grouped = df.groupby('Year')
    for name, group in grouped:
        print(name)
        print(group)

    d = df.groupby('Team')
    score = lambda x: (x - x.mean()) / x.std() * 10
    d.transform(score)


def f7():
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(np.random.randint(6, size=(6, 4)),
                      index=pd.date_range('2019-01-01', periods=6),
                      columns=['A', 'B', 'C', 'D'])

    print(df)
    print("=======================================")
    # r = df.rolling(window=3, min_periods=3)
    r = df.rolling(window=3)
    print(r)
    r.aggregate(np.mean)

    # e = df.expanding(min_periods=3)
    e = df.expanding(3)
    print(e)
    e.aggregate(np.mean)

    print(df.ewm(com=0.5).mean())
