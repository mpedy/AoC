#include<iostream>
#include <fstream>

using namespace std;

int main(){
    ifstream file("input.txt");
    string line;
    while(getline(file,line)){
        std::stringstream linestream(line);
        string data;
        int val1;
        int val2;
        getline(linestream,data,"\n\n");
    }


}