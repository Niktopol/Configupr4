#include <iostream>
#include "tree.h"

int main(){
    //Среднее арифметическое
    tree tr1;
    for(int i = 1; i < 16; i++){
        tr1.add_item(i);}
    tr1.print_brach_mean();
    //Подсчёт по значению
    tree tr2;
    std::cout << "Записано в дерево: ";
    for(int i = 1; i < 25; i++){
        tr2.add_item(i%5);
        std::cout << i%5 << " ";
    }
    std::cout << std::endl << "Количество элементов со значением 3 равно " << tr2.count_elements(3) << std::endl;
    return 0;
    //Удаление происходит автоматически
}