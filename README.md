# yeager
data testing with python

file.yaml - file configuration

command test

regex: string
regex - create python regular expression using supplied string

common strings
- Money : 
- Number : '^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'
- BinaryChoice : "^National$|^State$"
- Integer: "^(0|[1-9][0-9]*)$"
- Zipcode: 
- Email: 
- Two digit code, Not required: "^[0-9]{0,2}$"
- State Abbreviation: "^(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY])$

-

Specialized
- CPT4 : ^[A-Z0-9]{5}$