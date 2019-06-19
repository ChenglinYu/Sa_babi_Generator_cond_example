#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    char entity_2[73];        // Tag.BODY
    int entity_5;             // Tag.BODY
    int entity_8;             // Tag.BODY
    char entity_4[90];        // Tag.BODY
    int entity_1;             // Tag.BODY
    entity_1 = 37;            // Tag.BODY
    entity_8 = 30;            // Tag.BODY
    entity_5 = 70;            // Tag.BODY
    if(entity_1 < entity_5){  // Tag.BODY
    entity_1 = 15;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_2[entity_8] = 'i'; // Tag.BUFWRITE_TAUT_SAFE
    entity_1 = 70;            // Tag.BODY
    }                         // Tag.BODY
    entity_4[entity_1] = 'l'; // Tag.BUFWRITE_COND_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER