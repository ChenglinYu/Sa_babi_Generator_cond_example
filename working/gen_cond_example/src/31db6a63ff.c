#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_2;             // Tag.BODY
    int entity_4;             // Tag.BODY
    char entity_9[28];        // Tag.BODY
    entity_4 = 8;             // Tag.BODY
    entity_2 = 33;            // Tag.BODY
    if(entity_4 < entity_2){  // Tag.BODY
    entity_4 = 9;             // Tag.BODY
    } else {                  // Tag.BODY
    entity_4 = 82;            // Tag.BODY
    }                         // Tag.BODY
    entity_9[entity_4] = 'j'; // Tag.BUFWRITE_COND_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER