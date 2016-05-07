#include <stdio.h>
#include <setjmp.h>
 
jmp_buf jump_buffer;
 
void func(void) 
{
    printf("Before calling longjmp\n");
    longjmp(jump_buffer, 1);
    printf("After calling longjmp\n");
}

void func1(void) 
{
    printf("Before calling func\n");
    func();
    printf("After calling func\n");
}

void func2(void) 
{
    printf("calling func2\n");
    longjmp(jump_buffer, 2);
    printf("After calling func2\n");
}

void func0(void) 
{
    printf("calling func0\n");
    longjmp(jump_buffer, 0);
    printf("After calling func0\n");
}

int main() 
{
    int tmp = setjmp(jump_buffer);
    printf("tmp = %d\n", tmp);
    
    if (tmp == 0) {
        printf("first calling set_jmp\n");
        func1();
    }
    else if (tmp == 1) {
        printf("second calling set_jmp\n");
        func2();
    }
    else {
        printf("third calling set_jmp\n");
        func0();
    }
    
    return 0;
}
