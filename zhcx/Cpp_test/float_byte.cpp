#include <iostream>
#include <array>

using namespace std;

typedef unsigned char byte;
struct floatarray {byte arr[4];}

floatarray float2byte(float x){
    floatarray y;
    unsigned char const * p = reinterpret_cast<unsigned char const *>(&x);
    for (int i =3; i >= 0; -- i){
        y.arr[3-i] = (byte)p[i];
    }
    return y
}


int main()
{
    floatarray y = float2byte(1.2);
    byte z[4] = y.arr;
    //byte x[4];
    //float y = 1.2;
    //unsigned char const * p = reinterpret_cast<unsigned char const *>(&y);
    //for (int i =3; i >= 0; -- i){
    //int z = (int)y;
    //    //cout<<hex<<(int)p[i]<< endl;
    //    x[3-i] = (int)p[i];
    //}
    for (int i=0; i<4;i++) cout << hex << (int)z[i] << endl;
    return 0;
}
