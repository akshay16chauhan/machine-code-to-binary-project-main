import sys

REG_data={"00000":0,"00001":0,"00010":256,"00011":0,"00100":0,"00101":0,"00110":0,"00111":0,
           "01000":0, "01001":0,"01010":0, "01011":0,
           "01100":0, "01101":0,"01110":0, "01111":0,
            "10000":0,"10001":0, "10010":0,"10011":0,"10100":0,"10101":0,"10110":0,"10111":0,
            "11000":0, "11001":0,"11010":0, "11011":0 ,"11100":0,"11101":0,"11110":0,"11111":0}  

mem_data={65536: 0, 65540: 0, 65544: 0, 65548: 0, 65552: 0, 65556: 0, 65560: 0,
        65564: 0, 65568: 0, 65572: 0, 65576: 0, 65580: 0, 65584: 0, 65588: 0,
        65592: 0, 65596: 0, 65600: 0, 65604: 0, 65608: 0, 65612: 0, 65616: 0,
        65620: 0, 65624: 0, 65628: 0, 65632: 0, 65636: 0, 65640: 0, 65644: 0,
        65648: 0, 65652: 0, 65656: 0, 65660: 0}

def right_shift(value, shift_amount):
    return value // (2 ** shift_amount)

def left_shift(value, shift_amount):
    return value * (2 ** shift_amount)

def binary_to_decimal(binary_str, bits, is_twos_complement=True):
    decimal_val = 0
    if is_twos_complement and binary_str[0] == '1':
        binary_list = [int(bit) for bit in binary_str]
        for i in range(bits):
            binary_list[i] = 1 - binary_list[i]
        for i in range(bits-1, -1, -1):
            if binary_list[i] == 0:
                binary_list[i] = 1
                break
            else:
                binary_list[i] = 0
        complement_str = ''.join(map(str, binary_list))
        decimal_val = -int(complement_str, 2)
    else:
        decimal_val = int(binary_str, 2)
    
    return decimal_val

def decimal_to_binary(decimal, num_bits):
    binary = ""
    for i in range(num_bits - 1, -1, -1):
        bit = (decimal >> i) & 1
        binary += str(bit)
    return binary

def Convert_hex(binary):
    decimal = int(binary, 2)
    hex_num = hex(decimal)
    return  hex_num

def to_hex_string(i, length):
    hex_string = hex(i)[2:].upper()  # Convert integer to hexadecimal string, remove '0x' prefix, and convert to uppercase
    padded_hex_string = '0' * (length - len(hex_string)) + hex_string  # Pad with zeros to the desired length
    return padded_hex_string  

file_int=sys.argv[1]
file_out= sys.argv[2]
# file_int="/Users/abhishekrao/Documents/vscode/python/read.txt"
# file_out= "/Users/abhishekrao/Documents/vscode/python/write.txt"

f=open(file_int,'r')
text=[]
for line in f:
    text.append(line)
f.close

for i in range(len(text)-1):
    text[i]=text[i][0:-1]

f1= open(file_out,'w')

program_counter=0

I_list=["0000011","0010011","0010011","1100111"]
S_list=["0100011"]
B_list=["1100011"]
U_list=["0110111","0010111"]
J_list= ["1101111"]

# print(mem_data)
visualH=False
while True:
    line= text[program_counter//4]
    if  line=='00000000000000000000000001100011'  : 
        visualH=True
        REG_data["00000"] = 0
        REG_data_output_list = []
        for i in range(0, 32):
            register_value = REG_data[decimal_to_binary(i, 5)]
            binary_value = decimal_to_binary(register_value, 32)
            REG_data_output_list.append("0b" + binary_value)
        REG_data_output = " ".join(REG_data_output_list)
        output = "0b" + decimal_to_binary(program_counter, 32) + " " + REG_data_output + "\n"
        f1.write(output)
        break
 
    elif line[-7:] in U_list: 
         op = line[-7:]
         program_counter+=4

         if op == '0110111': 
            imm = line[-32:-12] 
            rd = line[-12:-7] 
            imm_value = binary_to_decimal(imm, 32)
            REG_data[rd] = imm_value * 4096
         elif op == '0010111': 
            imm = line[-32:-12]
            rd = line[-12:-7] 
            imm_value = binary_to_decimal(imm, 32)
            REG_data[rd] = program_counter + (imm_value * (2 ** 12)) - 4


    elif line[-7:] in J_list: 
         imm= line[-32]+ line[-20:-12]+ line[-21]+line[-31:-21]
         rd=line[-12:-7]
         REG_data[rd]= program_counter+4
         program_counter+= binary_to_decimal(imm+"0", 21)
         program_counter= decimal_to_binary(program_counter,32)
         program_counter= program_counter[:-1]+"0"

         program_counter = binary_to_decimal(program_counter,32)

    elif line[-7:] in S_list: 
         program_counter+=4
         imm= line[-32:-25]+ line[-12:-7]
         rs2= line[-25:-20]
         rs1= line[-20:-15]
         mem= REG_data[rs1]+ binary_to_decimal(imm,12)
         mem_data[mem]= REG_data[rs2]

    
    elif line[-7:] =="0110011":
        program_counter+=4
        op = line[-7:]
        data1 = line[-15:-12]
        data2 = line[-32:-25]
        rs1 = line[-20:-15]
        rs2 = line[-25:-20]
        rd = line[-12:-7]
        if data1 == '000' and data2 == '0000000': 
            REG_data[rd] = REG_data[rs1] + REG_data[rs2]
        elif data1 == '000' and data2 == '0100000': 
            REG_data[rd] = REG_data[rs1] - REG_data[rs2]
        elif data1 == '001' :
            shifted_value = left_shift(REG_data[rs1], binary_to_decimal(decimal_to_binary(REG_data[rs2], 5), 5, False))
            REG_data[rd] = shifted_value
        elif data1 == '010' :
            if REG_data[rs1] < REG_data[rs2]:
                REG_data[rd]=1

        elif data1 == '011' :
            if binary_to_decimal(decimal_to_binary(REG_data[rs1],4),5,False) < binary_to_decimal(decimal_to_binary(REG_data[rs2],4),5,False):
                REG_data[rd]=1
        elif data1 == '100' :
            REG_data[rd]= REG_data[rs1] ^ REG_data[rs2]
        elif data1 == '101' : 
            rs1_value = REG_data[rs1]
            rs2_value = binary_to_decimal(decimal_to_binary(REG_data[rs2], 4), 5, False)
            result = right_shift(rs1_value, rs2_value)
            REG_data[rd] = result
        elif data1== "110" : 
            REG_data[rd]= REG_data[rs1] | REG_data[rs2]
        elif data1== "111" : 
            REG_data[rd]= REG_data[rs1] & REG_data[rs2]

    elif (line)[-7:] in B_list: 
            program_counter+=4
            imm=""
            rs1= line[-20:-15]
            rs2= line[-25:-20]
            imm= line[-32]+line[-8]+ line[ -31:-25]+ line[-12:-8] +"0" 
            imm= binary_to_decimal( imm, 13)
            func3= line [-15:-12]
            if func3== "110": 
                if REG_data[rs1] < REG_data[rs2]:
                    program_counter-=4
                    program_counter+= imm
            elif func3== "111": 
                if REG_data[rs1] >= REG_data[rs2]:
                    program_counter-=4
                    program_counter+=imm
            elif func3== "000": 
                if REG_data[rs1]==REG_data[rs2]:
                    if rs1== "00000":
                        break  
                    program_counter-=4                 
                    program_counter+=imm
            elif func3== "001": 
                if REG_data[rs1]!=REG_data[rs2]:
                    program_counter-=4
                    program_counter+=imm
            elif func3== "101": 
                if REG_data[rs1] >= REG_data[rs2]:
                    program_counter-=4
                    program_counter+= imm
            elif func3== "100": 
                if REG_data[rs1] < REG_data[rs2]:
                    program_counter-=4
                    program_counter+= imm

    elif line[-7:] in I_list: 
         program_counter+=4
         funct3= line[-15:-12]
         rd= line[-12:-7]
         rs= line[-20:-15]
         imm= line[-32:-20]
         op= line[-7:]
         if op== "1100111" and funct3=="000": 
             REG_data[rd]= program_counter
             program_counter-=4
             program_counter= REG_data[rs]+ int(imm,2)
             program_counter= decimal_to_binary(program_counter,32)
             program_counter= program_counter[:-1]+"0"

             program_counter = binary_to_decimal(program_counter,32)
            
         
         elif op=="0010011" and funct3== "000": 
             REG_data[rd]= REG_data[rs]+ binary_to_decimal(imm, 12)

         elif op=="0000011" and funct3=="010":
            REG_data[rd]= mem_data[REG_data[rs1]+ binary_to_decimal(imm,12)]
         elif op== "0010011" and funct3== "011": 
             if binary_to_decimal(decimal_to_binary(REG_data[rs],12),13,False) < binary_to_decimal(decimal_to_binary(REG_data[imm],12),13,False):
                 REG_data[rd]= 1

    else: 
        print("Error : op code not found")
        break


    REG_data["00000"] = 0
    REG_data_output_list = []
    for i in range(0, 32):
        register_binary = decimal_to_binary(REG_data[decimal_to_binary(i, 5)], 32)
        REG_data_output_list.append("0b" + register_binary)

    REG_data_output = " ".join(REG_data_output_list)
    output = "0b" + decimal_to_binary(program_counter, 32) + " " + REG_data_output + "\n"
    f1.write(output)

n = ""
for i in mem_data.keys():
    mem_hex = to_hex_string(i, 8)
    n += "0x" + mem_hex.lower() + ":0b" + decimal_to_binary(mem_data[i], 32) + "\n"

f1.write(n)
f1.close()
