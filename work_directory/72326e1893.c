#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    char entity_3[11];        // Tag.BODY
    int entity_8;             // Tag.BODY
    int entity_5;             // Tag.BODY
    int entity_6;             // Tag.BODY
    entity_8 = 81;            // Tag.BODY
    entity_6 = 73;            // Tag.BODY
    entity_5 = 47;            // Tag.BODY
    char entity_1[5];         // Tag.BODY
    if(entity_6 < entity_8){  // Tag.BODY
    entity_3[entity_5] = 'R'; // Tag.BUFWRITE_TAUT_UNSAFE
    entity_6 = 68;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_6 = 77;            // Tag.BODY
    }                         // Tag.BODY
    entity_1[entity_6] = 'H'; // Tag.BUFWRITE_COND_UNSAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER