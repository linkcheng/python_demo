/*************************************************************************
	> File Name: mem_text.c
	> Created Time: 2016年05月06日 星期五 17时34分01秒
 ************************************************************************/

#include<stdio.h>


struct node {
	char a;   
	char b;  
	short c;   
	int d;
};

void arr_test(void) 
{
    int a[5] = {1, 2, 3, 4, 5};
    int *ptr = (int*)(&a + 1);

    printf("&a[0] = %p\n", &a[0]);
    printf("a = %p\n", a);
    printf("&a = %p\n", &a);
    
    printf("&a[0]+1 = %p\n", &a[0]+1);   
    printf("a+1 = %p\n", a+1);      // This is equal to &a[0]+1, the step is a int.
    printf("&a+1 = %p\n", &a+1);    // But this is not. This is equal to int (*a)[5] + 1, the step is int[5].

    printf("*(&a[0]+1) = %d\n", *(&a[0]+1));
    printf("*(a+1) = %d\n", *(a+1));
    printf("*(ptr-1) = %d\n", *(ptr-1));
}

void mem_test(void) 
{
	struct node s = { 3, 5, 6, 9};
	struct node *pt = &s;
	int tmp[4] = {0};
	
	printf("a = %X\n", s.a);
	printf("b = %X\n", s.b);
	printf("c = %X\n", s.c);
	printf("d = %X\n", s.d);
	
	printf("addr a = %p\n", &s.a);
	printf("addr b = %p\n", &s.b);
	printf("addr c = %p\n", &s.c);
	printf("addr d = %p\n", &s.d);
	printf("addr pt = %p\n", &pt);
	
	
	printf("%X\n", *(short*)pt);
	printf("%X\n", *(int*)pt);

	printf("addr short pt  = %p\n", (short*)pt);
	printf("addr short pt next  = %p\n", ((short*)pt+1));
	printf("addr int pt = %p\n", (int*)pt); // 需要考虑字节对齐与大小端字节序

    printf("addr tmp0 = %p\n", &tmp[0]);
    printf("addr tmp1 = %p\n", &tmp[1]);
    printf("addr tmp2 = %p\n", &tmp[2]);
    printf("addr tmp3 = %p\n", &tmp[3]);
}

int main() 
{
     mem_test();

    arr_test();

	return 0;
}
