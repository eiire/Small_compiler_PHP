intro = '.intel_syntax noprefix\n.global main\n.LC0:\n.string \"%d\\n\"\nmain:\npush rbp\n' \
        'mov rbp, rsp\n'

marker = 0
marker_break = -1

displace = 0


def generate_assebler(childs):
    global displace
    asm_container = ''

    for node in childs:
        if node["kind"] == "assign":
            if node["right"][:-1].isdigit():  # a = 10
                asm_container += f"mov DWORD PTR [rbp-{node['displace']}], {node['right']}" + "\n"
            else:  # a = b
                temp = None
                right = node["right"][:-1]  # variable
                displace_right = None  # displace variable
                flag = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace_right = temp["displace"]
                        flag = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and flag is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace_right = temp["displace"]
                            flag = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right}]\nmov DWORD PTR [rbp-{node['displace']}], eax\n"
        elif node["kind"] == "assign_expression":
            op = {
                "operator_sum": "add ",
                "operator_substruction": "sub ",
                "operator_multiplication": "imul ",
                "operator_division": "idiv ",
                "operator_mod": "idiv "
            }
            cdq = ""
            if node["right"]["kind"] == "operator_division" or node["right"]["kind"] == "operator_mod":
                cdq = "cdq\n"
            if not node["right"]["left"].isdigit() and not node["right"]["right"].isdigit():  # a + b
                temp = None
                right_1 = node["right"]["left"]
                right_2 = node["right"]["right"]
                displace_right_1 = None  # variable
                displace_right_2 = None
                found = False
                for temp in childs:
                    if temp.get("left") == right_1:
                        displace_right_1 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right_1:
                            displace_right_1 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                    
                found = False
                for temp in childs:
                    if temp.get("left") == right_2:
                        displace_right_2 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right_2:
                            displace_right_2 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                if node["right"]["kind"] != "operator_mod":
                    if node["right"]["kind"] == "operator_division":
                        asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + cdq + op[node["right"]["kind"]]+ f"DWORD PTR [rbp-{displace_right_2}]\n" + f"mov DWORD PTR [rbp-{node['displace']}], eax\n"
                    else:
                        asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, DWORD PTR [rbp-{displace_right_2}]\n" + op[node["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{node['displace']}], eax\n"
                else:
                    if node["right"]["kind"] == "operator_mod":
                        asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + cdq + op[node["right"]["kind"]]+ f"DWORD PTR [rbp-{displace_right_2}]\n" + f"mov DWORD PTR [rbp-{node['displace']}], edx\n"
                    else:
                        asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, DWORD PTR [rbp-{displace_right_2}]\n" + op[node["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{node['displace']}], edx\n"

            elif not node["right"]["left"].isdigit() and node["right"]["right"].isdigit():  # a + 10
                temp = None
                right_1 = node["right"]["left"]
                displace_right_1 = None  # variable
                displace_right_1 = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == right_1:
                        displace_right_1 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right_1:
                            displace_right_1 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                if node["right"]["kind"] != "operator_mod":
                    if node["right"]["kind"] == "operator_division":
                        asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + cdq + op[node["right"]["kind"]]+ f"{node['right']['right']}\n" + f"mov DWORD PTR [rbp-{node['displace']}], eax\n"
                    else:
                        asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, {node['right']['right']}\n" + op[node["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{node['displace']}], eax\n"
                else:
                    if node["right"]["kind"] == "operator_mod":
                        asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + cdq + op[node["right"]["kind"]]+ f"{node['right']['right']}\n" + f"mov DWORD PTR [rbp-{node['displace']}], edx\n"
                    else:
                        asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, {node['right']['right']}\n" + op[node["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{node['displace']}], edx\n"
                    # asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n"+ cdq + op[node["right"]["kind"]] + f"eax, {node['right']['right']}\nmov DWORD PTR [rbp-{node['displace']}], edx\n"

            elif node["right"]["left"].isdigit() and not node["right"]["right"].isdigit():  # 10 + a
                temp = None
                right_1 = node["right"]["right"]
                displace_right_1 = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == right_1:
                        displace_right_1 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right_1:
                            displace_right_1 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov eax, {node['right']['left']}\nmov edx, DWORD PTR [rbp-{displace_right_1}]\n" + op[node["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{node['displace']}], eax\n"

            elif node["right"]["left"].isdigit() and node["right"]["right"].isdigit():  # a = 10 + 10
                asm_container += f"mov eax, {node['right']['right']}\n" + op[node["right"]["kind"]] + f"eax, {node['right']['left']}\nmov DWORD PTR [rbp-{node['displace']}], eax\n"

        elif node['kind'] == 'keyword_echo':
            if not node['elements'][:-1].isdigit():
                temp = None
                right = node["elements"][:-1]  # variable
                displace = None  # displace variable
                found = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")

                asm_container += f"mov eax, DWORD PTR [rbp-{displace}]\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\nmov eax, 0\n"
            else:
                asm_container += f"mov eax,{node['elements']}\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\nmov eax, 0\n"
        elif node['kind'] == 'keyword_if':
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
            if node["condition"]["left"].isdigit() and node["condition"]["right"].isdigit():
                asm_container += f"mov edx, {node['condition']['left']}\nmov eax, {node['condition']['right']}\n"
            elif not node["condition"]["left"].isdigit() and node["condition"]["right"].isdigit(): # if (a == 10)
                temp = None
                left = node["condition"]["left"]
                displace = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == left:
                        displace = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == left:
                            displace = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")

                asm_container += f"mov edx, DWORD PTR[rbp-{displace}]\nmov eax, {node['condition']['right']}\n"
            elif node["condition"]["left"].isdigit() and not node["condition"]["right"].isdigit(): # if (10 == a)
                temp = None
                right = node["condition"]["right"]
                displace = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov edx, {node['condition']['left']}\nmov eax, DWORD PTR[rbp-{displace}]\n"
            elif not node["condition"]["left"].isdigit() and not node["condition"]["right"].isdigit(): # if (b == a)
                temp = None
                left = node["condition"]["left"]
                right = node["condition"]["right"]
                displace_1 = None  # variable
                displace_2 = None
                found = False
                for temp in childs:
                    if temp.get("left") == left:
                        displace_1 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == left:
                            displace_1 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")

                found = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace_2 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace_2 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov edx, DWORD PTR[rbp-{displace_1}]\nmov eax, DWORD PTR[rbp-{displace_2}]\n"
            asm_container += "cmp edx, eax\n"
            asm_container += f"{jump[node['condition']['op']]} .L{marker}\n"
            temp_asm_container, _ = generate_assebler(node['childs'])
            asm_container += temp_asm_container + f".L{marker_end}:\n"
        elif node["kind"] == 'keyword_while':
            #global marker
            marker += 1
            jump = {
                "==": "jne",
                "!=": "je",
                "<": "jge",
                ">": "jle"
            }
            asm_container += f".L{marker}:\n"
            if node["condition"]["left"].isdigit() and node["condition"]["right"].isdigit():
                asm_container += f"mov edx, {node['condition']['left']}\nmov eax, {node['condition']['right']}\n"
            elif not node["condition"]["left"].isdigit() and node["condition"]["right"].isdigit(): # while (a == 10)
                temp = None
                left = node["condition"]["left"]
                displace = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == left:
                        displace = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node.get("cur_grandpa_childs")
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == left:
                            displace = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")

                asm_container += f"mov edx, DWORD PTR[rbp-{displace}]\nmov eax, {node['condition']['right']}\n"
            elif node["condition"]["left"].isdigit() and not node["condition"]["right"].isdigit(): # while (10 == a)
                temp = None
                right = node["condition"]["right"]
                displace = None  # variable
                found = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov edx, {node['condition']['left']}\nmov eax, DWORD PTR[rbp-{displace}]\n"
            elif not node["condition"]["left"].isdigit() and not node["condition"]["right"].isdigit(): # while (b == a)
                temp = None
                left = node["condition"]["left"]
                right = node["condition"]["right"]
                displace_1 = None  # variable
                displace_2 = None
                found = False
                for temp in childs:
                    if temp.get("left") == left:
                        displace_1 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == left:
                            displace_1 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")

                found = False
                for temp in childs:
                    if temp.get("left") == right:
                        displace_2 = temp["displace"]
                        found = True
                        break
                cur_grandpa_childs = node["cur_grandpa_childs"]
                while cur_grandpa_childs is not None and found is False:
                    for temp in cur_grandpa_childs:
                        if temp.get("left") == right:
                            displace_2 = temp["displace"]
                            found = True
                            break
                    cur_grandpa_childs = cur_grandpa_childs[-1].get("cur_grandpa_childs")
                asm_container += f"mov edx, DWORD PTR[rbp-{displace_1}]\nmov eax, DWORD PTR[rbp-{displace_2}]\n"
            asm_container += "cmp edx, eax\n"

            marker_start = marker
            marker += 1
            marker_end = marker
            asm_container += f"{jump[node['condition']['op']]} .L{marker}\n"
            global marker_break
            marker_break_end = marker_break
            marker_break = marker_end
            temp_asm_container, _ = generate_assebler(node['childs'])
            asm_container += temp_asm_container
            marker_break = marker_break_end
            asm_container += f"jmp .L{marker_start}\n"
            asm_container += f".L{marker_end}:\n"

        elif node.get("kind") == "keyword_break":
            asm_container += f"jmp .L{marker_break}\n"

    return asm_container, displace
