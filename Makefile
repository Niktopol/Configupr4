(result: main.o tree.o){
"g++ main.o tree.o -o result"
"echo "Компоновка исполняемого файла""
}
(main.o: main.cpp){
"g++ -c main.cpp"
"echo "Компиляция main.cpp""
}
(tree.o: tree.cpp){
"g++ -c tree.cpp"
"echo "Компиляция tree.cpp""
}