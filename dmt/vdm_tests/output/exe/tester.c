#include <stdio.h>
#include "../tester/Vdm_ASN1_Types.h"

int main(){
     
    printf("\n--\tArray of Bool\n");
    printf("--\tASN Source Bool Array\n");
    asn1SccMSeq s_ab = (asn1SccMSeq) { .arr= {FALSE, FALSE, TRUE, FALSE, FALSE}};    
    TVP out_seq = newSeq(5);

    Convert_MSeq_from_ASN1SCC_to_VDM(&out_seq, &s_ab);
    UNWRAP_COLLECTION(col, out_seq);
    printf("Size: %d\n", col->size);
    for(int i=0; i <5; i++)
        printf("[%d] %d\n", i, ((TVP) col->value[i])->value.boolVal);   
    col->value[3]->value.boolVal = true;
    Convert_MSeq_from_VDM_to_ASN1SCC(&s_ab, &out_seq);
    for(int i = 0; i < 5; i++)
        printf("[%d] %d\n" , i, s_ab.arr[i]);
    return 0;

}
