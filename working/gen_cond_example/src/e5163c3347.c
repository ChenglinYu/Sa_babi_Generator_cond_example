#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_1;             // Tag.BODY
    int entity_6;             // Tag.BODY
    char entity_8[66];        // Tag.BODY
    int entity_5;             // Tag.BODY
    entity_1 = 83;            // Tag.BODY
    entity_8[entity_1] = 'F'; // Tag.BUFWRITE_TAUT_UNSAFE
    char entity_7[50];        // Tag.BODY
    entity_5 = 12;            // Tag.BODY
    entity_6 = 60;            // Tag.BODY
    if(entity_6 < entity_5){  // Tag.BODY
    entity_6 = 80;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_6 = 10;            // Tag.BODY
    }                         // Tag.BODY
    int entity_0;             // Tag.BODY
    entity_7[entity_6] = '1'; // Tag.BUFWRITE_COND_SAFE
    char entity_3[5];         // Tag.BODY
    entity_0 = 26;            // Tag.BODY
    entity_3[entity_0] = 'H'; // Tag.BUFWRITE_TAUT_UNSAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER