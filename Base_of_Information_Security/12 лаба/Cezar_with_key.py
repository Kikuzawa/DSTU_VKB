def cezar_with_key_rus(text, keyword, step):
    key_ = ''
    for i in keyword:
        if i not in key_:
            key_ += i
    if step < 0:
        flag = 1
        step = step * (-1)
    else:
        flag = 0
    key = key_
    phrases = text
    alpha = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    tmp = ''
    for element in alpha:
        if element not in key:
            tmp += element

    alpha_new = tmp[-step:] + key + tmp[:-step]

    if flag == 0:
        return phrases.translate(str.maketrans(alpha, alpha_new))
    else:
        return phrases.translate(str.maketrans(alpha_new, alpha))

def cezar_with_key_eng(text, keyword, shift): #ABCDEFGHIJKLMNOPQRSTUVWXYZ
    try:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_length = len(alphabet)
        message = text.upper()
        encrypted_message = ""
        keyword = keyword.upper()
        keyword_length = len(keyword)
        if shift < 0:
            flag = -1
        else:
            flag = 1

        for i, char in enumerate(message):
            if char.isalpha():
                shift = flag * (alphabet.index(keyword[i % keyword_length].upper())) + shift
                new_char = alphabet[(alphabet.index(char.upper()) + shift) % alphabet_length]
                if char.isupper():
                    new_char = new_char.upper()
                encrypted_message += new_char
            else:
                encrypted_message += char

        return encrypted_message
    except Exception as e:
        return str(e)
