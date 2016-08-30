int Pritation(int* a, int left, int right)
{
    if (a == NULL || left < 0 || right <= 0||left>=right)
        return -1;
    int priot = a[left];
    int i = left, j = right;
    while (i < j)
    {
        while (i > j&&a[j] >= priot)
            j--;
        if(i<j)
            a[i]=a[j];
        while (i < j&&a[i] <= priot)
            i++;
        if(i<j)
            a[j]=a[i];
    }
    a[i] = priot;
    return i;
}

void QuickSort(int *a, int left,int right)
{
    if (a == NULL || left < 0 || right <= 0 || left>right)
        return;
    int k = Pritation(a, i, j);
    //下面是递归实现的代码
    if (k > left)
        QuickSort(a, left, k - 1);
    if (k < right)
        QuickSort(a, k + 1, right);
}

//最后贴出非递归的实现方式：

void QuickSort(int *a, int left,int right)
{
    if (a == NULL || left < 0 || right <= 0 || left>right)
        return;
    stack<int> temp;
    int i, j;
    //（注意保存顺序）先将初始状态的左右指针压栈
    temp.push(right);//先存右指针
    temp.push(left);//再存左指针
    while (!temp.empty())
    {
        i = temp.top();//先弹出左指针
        temp.pop();
        j = temp.top();//再弹出右指针
        temp.pop();
        if (i < j)
        {
            int k = Pritation(a, i, j);
            if (k > i)
            {
                temp.push(k - 1);//保存中间变量
                temp.push(i);  //保存中间变量 
            }
            if (j > k)
            {
                temp.push(j);
                temp.push(k + 1);
            }
        }

    }
    
}