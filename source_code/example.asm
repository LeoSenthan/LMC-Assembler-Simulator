        INP         
        STA FIRST   
        INP   
        SUB ONE     
        STA SECOND

LOOP    LDA SECOND
        SUB ONE
        STA SECOND
        LDA RESULT
        ADD FIRST
        STA RESULT
        LDA SECOND
        BRP LOOP

        LDA RESULT
        OUT         
        HLT        

FIRST   DAT 0 
SECOND  DAT 0 
RESULT  DAT 0
ONE     DAT 1