#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    char entity_8[75];        // Tag.BODY
    int entity_1;             // Tag.BODY
    int entity_5;             // Tag.BODY
    char entity_2[90];        // Tag.BODY
    int entity_4;             // Tag.BODY
    char entity_7[82];        // Tag.BODY
    entity_5 = 80;            // Tag.BODY
    entity_4 = 67;            // Tag.BODY
    int entity_3;             // Tag.BODY
    entity_1 = 89;            // Tag.BODY
    entity_3 = 35;            // Tag.BODY
    if(entity_4 < entity_3){  // Tag.BODY
    entity_4 = 66;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_4 = 30;            // Tag.BODY
    }                         // Tag.BODY
    entity_2[entity_4] = 'S'; // Tag.BUFWRITE_COND_SAFE
    entity_7[entity_1] = 'W'; // Tag.BUFWRITE_TAUT_UNSAFE
    entity_8[entity_5] = 'l'; // Tag.BUFWRITE_TAUT_UNSAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER