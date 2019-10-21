import os, csv, time
from tqdm import tqdm
import termcolor
import colorama
colorama.init()


def select_your_language(): # the function for enter your language / функция ввода языка
    language=input('enter your language/введите язык [rus/eng]: ').lower()
    return language


def start_search_rus(): # блок управления поиском на русском языке
    file_list = list(map(str.lower, input('Введите название искомых файлов и папок через запятую: ').split(','))) # ввод имен для поиска
    file_list = [file_name.strip() for file_name in file_list]
    result=[]
    result_start, result_end = set(file_list), set()
    file_date_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))

    def search_file_in_dir(file_name, result, foldername): # функция поиска файлов и папок внутри папок логического диска
        try:
            for file_dir in os.listdir(foldername): # итерация по списку файлов и папок внутри папок логического диска
                if os.path.isfile(f'{foldername}\\{file_dir}') == True and ('').join(file_dir.split(".")[:-1]).lower() == file_name:
                    result.append('файл найден:'+' '+f'{foldername}\\{file_dir}')
                    return result
                elif os.path.isdir(f'{foldername}\\{file_dir}') == True and file_dir.lower()!= file_name:
                    search_file_in_dir(file_name, result, foldername=f'{foldername}\\{file_dir}')
                elif os.path.isdir(f'{foldername}\\{file_dir}') == True and file_dir.lower()== file_name:
                    result.append('папка найдена:' + ' '+f'{foldername}\\{file_dir}')
                    search_file_in_dir(file_name, result, foldername=f'{foldername}\\{file_dir}')
                else: continue
        except PermissionError: # Исключение. Если папка не существует
            pass

    def search_file_in_drive(list_drives, file_name):
        for name_drives in list_drives: # проход по списку дисков.
            try:                        # если диск существует
                for foldername in tqdm(os.listdir(name_drives), desc='проверенно файлов и папок на диске ' + name_drives[0]): # итерация по списку файлов и папок на логическом диске
                    if os.path.isfile(f'{name_drives}{foldername}')== True and ('').join(foldername.split(".")[:-1]).lower()== file_name:
                        result.append('файл найден:'+' '+f'{name_drives}{foldername}')
                    elif os.path.isdir(f'{name_drives}{foldername}')== True and foldername.lower()== file_name:
                        result.append('папка найдена:' + ' ' + f'{name_drives}{foldername}')
                        search_file_in_dir(file_name, result, foldername=f'{name_drives}{foldername}')
                    elif os.path.isdir(f'{name_drives}{foldername}')== True and foldername.lower()!= file_name:
                        search_file_in_dir(file_name, result, foldername=f'{name_drives}{foldername}')
                    else:
                        continue
            except FileNotFoundError:   # Исключение, если диск не существует
                continue

    def get_file_name(file_list=[]): # функция получения имени файла или папки для поиска
        for file_name in file_list:  # итерация по списку имен введенных для поиска
            if file_name == '': continue
            else:
                termcolor.cprint('проверяется наименование: '+file_name, 'yellow')
                search_file_in_drive(list_drives, file_name)
        os.system('cls')

    def get_not_find(result_start=set()): # функция получения найденных файлов без адреса в ОС
        cor_result = [name.lower() for name in result]
        for element in result_start:
            for name in cor_result:
                if name.endswith(element) or ('').join(name.split(".")[:-1]).endswith(element): result_end.add(element)
                else: continue
        return result_end



    get_file_name(file_list)
    result_end = get_not_find(result_start)
    if result_start-result_end==set():
        result_not_find=['все имена найдены']
        termcolor.cprint('все имена найдены','green')
    elif result_start-result_end!=set() and result_start-result_end!=result_start:
        result_not_find=list(result_start-result_end)
        [termcolor.cprint('наименование не найдено: ' + res_not, 'red') for res_not in result_not_find]  # вывод файлов и папок в терминал не найденных на ПК
    elif result_start-result_end!=set() and result_start-result_end==result_start:
        termcolor.cprint('имена не найдены', 'red')
        result_not_find=['имена не найдены']


    if (file_list == [] or file_list == [' ']): termcolor.cprint('Вы не ввели имена для поиска. Список пуст', 'red')
    [termcolor.cprint(res_like, 'green') for res_like in result] # вывод файлов и папок в терминал найденных на ПК


    def save_search(result=[]): # сохранить результаты поиска
        with open(f'результат_поиска_{file_date_time}.csv',  'w') as resultFile:
            wr = csv.writer(resultFile, delimiter=';')
            for item in result:
                wr.writerow([item])
            for item in result_not_find:
                wr.writerow(['файл не найден: ']+[item])

    def quest_save(): # функция запроса на сохранения результатов поиска
        quest_s = input('сохранить результаты поиска [да/нет]: ').lower()
        if quest_s.lower() == "да": return True
        elif quest_s.lower() == "нет": return False
        else: return None

    while True: # сохранение результатов поиска
        quest = quest_save()
        if quest == True:
            save_search(result)
            break
        elif quest == False: break
        else: termcolor.cprint('Неправильный ввод. Необходимо ввести [да/нет]', 'red')





def start_search_eng(): # english language search control unit
    file_list = list(map(str.lower, input('input name of search files and folders using comma: ').split(','))) # input name of search
    file_list = [file_name.strip() for file_name in file_list]
    result = []
    result_start, result_end = set(file_list), set()
    file_date_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))

    def search_file_in_dir(file_name, result, foldername): # the function for search in folder of folders
        try:
            for file_dir in os.listdir(foldername): # sort out for search in folder of folders
                if os.path.isfile(f'{foldername}\\{file_dir}') == True and ('').join(file_dir.split(".")[:-1]).lower() == file_name:
                    result.append('file found:'+' '+f'{foldername}\\{file_dir}')
                    return result
                elif os.path.isdir(f'{foldername}\\{file_dir}') == True and file_dir.lower()!= file_name:
                    search_file_in_dir(file_name, result, foldername=f'{foldername}\\{file_dir}')
                elif os.path.isdir(f'{foldername}\\{file_dir}') == True and file_dir.lower()== file_name:
                    result.append('folder found:' + ' '+f'{foldername}\\{file_dir}')
                    search_file_in_dir(file_name, result, foldername=f'{foldername}\\{file_dir}')
                else: continue
        except PermissionError: # if foldername does not exist
            pass



    def search_file_in_drive(list_drives, file_name): # the function for search of drives
        for name_drives in list_drives: # sort out list of drives.
            try:                        # if drives exists
                for foldername in tqdm(os.listdir(name_drives), desc='checked files and folders on disk ' + name_drives[0]): # sort out list of foldername drives.
                    if os.path.isfile(f'{name_drives}{foldername}')== True and ('').join(foldername.split(".")[:-1]).lower()== file_name:
                        result.append('file found:'+' '+f'{name_drives}{foldername}')
                    elif os.path.isdir(f'{name_drives}{foldername}')== True and foldername.lower()== file_name:
                        result.append('folder found:' + ' ' + f'{name_drives}{foldername}')
                        search_file_in_dir(file_name, result, foldername=f'{name_drives}{foldername}')
                    elif os.path.isdir(f'{name_drives}{foldername}')== True and foldername.lower()!= file_name:
                        search_file_in_dir(file_name, result, foldername=f'{name_drives}{foldername}')
                    else:
                        continue
            except FileNotFoundError:   # if drives does not exist
                continue

    def get_file_name(file_list=[]): # the function get name for search
        for file_name in file_list: # sort out list of name input .
            if file_name == '': continue
            else:
                termcolor.cprint('name checked : ' + file_name, 'yellow')
                search_file_in_drive(list_drives, file_name)
        os.system('cls') # clear terminal

    def get_not_find(result_start=set()): # get found names without address
        cor_result = [name.lower() for name in result]
        for element in result_start:
            for name in cor_result:
                if name.endswith(element) or ('').join(name.split(".")[:-1]).endswith(element):
                    result_end.add(element)
                else:
                    continue
        return result_end

    get_file_name(file_list)
    result_end = get_not_find(result_start)

    if result_start-result_end==set():
        result_not_find=['all names are found']
        termcolor.cprint('all names are found','green')
    elif result_start-result_end!=set() and result_start-result_end!=result_start:
        result_not_find=list(result_start-result_end)
        [termcolor.cprint('name not found: ' + res_not, 'red') for res_not in result_not_find]  # the output terminal of the not found names
    elif result_start-result_end!=set() and result_start-result_end==result_start:
        termcolor.cprint('all names are not found', 'red')
        result_not_find=['all names are not found']

    print(result) # get not found names without address

    [termcolor.cprint(res_like, 'green') for res_like in result]  # the output terminal of the found names
    if (file_list  == [] or file_list  == [' ']): termcolor.cprint('You have not entered a name for the search. The list is empty', 'red')


    def save_search(result=[]): # to save result data
        with open(f'result_search_{file_date_time}.csv',  'w') as resultFile:
            wr = csv.writer(resultFile, delimiter=';')
            for item in result:
                wr.writerow([item])
            for item in result_not_find:
                wr.writerow(['name not found: ']+[item])

    def quest_save(): # question to save result
        quest_s = input('Do you want to save result of search [yes/no]: ').lower()
        if quest_s.lower() == "yes": return True
        elif quest_s.lower() == "no": return False
        else: return None

    while True: # to save of result
        quest=quest_save()
        if quest == True:
            save_search(result)
            break
        elif quest == False: break
        else: termcolor.cprint('Invalid input. Please try again. Enter [yes/no]', 'red')



