#include <stdio.h>
#include "../tester/Vdm_ASN1_Types.h"

int main(){
    /*
     * Tester.c is used to test the generated code functions.
     * The tests provided are the following:
     * INTEGER [X]
     * BOOLEAN [X]
     * SEQUENCE OF INTEGER []
     * SEQUENCE OF BOOLEAN []
     * ENUM []
     * OCTET STRING [] 
     *
     */

    // INTEGER
    printf("Test INTEGER\n");
    asn1SccMInt mint = 10;
    printf("ASN1SCC Source MInt=%d\n", mint); 
    TVP vdm_mint;
    Convert_MInt_from_ASN1SCC_to_VDM(&vdm_mint, &mint);
    printf("VDM Dest MInt=%d\n\n", vdm_mint->value.intVal);
    vdm_mint->value.intVal = 5;
    printf("VDM Source MInt=%d\n", vdm_mint->value.intVal);
    Convert_MInt_from_VDM_to_ASN1SCC(&mint, vdm_mint);
    printf("ASN1SCC Dest MInt=%d\n\n", mint); 

    // BOOLEAN
    printf("Test BOOLEAN\n");
    asn1SccMBool mbool = TRUE;
    printf("ASN1SCC Source MBool=%d\n", mbool); 
    TVP vdm_mbool;
    Convert_MBool_from_ASN1SCC_to_VDM(&vdm_mbool, &mbool);
    printf("VDM Dest MBool=%d\n\n", vdm_mbool->value.boolVal);
    vdm_mbool->value.boolVal = false;
    printf("VDM Source MBool=%d\n", vdm_mbool->value.boolVal);
    Convert_MBool_from_VDM_to_ASN1SCC(&mbool, vdm_mbool);
    printf("ASN1SCC Dest MBool=%d\n\n", mbool); 

    // SEQUENCE OF INTEGER
    printf("Test SEQUENCE OF INTEGER\n");
    printf("ASN1SCC Source MSeqI\n");
    asn1SccMSeqI mseq_i = (asn1SccMSeqI) { .arr= {1,2,3,4,5}}; 
    int size =  sizeof(mseq_i.arr)/sizeof(mseq_i.arr[0]);
    for(int i=0; i < size; i++ )
        printf("%d ", mseq_i.arr[i]);
    printf("\n");
    TVP mseq_i_vdm = newSeq(size);
    Convert_MSeqI_from_ASN1SCC_to_VDM(&mseq_i_vdm, &mseq_i);
    UNWRAP_COLLECTION(col, mseq_i_vdm);
    printf("VDM Dest MSeqI\n");
    for(int i=0; i < size; i++)
        printf("%d ", ((TVP) col->value[i])->value.intVal);   
    printf("\n");
    col->value[3]->value.intVal = 10;
    printf("VDM Source MSeqI\n");
    for(int i=0; i < size; i++)
        printf("%d ", ((TVP) col->value[i])->value.intVal);   
    printf("\n");
    Convert_MSeqI_from_VDM_to_ASN1SCC(&mseq_i, &mseq_i_vdm);
    printf("ASN1SCC Dest MSeqI\n");
    for(int i = 0; i < size; i++)
        printf("%d " , mseq_i.arr[i]);
    printf("\n\n");

    // SEQUENCE OF BOOLEAN
    printf("Test SEQUENCE OF BOOLEAN\n");
    printf("ASN1SCC Source MSeqB\n");
    asn1SccMSeqB mseq_b = (asn1SccMSeqB) { .arr= {TRUE, FALSE, FALSE, FALSE, TRUE}}; 
    size =  sizeof(mseq_b.arr)/sizeof(mseq_b.arr[0]);
    for(int i=0; i < size; i++ )
        printf("%d ", mseq_b.arr[i]);
    printf("\n");
    TVP mseq_b_vdm = newSeq(size);
    Convert_MSeqB_from_ASN1SCC_to_VDM(&mseq_b_vdm, &mseq_b);
    UNWRAP_COLLECTION(col_b, mseq_b_vdm);
    printf("VDM Dest MSeqB\n");
    for(int i=0; i < size; i++)
        printf("%d ", ((TVP) col_b->value[i])->value.boolVal);   
    printf("\n");
    col_b->value[3]->value.boolVal = true;
    printf("VDM Source MSeqB\n");
    for(int i=0; i < size; i++)
        printf("%d ", ((TVP) col_b->value[i])->value.boolVal);   
    printf("\n");
    Convert_MSeqB_from_VDM_to_ASN1SCC(&mseq_b, &mseq_b_vdm);
    printf("ASN1SCC Dest MSeqB\n");
    for(int i = 0; i < size; i++)
        printf("%d " , mseq_b.arr[i]);
    printf("\n\n");   
    return 0;

}
