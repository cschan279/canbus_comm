#include <iostream>
//#include <array>
#include <cstring>

using namespace std;

typedef unsigned char byte;
// struct floatarray {
//     byte arr[4];
// };

// void float2byte(float f, byte *b){
//     // floatarray y;
// //     unsigned char const * p = reinterpret_cast<unsigned char const *>(&f);
// //     for (int i =3; i >= 0; -- i){
// //         *(b+3-i) = (byte)p[i];
// //     }
// //     return;
//     byte buf[4];
//     memcpy(&buf, &f, 4);
//     for (int i=0;i<4;i++){
//         b[3-i] = buf[i];
//     }
// }
// void byte2float(byte *b, float *f){
//     byte *buf;
//     float fb;
//     for (int i=0;i<4;i++){
//         *(buf+i) = *(b+3-i);
//         cout << hex << (int)*(buf+i) << endl;
//     }
//     cout << 1000000 << *f << endl;
//     memcpy(&fb, &buf, sizeof(fb));
//     *f = fb;
//     cout << 1234567 << endl;
// }
// 
// 
// int main()
// {
//     byte z[4];
//     float2byte(1.2, z);
//     //byte z[4] = y.arr;
//     for (int i=0; i<4;i++) cout << hex << (int)z[i] << endl;
//     
//     byte a[4] = {0x3f, 0x99, 0x99, 0x9a};
//     float *c;
//     byte2float(a, c);
//     cout << *c << endl;
//     
//     
//     return 0;
// }
union {
    float f;
    byte b[4];
} u;

int main() {
    u.f = 1.2;
    for (int i=0; i<4;i++) cout << hex << (int)u.b[i] << endl;
    byte x[] = {0x9a, 0x99, 0x99, 0x3f};
    for (int i=0; i<4;i++) u.b[i] = x[i];
    cout << u.f << endl;
    return 0;
}
