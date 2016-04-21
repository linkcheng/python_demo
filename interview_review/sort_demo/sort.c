#include <stdio.h>

int bubble_sort_arr(int a[], int len) {
    if (len <= 0){
        return 0;
    }

    int i = 0;
    int j = 0;
    int is_changed = 0;
    
    for(i=0; i<len; i++) {
        is_changed = 0;
        
        for(j=0; j<len-1; j++) {
            if(a[j] > a[j+1]) {
                int temp = a[j];
                a[j] = a[j+1];
                a[j+1] = temp;
                is_changed = 1;
            }
            
        }
        
        if (0 == is_changed) {
            break;
        }
        for(j=0; j<len; j++) {
            printf("%d ", a[j]);
        }
        printf("\n");
    }
    
    return 1;
}

int select_sort_arr(int a[], int len) {
    if (len <= 0){
        return 0;
    }

    int i = 0;
    int j = 0;
    int max, k;
    
    for(i=0; i<len; i++) {
        max = a[i];
        k = i;
        
        for(j=i+1; j<len; j++) {
            if(a[j] > max) {
                max = a[j];
                k = j;
            }
            
        }
        
        a[k] = a[i];  
        a[i] = max;
        
        for(j=0; j<len; j++) {
            printf("%d ", a[j]);
        }
        printf("\n");
    }
    
    return 1;
}

int quick_sort_arr(int a[], int left,int right) 
{ 
    int i,j,t,temp; 
    
    if(left > right) {
       return 0; 
    }
                                
    temp = a[left]; //temp中存的就是基准数 
    i = left; 
    j = right; 
    
    while(i < j) { 
        //顺序很重要，要先从右边开始找 
        while(a[j] >= temp && i < j) 
            j--; 
        //再找左边的 
        while(a[i] <= temp && i < j) 
            i++; 
        //交换两个数在数组中的位置 
        if(i < j) { 
            t = a[i]; 
            a[i] = a[j]; 
            a[j] = t; 
        } 
    } 
    
    //最终将基准数归位 
    a[left] = a[i]; 
    a[i] = temp; 
               
    for(t=0; t<right+1; t++) {
        printf("%d ", a[t]);
    }
    printf("\n");
                             
    quick_sort_arr(a, left, i-1); //继续处理左边的，这里是一个递归的过程 
    quick_sort_arr(a, i+1, right); //继续处理右边的，这里是一个递归的过程 
    
    return 1;
}

int main(void) {

    int a[10] = {3, 4, 6, 1, 2, 5, 0, 9, 7, 8};
    int i = 0;
    
    printf("before arr sort\n");
    for(i=0; i<10; i++) {
        printf("%d ", a[i]);
    }
    printf("\n\n");
    
    //bubble_sort_arr(a, 10);
    
    //select_sort_arr(a, 10);
    
    quick_sort_arr(a, 0, 9);
    
    printf("after arr sort\n");
    for(i=0; i<10; i++) {
        printf("%d ", a[i]);
    }
    printf("\n=============\n");
    
    return 0;
}