def soft_info_rus(): # функция информирования о программе
    termcolor.cprint('-------------------------------------------------------', 'blue')
    termcolor.cprint('ПРОГРАММА ДОЛЖНА БЫТЬ ЗАПУЩЕННА ОТ ИМЕНИ АДМИНИСТРАТОРА', 'yellow')
    termcolor.cprint('ИНАЧЕ ВОЗНИКНЕТ ОШИБКА И ПРИЛОЖЕНИЕ НЕ СМОЖЕТ РАБОТАТЬ', 'yellow')
    termcolor.cprint('-------------------------------------------------------', 'blue')
    rus_info=['Разработчик: Алексей Сурнов', 'search_file служит поиска файлов и папок:',
              '-1. Введите язык управления [rus / eng] и нажмите Enter',
              '-2. Введите названия искомых файлов и папок через запятую',
              '-2.1 Например: документ1, документ2, видео 1, System',
              '-2.2 Нажмите Enter',
              'Вы можете сохранить результаты поиска в отдельный файл',
              'Файл с данными в формате csv будет находится в той же папке что и программа',
              'Использовать в операционных системаx: ', '--Windows v.7,8,10 ']
    for info in rus_info:
        termcolor.cprint(info, 'green')
    termcolor.cprint('-------------------------------------------------------', 'blue')


def soft_info_eng(): # the function of informing about programm
    termcolor.cprint('-------------------------------------------------------', 'blue')
    termcolor.cprint('THE PROGRAM MUST BE RUN AS ADMINISTRATOR', 'yellow')
    termcolor.cprint('OTHERWISE AN ERROR WILL OCCUR AND THE APPLICATION WILL NOT BE ABLE TO WORK', 'yellow')
    termcolor.cprint('-------------------------------------------------------', 'blue')
    eng_info=['Developer: Alexey Surnov', 'search_file serves for look up files and folders',
              '-1. Input your language and press Enter',
              '-2. Input name of search files and folders using comma',
              '-2.1 For example: document1, document2, Videofile 1, System',
              '-2.2 Press Enter',
              'You can save search results in a separate file.',
              'The data file in csv format will be located in the same folder as the program',
              'Use in operating systems: ', '--Windows v.7,8,10']
    for info in eng_info:
        termcolor.cprint(info, 'green')
    termcolor.cprint('-------------------------------------------------------', 'blue')


def asking_rus(lang=0): # вопрос на русском языке: 'продолжить поиск'
    while True:
        question = input('Продолжить поиск [да / нет]: ').lower()
        if question == 'да' or question == 'нет':
            break
        else:
            termcolor.cprint('неправильный ввод ответа, повторите попытку', 'red')
            continue
    return question


def asking_eng(lang=0): # question in English: 'to continue the search'
    while True:
        question = input('Do you want to continue the search [yes / no]: ').lower()
        if question == 'yes' or question == 'no': break
        else:
            termcolor.cprint('invalid input, please try again', 'red')
            continue
    return question


def start_programm(lang=0):
    while True:
        if lang == 'rus':
            soft_info_rus()
            start_search_rus()
            question = asking_rus(lang)
            if question =='да': continue
            elif question =='нет': break
        elif lang == 'eng':
            soft_info_eng()
            start_search_eng()
            question = asking_eng(lang)
            if question == 'yes': continue
            elif question == 'no': break
        else:
            termcolor.cprint('invalid input, please try again / неправильный ввод языка, повторите попытку', 'red')
            lang = select_your_language()

if __name__ == "__main__":
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # имена дисков/name of drives
    list_drives = [f'{name_drives}:\\' for name_drives in letters]  # Using f'strings and list comprehension. Create a list of your drives / Использование f'строк  и генератора списка. Создаем спискок из дисков.
    lang = select_your_language()
    start_programm(lang)


