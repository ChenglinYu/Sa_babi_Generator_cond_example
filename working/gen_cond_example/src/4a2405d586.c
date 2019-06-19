#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_1;             // Tag.BODY
    int entity_7;             // Tag.BODY
    char entity_0[24];        // Tag.BODY
    entity_7 = 75;            // Tag.BODY
    char entity_9[86];        // Tag.BODY
    int entity_8;             // Tag.BODY
    int entity_5;             // Tag.BODY
    char entity_4[90];        // Tag.BODY
    entity_1 = 86;            // Tag.BODY
    entity_5 = 45;            // Tag.BODY
    entity_8 = 89;            // Tag.BODY
    entity_4[entity_1] = 'A'; // Tag.BUFWRITE_TAUT_SAFE
    if(entity_5 < entity_7){  // Tag.BODY
    entity_5 = 81;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_0[entity_8] = 'l'; // Tag.BUFWRITE_TAUT_UNSAFE
    entity_5 = 79;            // Tag.BODY
    }                         // Tag.BODY
    entity_9[entity_5] = '8'; // Tag.BUFWRITE_COND_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER