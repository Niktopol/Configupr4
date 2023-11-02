#ifndef TREE
#define TREE
#include <cmath>
#include <iostream>
#include <queue>

class tree{
    //Структура узла дерева
    struct tree_item{
        tree_item* left;
        tree_item* right;
        double value;
        //Метод, считающий сумму узлов дерева и их количество
        void branch_sum(double&, int&);
        //Метод, считающий количество узлов, значение в которых совпадает со значением параметра
        int count_elements(double);
        tree_item(double);
        ~tree_item();
    };
    int records;
    tree_item* root;
    public:
    //Метод, считающий средние арифметические поддеревьев и выводящий результат в консоль
    void print_brach_mean();
    //Метод, считающий количество узлов, значение в которых совпадает со значением параметра и возвращающий результат
    int count_elements(double);
    //Метод, добавляющий новый узел в дерево
    void add_item(double);
    tree();
    ~tree();
};
#endif