#include <iostream>

using namespace std;

typedef unsigned char byte;

int main()
{
    byte x[4];
    float y = 1.2;
    unsigned char const * p = reinterpret_cast<unsigned char const *>(&y);
    for (int i =3; i >= 0; -- i){
    //int z = (int)y;
        //cout<<hex<<(int)p[i]<< endl;
        x[3-i] = (int)p[i];
    }
    for (int i=0; i<4;i++) cout << hex << (int)x[i] << endl;
    return 0;
}
