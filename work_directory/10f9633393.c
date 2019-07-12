#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_8;             // Tag.BODY
    int entity_4;             // Tag.BODY
    int entity_0;             // Tag.BODY
    char entity_7[89];        // Tag.BODY
    entity_8 = 32;            // Tag.BODY
    entity_4 = 26;            // Tag.BODY
    entity_0 = 86;            // Tag.BODY
    char entity_6[84];        // Tag.BODY
    if(entity_0 < entity_4){  // Tag.BODY
    entity_0 = 98;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_0 = 7;             // Tag.BODY
    }                         // Tag.BODY
    entity_6[entity_8] = '9'; // Tag.BUFWRITE_TAUT_SAFE
    entity_7[entity_0] = 'O'; // Tag.BUFWRITE_COND_SAFE
    char entity_9[56];        // Tag.BODY
    int entity_1;             // Tag.BODY
    entity_1 = 85;            // Tag.BODY
    entity_9[entity_1] = 'b'; // Tag.BUFWRITE_TAUT_UNSAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER