# -*- coding: utf8 -*-

##############
#Блок импорта#
##############

import sys
from datetime import datetime
import time
import os
from array import array

##############
#Блок функций#
##############

def load_log_file(log_file_path):                                                                           #Функция загрузки лог файла.
    log_line_date = []                                                                                      #Возвращает только те значения которые требуются 
    log_line_answ = array('i',[])                                                                           #для проведения анализа на наличие аварий
    with open(log_file_path) as log_file:
        log_file_lines = log_file.readlines()[1:]
        for line in log_file_lines:
            log_ln = line.split(' ')
            log_line_date.append(log_ln[0]+' '+log_ln[1])
            log_line_answ.append(int(log_ln[15]))
    return log_line_answ, log_line_date
    
def write_analize_file(output_dir, output_file_name, analize_str):                                          #Функция записи результатов анализа в файл
    with open(output_dir+output_file_name+'.analize','a') as analize_file:
        analize_file.write(analize_str)

def log_file_list(input_dir,output_dir):                                                                    #Функция возращает список файлов для анализа
    for line in os.listdir(output_dir):
        output_files_name.append(line.rstrip('.analize'))
    for line in os.listdir(input_dir):
        input_files_name.append(line.rstrip('.log'))
    input_files = os.listdir(input_dir)
    for i in range(len(input_files)): input_files[i] = input_dir+input_files[i]
    return input_files, input_files_name, output_files_name

def analize_log_file(sequence, answ_time, log_line_answ, log_line_date, output_dir, output_file_name):      #Функция анализа лог файла на наличие аварий
    seq = 0
    log_analize = []
    answ_time_med = 0
    answ_time_max = 0
    answ_time_evnt = 0
    for i in range(len(log_line_answ)):
        if log_line_answ[i] > answ_time:     
            if seq >= 1:
                seq = sequence
                log_analize.append(str(log_line_date[i])+' '+str(log_line_answ[i]))
            elif seq == 0: 
                seq = sequence 
                log_analize = []
                log_analize.append(str(log_line_date[i])+' '+str(log_line_answ[i]))   
            continue
        elif seq > 0: 
            seq -= 1
            log_analize.append(str(log_line_date[i])+' '+str(log_line_answ[i]))
            continue      
        elif seq == 0:
            if len(log_analize) > sequence*2: 
                answ_time_med = 0
                answ_time_evnt = 0
                answ_time_max = 0
                td = datetime.strptime(log_analize[len(log_analize)-sequence][0:19],'%Y-%m-%d %H:%M:%S')-datetime.strptime(log_analize[0][0:19],'%Y-%m-%d %H:%M:%S')
                for z in range(len(log_analize)): 
                    if int(log_analize[z][20:]) > answ_time: 
                        answ_time_evnt += 1
                        answ_time_med += int(log_analize[z][20:])
                    if int(log_analize[z][20:]) > answ_time_max: 
                        answ_time_max = int(log_analize[z][20:])
                analize_str = log_analize[0][0:19]+' Авария длительностью '+str(td)+'. Серия из '+str(len(log_analize)-sequence)+' событий.\n                    Среднее время ответа '+str(answ_time_med//answ_time_evnt)+' мс превысило пороговое значение '+str(answ_time)+' мс на '+str((answ_time_med//answ_time_evnt)-answ_time)+' мс\n                    Максимальное время ответа '+str(answ_time_max)+' мс превысило пороговое значение '+str(answ_time)+' мс на '+str(answ_time_max-answ_time)+' мс\n'
                write_analize_file(output_dir, output_file_name, analize_str)
                log_analize = []
            else: log_analize = []
            continue
        else: break

###################################
#Блок параметров работы программы#
###################################

input_dir = '/Input/'         #Путь до папки с логами подлежащими анализу
output_dir = '/Output/'       #Путь до папки куда складывать файлы с анализом
sequence = 3                                #Количество событий превышающих пороговое значение которое считать аварией
answ_time = 5000                            #Пороговое значение времени ответа сервера в миллисекундах которое считается критическим
work = 'True'                               #Условие выполнения программы
sleep = 60                                  #Частота проверки новых файлов для анализа в секундах

####################
#Основная программа#
####################

if __name__ == "__main__":
    while work:
        log_line_date = []
        log_line_answ = array('i',[])
        input_files = []
        input_files_name = []
        output_files_name = []
        input_files, input_files_name, output_files_name = log_file_list(input_dir,output_dir)
        for f in range(len(input_files_name)):
            if input_files_name[f] in output_files_name: continue
            else: 
                log_line_answ, log_line_date = load_log_file(input_files[f])
                analize_log_file(sequence, answ_time, log_line_answ, log_line_date, output_dir, input_files_name[f])
        time.sleep(sleep)
else: sys.exit()
