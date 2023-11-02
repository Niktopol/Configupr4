#include "tree.h"
tree::tree_item::tree_item(double value){
    this->left = nullptr;
    this->right = nullptr;
    this->value = value;
};
tree::tree_item::~tree_item(){
    std::cout << "Node " << value << " deleted"<<std::endl;
    if (left){
        delete left;
    }
    if (right){
        delete right;
    }
}
void tree::tree_item::branch_sum(double &sum, int &counter){
    counter += 1;
    sum += value;
    if (left){
        left->branch_sum(sum, counter);
    }
    if(right){
        right->branch_sum(sum, counter);
    }
}
int tree::tree_item::count_elements(double num){
    int res = 0;
    if (value == num){
        res += 1;
    }
    if(left){
        res += left->count_elements(num);
    }
    if(right){
        res += right->count_elements(num);
    }
    return res;
}
void tree::print_brach_mean(){
    double sum = 0;
    int counter = 0;
    std::queue<tree_item*> queue;
    tree_item* litem;
    tree_item* ritem;
    if(root){
        if(root->left){
            queue.push(root->left);
        }
        if(root->right){
            queue.push(root->right);
        }
    }
    while (!queue.empty()){
        sum = 0;
        counter = 0;
        litem = queue.front();
        queue.pop();
        litem->branch_sum(sum, counter);
        std::cout<< "Arithmetic mean of the left subtree with root " << litem->value << ": " << (sum/counter) << std::endl;
        if(litem->left){
            queue.push(litem->left);
        }
        if(litem->right){
            queue.push(litem->right);
        }
        if(!queue.empty()){
            sum = 0;
            counter = 0;
            ritem = queue.front();
            queue.pop();
            ritem->branch_sum(sum, counter);
            std::cout<< "Arithmetic mean of the right subtree with root " << ritem->value << ": " << (sum/counter) << std::endl;
            if(ritem->left){
                queue.push(ritem->left);
            }
            if(ritem->right){
                queue.push(ritem->right);
            }
        }
    }
}
int tree::count_elements(double num){
    if(root){
        return root->count_elements(num);
    }
    return 0;
}
void tree::add_item(double value){
    records += 1;
    unsigned int mask = (1 <<(sizeof(int)*8-1));
    tree_item** cur = &root;
    for(;(mask&records) == 0;mask = (mask >> 1));
    mask = (mask >> 1);
    while(mask > 0){
        if((mask&records) == 0){
            cur = &((*cur)->left);
        }else{
            cur = &((*cur)->right);
        }
        mask = (mask >> 1);
    }
    *cur = new tree_item(value);
}
tree::tree(){
    root = nullptr;
    records = 0;
};
tree::~tree(){
    if (root){
        delete root;
    }
}