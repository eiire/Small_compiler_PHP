intro = '.intel_syntax noprefix\n.global main\n.LC0:\n.string \"%d\\n\"\nmain:\npush rbp\n' \
        'mov rbp, rsp\nsub rsp, '

marker = 0
marker_break = -1

displace = 0


def jopafunction(children, parent):
    asm_container = ''

    for i in children:
        if i["kind"] == "assign":
            if i["right"][:-1].isdigit():  # a = 10
                asm_container += f"mov DWORD PTR [rbp-{i['displace']}], {i['right']}" + "\n"
            else:  # a = b
                temp = None
                right = i["right"][:-1]  # variable
                displace_right = None  # displace variable
                flag = False
                for temp in children:
                    if temp.get("left") == right:
                        displace_right = temp["displace"]
                        flag = True
                        break
                parent = i["parent"]
                print(parent)
                while parent is not None and flag is False:
                    for temp in parent:
                        print(temp, right)
                        if temp.get("left") == right:
                            displace_right = temp["displace"]
                            flag = True
                            break
                    parent = parent[-1]["parent"]
                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right}]\nmov DWORD PTR [rbp-{i['displace']}], eax\n"
        elif i["kind"] == "assign_expression":
            op = {
                "operator_sum": "add ",
                "operator_substruction": "sub ",
                "operator_multiplication": "imul ",
                "operator_division": "idiv "
            }
            if not i["right"]["left"].isdigit() and not i["right"]["right"].isdigit():  # a + b
                temp = None
                right_1 = i["right"]["left"]
                right_2 = i["right"]["right"]
                displace_right_1 = None  # variable
                displace_right_2 = None
                for temp in children:
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break

                for temp in children:
                    if temp["left"] == right_2:
                        displace_right_2 = temp["displace"]
                        break
                asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, DWORD PTR [rbp-{displace_right_2}]\n" + op[i["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif not i["right"]["left"].isdigit() and i["right"]["right"].isdigit():  # a + 10
                temp = None
                right_1 = i["right"]["left"]
                displace_right_1 = None  # variable
                for temp in children:
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break
                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + op[i["right"]["kind"]] + f"eax, {i['right']['right']}\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif i["right"]["left"].isdigit() and not i["right"]["right"].isdigit():  # 10 + a
                temp = None
                right_1 = i["right"]["right"]
                displace_right_1 = None  # variable
                for temp in children:
                    print(temp)
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break
                asm_container += f"mov eax, {i['right']['left']}\nmov edx, DWORD PTR [rbp-{displace_right_1}]\n" + op[i["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif i["right"]["left"].isdigit() and i["right"]["right"].isdigit():  # a = 10 + 10
                asm_container += f"mov eax, {i['right']['right']}\n" + op[i["right"]["kind"]] + f"eax, {i['right']['left']}\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

        elif i['kind'] == 'keyword_echo':
            if not i['elements'][:-1].isdigit():
                temp = None
                right = i["elements"][:-1]  # variable
                displace_right = None  # displace variable
                if parent is None:
                    for temp in children:
                        if temp.get("left") == right:#if temp["left"] == right:
                            displace_right = temp["displace"]
                            break
                else:
                    for temp in parent:
                        if temp.get("left") == right:#if temp["left"] == right:
                            displace_right = temp["displace"]

                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right}]\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\nmov eax, 0\n"
            else:
                asm_container += f"mov eax,{i['elements']}\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\nmov eax, 0\n"
        elif i['kind'] == 'keyword_if':
            global marker
            marker += 1
            marker_end = marker
            marker_else = marker_end
            jump = {
                "==": "jne",
                "!=": "je",
                "<": "jge",
                ">": "jle"
            }
            if i["condition"]["left"].isdigit() and i["condition"]["right"].isdigit():
                asm_container += f"mov edx, {i['condition']['left']}\nmov eax, {i['condition']['right']}\n"
            elif not i["condition"]["left"].isdigit() and i["condition"]["right"].isdigit(): # if (a == 10)
                temp = None
                left = i["condition"]["left"]
                displace = None  # variable
                found = False
                for temp in children:
                    if temp.get("left") == left:
                        displace = temp["displace"]
                        found = True
                        break
                parent = i["parent"]
                while parent is not None and found is False:
                    for temp in parent:
                        if temp.get("left") == left:
                            displace = temp["displace"]
                            found = True
                            break
                    parent = parent[-1]["parent"]

                asm_container += f"mov edx, DWORD PTR[rbp-{displace}]\nmov eax, {i['condition']['right']}\n"
            elif i["condition"]["left"].isdigit() and not i["condition"]["right"].isdigit(): # if (10 == a)
                temp = None
                right = i["condition"]["right"]
                displace = None  # variable
                for temp in children:
                    if temp["left"] == right:
                        displace = temp["displace"]
                        break
                asm_container += f"mov edx, {i['condition']['left']}\nmov eax, DWORD PTR[rbp-{displace}]\n"
            elif not i["condition"]["left"].isdigit() and not i["condition"]["right"].isdigit(): # if (b == a)
                temp = None
                left = i["condition"]["left"]
                right = i["condition"]["right"]
                displace_1 = None  # variable
                displace_2 = None
                for temp in children:
                    if temp["left"] == left:
                        displace_1 = temp["displace"]
                        break

                for temp in children:
                    if temp["left"] == right:
                        displace_2 = temp["displace"]
                        break
                asm_container += f"mov edx, DWORD PTR[rbp-{displace_1}]\nmov eax, DWORD PTR[rbp-{displace_2}]\n"
            asm_container += "cmp edx, eax\n"
            asm_container += f"{jump[i['condition']['op']]} .L{marker}\n"
            temp_asm_container = jopafunction(i['children'], children)
            asm_container += temp_asm_container + f".L{marker_end}:\n"

    return asm_container