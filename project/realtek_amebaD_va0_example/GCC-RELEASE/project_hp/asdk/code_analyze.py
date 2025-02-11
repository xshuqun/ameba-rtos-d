#!/usr/bin/env python

from pickle import FALSE
import sys
import subprocess
import os
import re
import shutil
from typing import List


class SortStr:
    @staticmethod
    def __find_pha(str_olds: List[str]):
        '''
        filter the non-alpha in a string 
        :param str_olds: source string ：[--?—He teaches physics i（What is your father）]
        :return: filter string :[HeteachesphysicsiWhatisyourfather]
        '''
        str_news = []
        for str_old in str_olds:
            str_new = ''
            index = str_old.find('.o')
            for i in range(0, index):
                char_old = str_old[i]
                #if char_old.isalpha():
                str_new += char_old
            str_news.append(str_new)
        return str_news

    @staticmethod
    def __sort_str(str_olds: List[str], reverse: bool = False, target_index: int = 0):
        '''
        sort string list
        :param str_olds: source list
        :param reverse: False-ascending order, True-desending order
        :param target_index: sort begin index, default is 0
        :return:
        '''
        # transfer to upper
        str_olds_tem = []
        for i in str_olds:
            str_olds_tem.append(i.upper())
        # sort
        sort_index = []
        for i in str_olds_tem:
            sort_index.append({
                'key': str_olds_tem.index(i),
                'value': i[target_index]
            })
        reverse = reverse if reverse else False
        sort_index = sorted(sort_index, key=lambda e: e.__getitem__('value'), reverse=reverse)
        # 
        ture_index = []
        for i in sort_index:
            ture_index.append(i.get('key'))
        return ture_index

    @staticmethod
    def start(str_old, *args, **kwargs):
        '''
        :param str_old:
        :param args:
        :param kwargs: reverse=True 
        :return:
        '''
        str1 = SortStr.__find_pha(str_old)
        ture_index = SortStr.__sort_str(str1, *args, **kwargs)
        ture_str = []
        for i in ture_index:
            ture_str.append(str_old[i])
        return ture_str

flash_start = '__flash_text_start__ = .'
flash_end = '__flash_text_end__ = .'

sram_start = '__ram_text_start__ = .'
sram_end = '__ram_text_end__ = .'

text_filepath = 'image/text_image2_ns.map'

flash_base_addr = 0x60000000
sram_base_addr = 0x20000000  

sections = []
noload_sections = []

def obj_list_gen():
    if os.path.exists('obj_list.map'):
        os.remove('obj_list.map')
    f = open('obj_list.map', 'w')

    if os.path.exists('image/ram_size.txt'):
        parse_file = open('image/ram_size.txt', 'r')
    else:
        return
    all_lines = parse_file.readlines()

    for line in all_lines:
        item = list(filter(None, line.strip().split('\t')))
        num = len(item)


        line_strip = (line.strip())
        item_split_component = line_strip.split('component')

        found = line.find('component')
        if found > 0:
            print('component' + item_split_component[1], file=f)
        else:
            if num == 1:
                print(item[0], file=f)

    parse_file.close()
    f.close()
    return

def parse_img2_ld():
    global sections, noload_sections
    if os.path.exists('build/rlx8721d.ld'):
        parse_file = open('build/rlx8721d.ld', 'r')
    else:
        return
    all_lines = parse_file.readlines()

    Is_Noload = False
    sections_temp = {} 

    for line in all_lines:
        if line.find('NOLOAD') > 0 or line.find('COPY') > 0 or line.find('bluetooth_trace') > 0 or \
            line.find('.ram_image2.bss') > 0 or line.find('.ram_image2.nocache.data') > 0 or line.find('.ram_heap.data') > 0:
            Is_Noload = True
        
        if line.find('}') > 0:
            Is_Noload = False

        spos = line.find('*')
        epos1 = line.find('*)')
        epos2 = line.find(')')
        if spos>0 and epos1>0:
            newline = line[spos:epos1+2]
            if newline.find('SORT'):
                newline = newline.replace('SORT', 'SORT_BY_NAME')
            if sections_temp.get(newline) == None:
                sections_temp[newline] = dict(noload=False)
            sections_temp[newline] = Is_Noload
        elif spos>0 and epos2>0:
            newline = line[spos:epos2+1]
            if newline.find('SORT'):
                newline = newline.replace('SORT', 'SORT_BY_NAME')
            if sections_temp.get(newline) == None:
                sections_temp[newline] = dict(noload=False)
            sections_temp[newline] = Is_Noload

        
    for key,value in sections_temp.items():
        if value == True:
            noload_sections.append(key)  
        sections.append(key)
    #print(noload_sections)

def get_base_addr():
    global flash_base_addr, sram_base_addr

    text_file = open(text_filepath, 'r')
    text_all_lines = text_file.readlines()

    Is_Flash = False
    Is_Sram = False

    for line in text_all_lines:
        if line.find(flash_start) > 0:
            items = list(filter(None, line.strip().split(' ')))
            flash_base_addr = (int(items[0], 16) >> 24 ) << 24
            Is_Flash = True
        
        if line.find(sram_start) > 0:
            items = list(filter(None, line.strip().split(' ')))
            sram_base_addr = (int(items[0], 16) >> 24 ) << 24
            Is_Sram = True
        
        if Is_Flash and Is_Sram:
            break
    
    #print(hex(flash_base_addr), hex(sram_base_addr))

def sort_modules(strx):
    if strx == 'flash':
        srcfile = 'parse_sections_flash.map'
        dstfile = 'parse_sections_flash_n.map'
    elif strx == 'sram':
        srcfile = 'parse_sections_sram.map'
        dstfile = 'parse_sections_sram_n.map'
    elif strx == 'image':
        srcfile = 'parse_sections_image.map'
        dstfile = 'parse_sections_image_n.map'

    f = open(srcfile, 'r')
    all_lines = f.readlines()
    lib = []
    opensrc = []
    for line in all_lines:
        if line.find('.a') > 0:
            lib.append(line)
        else:
            opensrc.append(line)
    f.close()
    new_lib = []
    for line in lib:
        s = line.find('(')
        e = line.find(')')
        #libname = line[:s]
        filename = line[s+1:e]
        new_line = filename + ' ' + line
        new_lib.append(new_line)

    newopen = SortStr.start(opensrc)
    newlib = SortStr.start(new_lib)
    f = open(dstfile, 'w')
    for line in newlib:
        line = (line.strip())
        item = line.split(' ')
        if (item[1].find('wlan') > 0):
            if(item[1].find('phydm')) > 0:
                item[1] = 'phydm_'+ item[1]
            elif (item[1].find('halrf') > 0) :
                item[1] = 'halrf_'+ item[1]
        if srcfile == 'parse_sections_image.map':
            print(item[2] + ' ' + item[3] + ' ' + item[4] + ' ' + item[5] + ' ' + item[6] + ' ' + item[7] + ' ' 
                + item[8] + ' ' + item[9] + ' ' + item[10] + ' ' + item[11] + ' ' + item[12] + ' ' + item[13] + ' ' + item[14] + ' '+ item[1], file=f)
        else:
            print(item[2] + ' ' + item[3] + ' ' + item[4] + ' ' + item[5] + ' '+ item[1], file=f)
    for line in newopen:
        line = (line.strip())
        item = line.split(' ')
        if srcfile == 'parse_sections_image.map':
            print(item[1] + ' ' + item[2] + ' ' + item[3] + ' ' + item[4] + ' ' + item[5] + ' ' + item[6] + ' ' 
                + item[7] + ' ' + item[8] + ' ' + item[9] + ' ' + item[10] + ' ' + item[11] + ' ' + item[12] + ' ' + item[13] + ' '+ item[0], file=f)
        else:
            print(item[1] + ' ' + item[2] + ' ' + item[3] + ' ' + item[4] + ' '+ item[0], file=f)
    f.close()


def parse_sections():
    if os.path.exists('parse_sections_temp.map'):
        os.remove('parse_sections_temp.map')

    if os.path.exists('parse_sections_flash.map'):
        os.remove('parse_sections_flash.map')

    if os.path.exists('parse_sections_sram.map'):
        os.remove('parse_sections_sram.map')

    if os.path.exists('parse_sections_image.map'):
        os.remove('parse_sections_image.map')

    flashf = open('parse_sections_flash.map', 'w')
    sramf = open('parse_sections_sram.map', 'w')
    imagef = open('parse_sections_image.map', 'w')

    temp_file = open('parse_sections_temp.map', 'w')
    text_file = open(text_filepath, 'r')
    #text_file = open('temp_text.map', 'r')
    
    text_all_lines = text_file.readlines()

    modules_flash = {}
    modules_sram = {}

    IF_Write = False
    last_line = ''
    find_sections = []
    fill_size = 0
    for section in sections:
        for text_line in text_all_lines:
            if text_line.find(section) > 0:
                find_sections.append(section)
                IF_Write = True

            #if IF_Write and (text_line.startswith(' *(') or text_line.startswith(' *'))  and text_line.find(section) < 0 and text_line.find('*fill*') < 0:
            if IF_Write and (text_line.strip() in sections) and text_line.find(section) < 0:
                IF_Write = False
                #if(text_line.find('*fill*') > 0):
                #    print(text_line)
                break
                    
            if IF_Write:
                
                items = list(filter(None, text_line.strip().split(' ')))
                num = len(items)
                if num == 3:
                    if items[0] == '*fill*':
                        fill_size += int(items[2],16)
                    if (items[0].find('0x') == 0 and (items[-1].endswith('.o') or items[-1].endswith('.o)'))):
                        #modules[items[2]] = dict(rodata='',data='',text='',bss='')
                        if ((int(items[0],16) & flash_base_addr) == 0) and ((int(items[0],16) & sram_base_addr) == 0):
                            #print(text_line)
                            continue
                        items[2] = os.path.split(items[2])[1]
                        if ((int(items[0],16) & flash_base_addr) == flash_base_addr):
                            if modules_flash.get(items[2]) == None:
                                #modules[items[2]] = dict.fromkeys(['text', 'rodata', 'data', 'bss'])
                                modules_flash[items[2]] = dict(rodata=0,data=0,text=0,bss=0,noload_data=0,noload_bss=0)
                            if section in noload_sections:
                                if section.find('data') > 0:
                                    modules_flash[items[2]]['noload_data'] += int(items[1],16)
                                elif section.find('bss') > 0:
                                    modules_flash[items[2]]['noload_bss'] += int(items[1],16)
                            else:

                                if section.find('rodata') > 0 and section.find('text') > 0:
                                    if(last_line.find('rodata') > 0) :
                                        modules_flash[items[2]]['rodata']  += int(items[1],16)
                                    elif(last_line.find('text') > 0) :
                                        modules_flash[items[2]]['text'] += int(items[1],16)
                                elif section.find('rodata') > 0:
                                    modules_flash[items[2]]['rodata']  += int(items[1],16)
                                elif section.find('data') > 0:
                                    modules_flash[items[2]]['rodata'] += int(items[1],16)
                                elif section.find('text') > 0:
                                    modules_flash[items[2]]['text'] += int(items[1],16)
                                elif section.find('bss') > 0:
                                    modules_flash[items[2]]['bss'] += int(items[1],16)
                        elif ((int(items[0],16) & sram_base_addr) == sram_base_addr):
                            if modules_sram.get(items[2]) == None:
                                #modules[items[2]] = dict.fromkeys(['text', 'rodata', 'data', 'bss'])
                                modules_sram[items[2]] = dict(rodata=0,data=0,text=0,bss=0,noload_data=0,noload_bss=0)
                            if section in noload_sections:
                                if section.find('data') > 0:
                                    modules_sram[items[2]]['noload_data'] += int(items[1],16)
                                elif section.find('bss') > 0:
                                    modules_sram[items[2]]['noload_bss'] += int(items[1],16)
                            else:
                                if section.find('rodata') > 0 and section.find('text') > 0:
                                    #print(section+' '+text_line)
                                    if(last_line.find('rodata') > 0) :
                                        modules_sram[items[2]]['rodata']  += int(items[1],16)
                                    elif(last_line.find('text') > 0) :
                                        modules_sram[items[2]]['text'] += int(items[1],16)
                                elif section.find('rodata') > 0:
                                    modules_sram[items[2]]['rodata']  += int(items[1],16)
                                elif section.find('data') > 0:
                                    modules_sram[items[2]]['data'] += int(items[1],16)
                                elif section.find('text') > 0:
                                    modules_sram[items[2]]['text'] += int(items[1],16)
                                elif section.find('bss') > 0:
                                    modules_sram[items[2]]['bss'] += int(items[1],16)
                        temp_file.write(text_line)
                if num == 4:
                    if (items[1].find('0x') == 0 and (items[-1].endswith('.o') or items[-1].endswith('.o)'))):
                        #modules[items[2]] = dict(rodata='',data='',text='',bss='')
                        if ((int(items[1],16) & flash_base_addr) == 0) and ((int(items[1],16) & sram_base_addr) == 0):
                            #print(text_line)
                            continue
                        items[3] = os.path.split(items[3])[1]
                        if ((int(items[1],16) & flash_base_addr) == flash_base_addr):
                            if modules_flash.get(items[3]) == None:
                                #modules[items[2]] = dict.fromkeys(['text', 'rodata', 'data', 'bss'])
                                modules_flash[items[3]] = dict(rodata=0,data=0,text=0,bss=0,noload_data=0,noload_bss=0)
                            if section in noload_sections:
                                if section.find('data') > 0:
                                    modules_flash[items[3]]['noload_data'] += int(items[2],16)
                                elif section.find('bss') > 0:
                                    modules_flash[items[3]]['noload_bss'] += int(items[2],16)
                            else:
                                if section.find('rodata') > 0 and section.find('text') > 0:
                                    #print('='+text_line)
                                    if(last_line.find('rodata') > 0) :
                                        modules_flash[items[3]]['rodata']  += int(items[2],16)
                                    elif(last_line.find('text') > 0) :
                                        modules_flash[items[3]]['text'] += int(items[2],16)
                                elif section.find('rodata') > 0:
                                    modules_flash[items[3]]['rodata']  += int(items[2],16)
                                elif section.find('data') > 0:
                                    modules_flash[items[3]]['rodata'] += int(items[2],16)
                                elif section.find('text') > 0:
                                    modules_flash[items[3]]['text'] += int(items[2],16)
                                elif section.find('bss') > 0:
                                    modules_flash[items[3]]['bss'] += int(items[2],16)
                        elif ((int(items[1],16) & sram_base_addr) == sram_base_addr):
                            if modules_sram.get(items[3]) == None:
                                #modules[items[2]] = dict.fromkeys(['text', 'rodata', 'data', 'bss'])
                                modules_sram[items[3]] = dict(rodata=0,data=0,text=0,bss=0,noload_data=0,noload_bss=0)
                            if section in noload_sections:
                                if section.find('data') > 0:
                                    modules_sram[items[3]]['noload_data'] += int(items[2],16)
                                elif section.find('bss') > 0:
                                    modules_sram[items[3]]['noload_bss'] += int(items[2],16)
                            else:
                                if section.find('rodata') > 0 and section.find('text') > 0:
                                    if(last_line.find('rodata') > 0) :
                                        modules_sram[items[3]]['rodata']  += int(items[2],16)
                                    elif(last_line.find('text') > 0) :
                                        modules_sram[items[3]]['text'] += int(items[2],16)
                                elif section.find('rodata') > 0:
                                    modules_sram[items[3]]['rodata']  += int(items[2],16)
                                elif section.find('data') > 0:
                                    modules_sram[items[3]]['data'] += int(items[2],16)
                                elif section.find('text') > 0:
                                    modules_sram[items[3]]['text'] += int(items[2],16)
                                elif section.find('bss') > 0:
                                    modules_sram[items[3]]['bss'] += int(items[2],16)
                        temp_file.write(text_line)

                last_line = text_line
    #print(fill_size)
    for key,value in modules_flash.items():
        print(key + ' ' +  hex(value['text'])+ ' ' + hex(value['rodata']) + ' ' + hex(value['data']) + ' ' + hex(value['bss']), file=flashf)

    for key,value in modules_sram.items():
        print(key + ' ' +  hex(value['text'])+ ' ' + hex(value['rodata']) + ' ' + hex(value['data']) + ' ' + hex(value['bss']), file=sramf)

    # merge flash(flash) and sram
    for key,value in modules_flash.items():
        item = modules_sram.pop(key, None)
        if item == None:
            item = dict(rodata=0,data=0,text=0,bss=0,noload_data=0,noload_bss=0)
        flash_total_size = value['text'] + value['rodata']
        sram_total_size = item['text'] + item['rodata'] + item['data'] + item['bss']
        noload_total_size = item['noload_data'] + item['noload_bss'] + value['noload_data'] + value['noload_bss']
        image_total_size = flash_total_size + sram_total_size
        ram_total_size = sram_total_size + noload_total_size
        print(key + ' ' +  hex(value['text'])+ ' ' + hex(value['rodata']) + ' ' + hex(item['text'])+ ' ' + hex(item['rodata']) + ' '
                         + hex(item['data']) + ' ' + hex(item['bss']) + ' ' + hex(item['noload_data']) + ' ' + hex(item['noload_bss']) + ' ' 
                         + hex(value['noload_data']) + ' ' + hex(value['noload_bss']) + ' ' 
                         + hex(image_total_size) + ' ' + hex(flash_total_size) + ' ' + hex(ram_total_size), file=imagef)
    # files in sram but not in flash(flash)
    for key,item in modules_sram.items():
        value['text'] = 0
        value['rodata'] = 0
        value['noload_data'] = 0
        value['noload_bss'] = 0
        flash_total_size = value['text'] + value['rodata']
        sram_total_size = item['text'] + item['rodata'] + item['data'] + item['bss']
        noload_total_size = item['noload_data'] + item['noload_bss'] + value['noload_data'] + value['noload_bss']
        image_total_size = flash_total_size + sram_total_size
        ram_total_size = sram_total_size + noload_total_size
        print(key + ' ' +  hex(value['text'])+ ' ' + hex(value['rodata']) + ' ' + hex(item['text'])+ ' ' + hex(item['rodata']) + ' ' 
                        + hex(item['data']) + ' ' + hex(item['bss']) + ' ' + hex(item['noload_data']) + ' ' + hex(item['noload_bss']) + ' '
                        + hex(value['noload_data']) + ' ' + hex(value['noload_bss']) + ' ' 
                        + hex(image_total_size) + ' ' + hex(flash_total_size) + ' ' + hex(ram_total_size), file=imagef) 
    flashf.close()
    sramf.close()
    imagef.close()
    temp_file.close()


def merge_size_and_objs_2(strx):
    if (strx == 'flash'):
        des_file = 'code_size_flash.map'
        f = open('parse_sections_flash_n.map', 'r')
        sepsize = 25
    elif(strx == 'sram'):
        des_file = 'code_size_ram.map'
        f = open('parse_sections_sram_n.map', 'r')
        sepsize = 25
    elif strx == 'image':
        des_file = 'code_size_image.map'
        f = open('parse_sections_image_n.map', 'r')
        sepsize = 90

    if os.path.exists(des_file):
        os.remove(des_file)
    file_result = open(des_file, 'w')
    if des_file == 'code_size_image.map':
        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'
                .format('image_total', 'flash_total', 'sram_total', 'flash_text', 'flash_rodata','sram_text', 'sram_rodata', 'sram_data', 'sram_bss', 
                        'data(sram noload)', 'bss(sram noload)', 'module'), file=file_result)
    else:
        print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format('text', 'rodata', 'data', 'bss', 'module'), file=file_result)

    
    all_lines = f.readlines()
    total_size = 0
    total_section_size = dict(image_total=0,flash_total=0,sram_total=0,rodata=0,data=0,text=0,bss=0,data_sram=0,bss_sram=0,noload_data_sram=0,noload_bss_sram=0)
    #
    lable = []
    #
    for line in all_lines:
        #
        line_strip = (line.strip())
        item_split_bank = line_strip.split(' ')
        if des_file == 'code_size_image.map':
            found_a = item_split_bank[13].find('.a')
            filestr = item_split_bank[13]
        else:
            found_a = item_split_bank[4].find('.a')
            filestr = item_split_bank[4]

        if found_a > 0:
            item_split_bank_a = filestr.split('.a')
            if item_split_bank_a[0] not in lable:
                lable.append(item_split_bank_a[0])
    lable.sort(key=lambda x: x[-1], reverse=False)
    for i in range(len(lable)):
        print('{0} {1} {2} {3}{4}'.format('='*sepsize, lable[i],'start','='*(30-len(lable[i])-len('start')), '='*sepsize), file=file_result)
        section_size = dict(image_total=0,flash_total=0,sram_total=0,rodata=0,data=0,text=0,bss=0,data_sram=0,bss_sram=0,noload_data_sram=0,noload_bss_sram=0)
        for line in all_lines:
            line_strip = (line.strip())
            item_split_bank = line_strip.split(' ')

            found = line.find(lable[i])

            if(lable[i] == 'lib_wlan' and ((line.find('phydm_') >= 0) or line.find('halrf_') >= 0)):
                continue

            if (found > 0):
                section_size['text'] += int(item_split_bank[0], 16)
                section_size['rodata'] += int(item_split_bank[1], 16)
                section_size['data'] += int(item_split_bank[2], 16)
                section_size['bss'] += int(item_split_bank[3], 16)

                if des_file == 'code_size_image.map':            
                    if(lable[i].find('phydm_') == 0):
                        item_split_bank[13] = item_split_bank[13][len('phydm_'):]  
                    elif(lable[i].find('halrf_') == 0):
                        item_split_bank[13] = item_split_bank[13][len('halrf_'):]  
                    section_size['data_sram'] += int(item_split_bank[4], 16)
                    section_size['bss_sram'] += int(item_split_bank[5], 16)
                    section_size['noload_data_sram'] += int(item_split_bank[6], 16)
                    section_size['noload_bss_sram'] += int(item_split_bank[7], 16)
                    section_size['image_total'] += int(item_split_bank[10], 16)
                    section_size['flash_total'] += int(item_split_bank[11], 16)
                    section_size['sram_total'] += int(item_split_bank[12], 16)

                    print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}'.format(
                        str(int(item_split_bank[10], 16)),
                        str(int(item_split_bank[11], 16)),
                        str(int(item_split_bank[12], 16)),
                        str(int(item_split_bank[0], 16)), 
                        str(int(item_split_bank[1], 16)), 
                        str(int(item_split_bank[2], 16)),
                        str(int(item_split_bank[3], 16)),
                        str(int(item_split_bank[4], 16)),
                        str(int(item_split_bank[5], 16)),
                        str(int(item_split_bank[6], 16)),
                        str(int(item_split_bank[7], 16)),
                                item_split_bank[13]), file=file_result)
                else:
                    if(lable[i].find('phydm_') == 0):
                        item_split_bank[4] = item_split_bank[4][len('phydm_'):]  
                    elif(lable[i].find('halrf_') == 0):
                        item_split_bank[4] = item_split_bank[4][len('halrf_'):]  
                    print('{:<13}{:<13}{:<13}{:<13}{:<13}'.format(
                        str(int(item_split_bank[0], 16)), 
                        str(int(item_split_bank[1], 16)), 
                        str(int(item_split_bank[2], 16)),
                        str(int(item_split_bank[3], 16)),
                        item_split_bank[4]), file=file_result)

        for key,value in total_section_size.items():
            total_section_size[key] += section_size[key]
        print('{0} {1} {2} {3}{4}'.format('-'*sepsize, lable[i],'end','-'*(30-len(lable[i])-len('end')), '-'*sepsize), file=file_result)
        #print('\n' + 'total:', file=file_result)

        if des_file == 'code_size_image.map':
            print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'
                .format('image_total', 'flash_total', 'sram_total', 'flash_text', 'flash_rodata','sram_text', 'sram_rodata', 'sram_data', 'sram_bss', 
                        'data(sram noload)', 'bss(sram noload)', 'module'), file=file_result)
        else:
            print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format('text', 'rodata', 'data', 'bss', 'module'), file=file_result)
        
        if des_file == 'code_size_image.map':
            print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'.format(
                str(section_size['image_total']), 
                str(section_size['flash_total']), 
                str(section_size['sram_total']),
                str(section_size['text']), 
                str(section_size['rodata']), 
                str(section_size['data']),
                str(section_size['bss']),
                str(section_size['data_sram']),
                str(section_size['bss_sram']),
                str(section_size['noload_data_sram']),
                str(section_size['noload_bss_sram']),
                '(TOTALS)'), file=file_result)
            total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss'] + section_size['data_sram'] + section_size['bss_sram']
        else:
            print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format(
                str(section_size['text']), 
                str(section_size['rodata']), 
                str(section_size['data']),
                str(section_size['bss_sram']),'(TOTALS)'), file=file_result)
            total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss']
        print('Module {} size:'.format(lable[i]), file=file_result)        
        print(str(hex(total_size)) + '\t\t\t' + str(total_size) + '\n', file=file_result)

    if os.path.exists('sort_temp_file.map'):
        os.remove('sort_temp_file.map')
    file_sort_temp = open('sort_temp_file.map', 'w')

    for line in all_lines:
        line_strip = (line.strip())
        item_split_bank = line_strip.split(' ')

        found = line.find('.a')

        if (found < 0):
            if des_file == 'code_size_image.map':
                print(item_split_bank[0] + ' ' + 
                item_split_bank[1] + ' ' + 
                item_split_bank[2] + ' ' + 
                item_split_bank[3] + ' ' + 
                item_split_bank[4] + ' ' + 
                item_split_bank[5] + ' ' + 
                item_split_bank[6] + ' ' + 
                item_split_bank[7] + ' ' + 
                item_split_bank[8] + ' ' + 
                item_split_bank[9] + ' ' + 
                item_split_bank[10] + ' ' + 
                item_split_bank[11] + ' ' + 
                item_split_bank[12] + ' ' + 
                item_split_bank[13], file=file_sort_temp)
            else:
                print(item_split_bank[0] + ' ' + 
                item_split_bank[1] + ' ' + 
                item_split_bank[2] + ' ' + 
                item_split_bank[3] + ' ' + 
                item_split_bank[4], file=file_sort_temp)

    file_sort_temp.close()

    sort_lable_ipc = ['ipc', 'ipc_', 'inic_ipc', 'ipc']
    sort_lable_fwlib = ['fwlib', 'rtl8721d_', 'rtl8721dhp_']

    sort_lable_wifi = ['wifi', 'wifi_', 'lwip_netconf', 'wifi_interactive_mode', 'atcmd_sys', 'atcmd_wifi', 'tcptest', 'wlan_', 'rtw_']
    sort_label_utils = ['utils', 'iperf', 'cJSON', 'units', 'timer.', 'ping_']
    sort_lable_per = ['peripheral', 'platform', 'main', 'example_entry', '_api.']
    sort_lable_shell = ['shell', 'shell', 'log_', 'monitor', 'low_level_io', 'rtl_trace']
    sort_lable_os = ['os', 'croutine', 'event_groups', 'list', 'queue', 'tasks', 'timers', 'heap_5', 'port', 'freertos_', 'freertos',
                     'osdep_', 'device_lock', 'timer_service']
    sort_label_bt = ['bt','bt_', 'hci_', 'coex', 'ble_', '_bas', 'dis', 'gls', 'hids', 'hrs', 'ias', 'ftl', '_bt']

    sort_label_lwip = ['lwip', 'tcp', 'ip', 'udp', 'igmp', 'net', 'pbuf', 'icmp', 'eth', 'dhcp', 'dns', 'api_lib', 'api_msg', 'mem', 
                    'dscp', 'timeouts', 'sys_arch', 'sockets', 'raw', 'def', 'err', 'init']

    sort_labels = [sort_lable_ipc, sort_lable_wifi, sort_label_utils, 
                    sort_lable_shell, sort_lable_os, sort_lable_fwlib, sort_label_bt, sort_label_lwip, sort_lable_per]

    file_sort_temp_r = open('sort_temp_file.map', 'r')
    all_lines_sort = file_sort_temp_r.readlines()

    array_flag = [0 for i in range(len(all_lines_sort))]

    
    for label in sort_labels:
        print('{0} {1} {2} {3}{4}'.format('='*sepsize, label[0],'start','='*(30-len(label[0])-len('start')), '='*sepsize), file=file_result)
        section_size = dict(image_total=0,flash_total=0,sram_total=0,rodata=0,data=0,text=0,bss=0,data_sram=0,bss_sram=0,noload_data_sram=0,noload_bss_sram=0)
        temp_flag = 0
        for all_lines_sort_t in all_lines_sort:
            item = list(filter(None, all_lines_sort_t.strip().split(' ')))
            line_strip = (all_lines_sort_t.strip())
            item_split_bank = line_strip.split(' ')
            temp_flag = 0
            for idxn in range(1,len(label)):
                if des_file == 'code_size_image.map':
                    found = item_split_bank[13].find(label[idxn])
                else:
                    found = item_split_bank[4].find(label[idxn])
                if found >= 0:
                    temp_flag = 1
                    break
            if (temp_flag == 1):
                if (array_flag[all_lines_sort.index(all_lines_sort_t)] == 0):
                    section_size['text'] += int(item_split_bank[0], 16)
                    section_size['rodata'] += int(item_split_bank[1], 16)
                    section_size['data'] += int(item_split_bank[2], 16)
                    section_size['bss'] += int(item_split_bank[3], 16)

                    if des_file == 'code_size_image.map':              
                        section_size['data_sram'] += int(item_split_bank[4], 16)
                        section_size['bss_sram'] += int(item_split_bank[5], 16)
                        section_size['noload_data_sram'] += int(item_split_bank[6], 16)
                        section_size['noload_bss_sram'] += int(item_split_bank[7], 16)
                        section_size['image_total'] += int(item_split_bank[10], 16)
                        section_size['flash_total'] += int(item_split_bank[11], 16)
                        section_size['sram_total'] += int(item_split_bank[12], 16)

                        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}'.format(
                            str(int(item_split_bank[10], 16)),
                            str(int(item_split_bank[11], 16)),
                            str(int(item_split_bank[12], 16)),
                            str(int(item_split_bank[0], 16)), 
                            str(int(item_split_bank[1], 16)), 
                            str(int(item_split_bank[2], 16)),
                            str(int(item_split_bank[3], 16)),
                            str(int(item_split_bank[4], 16)),
                            str(int(item_split_bank[5], 16)),
                            str(int(item_split_bank[6], 16)),
                            str(int(item_split_bank[7], 16)),
                                    item_split_bank[13]), file=file_result)
                    else:
                        print('{:<13}{:<13}{:<13}{:<13}{:<13}'.format(
                            str(int(item_split_bank[0], 16)), 
                            str(int(item_split_bank[1], 16)), 
                            str(int(item_split_bank[2], 16)),
                            str(int(item_split_bank[3], 16)),
                            item_split_bank[4]), file=file_result)
                    array_flag[all_lines_sort.index(all_lines_sort_t)] = 1
        for key,value in total_section_size.items():
            total_section_size[key] += section_size[key]
        print('{0} {1} {2} {3}{4}'.format('-'*sepsize, label[0],'end','-'*(30-len(label[0])-len('end')), '-'*sepsize), file=file_result)
        #print('\n' + 'total:', file=file_result)

        if des_file == 'code_size_image.map':
            print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'
                .format('image_total', 'flash_total', 'sram_total', 'flash_text', 'flash_rodata','sram_text', 'sram_rodata', 'sram_data', 'sram_bss', 
                        'data(sram noload)', 'bss(sram noload)', 'module'), file=file_result)
        else:
            print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format('text', 'rodata', 'data', 'bss', 'module'), file=file_result)
        if des_file == 'code_size_image.map':
            print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'.format(
                str(section_size['image_total']), 
                str(section_size['flash_total']), 
                str(section_size['sram_total']),
                str(section_size['text']), 
                str(section_size['rodata']), 
                str(section_size['data']),
                str(section_size['bss']),
                str(section_size['data_sram']),
                str(section_size['bss_sram']),
                str(section_size['noload_data_sram']),
                str(section_size['noload_bss_sram']),
                '(TOTALS)'), file=file_result)
            total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss'] + section_size['data_sram'] + section_size['bss_sram']
        else:
            print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format(
                str(section_size['text']), 
                str(section_size['rodata']), 
                str(section_size['data']),
                str(section_size['bss_sram']),'(TOTALS)'), file=file_result)
            total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss']
        print('Module {} size:'.format(label[0]), file=file_result)
        
        print(str(hex(total_size)) + '\t\t\t' + str(total_size) + '\n', file=file_result)
    file_sort_temp_r.close()

    print('{0} {1} {2} {3}{4}'.format('='*sepsize,'others','start','='*(30-len('others')-len('start')), '='*sepsize), file=file_result)

    file_sort_temp_r = open('sort_temp_file.map', 'r')
    all_lines_sort = file_sort_temp_r.readlines()
    section_size = dict(image_total=0,flash_total=0,sram_total=0,rodata=0,data=0,text=0,bss=0,data_sram=0,bss_sram=0,noload_data_sram=0,noload_bss_sram=0)
    for all_lines_sort_t in all_lines_sort:
        line_strip = (all_lines_sort_t.strip())
        item_split_bank = line_strip.split(' ')

        temp_flag = 0
        for label in sort_labels:
            for idxn in range(1,len(label)):
                if des_file == 'code_size_image.map':
                    found = item_split_bank[13].find(label[idxn])
                else:
                    found = item_split_bank[4].find(label[idxn])
                if found >= 0:
                    temp_flag = 1
                    break
            if(temp_flag == 1):
                break

        if (temp_flag == 0):
            if (array_flag[all_lines_sort.index(all_lines_sort_t)] == 0):
                section_size['text'] += int(item_split_bank[0], 16)
                section_size['rodata'] += int(item_split_bank[1], 16)
                section_size['data'] += int(item_split_bank[2], 16)
                section_size['bss'] += int(item_split_bank[3], 16)

                if des_file == 'code_size_image.map':              
                    section_size['data_sram'] += int(item_split_bank[4], 16)
                    section_size['bss_sram'] += int(item_split_bank[5], 16)
                    section_size['noload_data_sram'] += int(item_split_bank[6], 16)
                    section_size['noload_bss_sram'] += int(item_split_bank[7], 16)
                    section_size['image_total'] += int(item_split_bank[10], 16)
                    section_size['flash_total'] += int(item_split_bank[11], 16)
                    section_size['sram_total'] += int(item_split_bank[12], 16)

                    print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}'.format(
                        str(int(item_split_bank[10], 16)),
                        str(int(item_split_bank[11], 16)),
                        str(int(item_split_bank[12], 16)),
                        str(int(item_split_bank[0], 16)), 
                        str(int(item_split_bank[1], 16)), 
                        str(int(item_split_bank[2], 16)),
                        str(int(item_split_bank[3], 16)),
                        str(int(item_split_bank[4], 16)),
                        str(int(item_split_bank[5], 16)),
                        str(int(item_split_bank[6], 16)),
                        str(int(item_split_bank[7], 16)),
                                item_split_bank[13]), file=file_result)
                else:
                    print('{:<13}{:<13}{:<13}{:<13}{:<13}'.format(
                        str(int(item_split_bank[0], 16)), 
                        str(int(item_split_bank[1], 16)), 
                        str(int(item_split_bank[2], 16)),
                        str(int(item_split_bank[3], 16)),
                        item_split_bank[4]), file=file_result)
                array_flag[all_lines_sort.index(all_lines_sort_t)] = 1

    for key,value in total_section_size.items():
        total_section_size[key] += section_size[key]
    print('{0} {1} {2} {3}{4}'.format('-'*sepsize, 'others','end','-'*(30-len('others')-len('end')), '-'*sepsize), file=file_result)

    if des_file == 'code_size_image.map':
        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'
                .format('image_total', 'flash_total', 'sram_total', 'flash_text', 'flash_rodata','sram_text', 'sram_rodata', 'sram_data', 'sram_bss', 
                        'data(sram noload)', 'bss(sram noload)', 'module'), file=file_result)
    else:
        print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format('text', 'rodata', 'data', 'bss', 'module'), file=file_result)

    if des_file == 'code_size_image.map':
        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'.format(
            str(section_size['image_total']), 
            str(section_size['flash_total']), 
            str(section_size['sram_total']),
            str(section_size['text']), 
            str(section_size['rodata']), 
            str(section_size['data']),
            str(section_size['bss']),
            str(section_size['data_sram']),
            str(section_size['bss_sram']),
            str(section_size['noload_data_sram']),
            str(section_size['noload_bss_sram']),
            '(TOTALS)'), file=file_result)
        total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss'] + section_size['data_sram'] + section_size['bss_sram']
    else:
        print('{:<13}{:<13}{:<13}{:<13}{:<13}\n'.format(
            str(section_size['text']), 
            str(section_size['rodata']), 
            str(section_size['data']),
            str(section_size['bss_sram']),'(TOTALS)'), file=file_result)
        total_size = section_size['text'] + section_size['rodata'] + section_size['data'] + section_size['bss']
    print('Module {} size:'.format('others'), file=file_result)
    
    print(str(hex(total_size)) + '\t\t\t' + str(total_size) + '\n', file=file_result)
    print('{0}'.format('='*(30 + sepsize * 2)), file=file_result)

    file_sort_temp_r.close()
    if des_file == 'code_size_image.map':
        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}\n'
                .format('image_total', 'flash_total', 'sram_total', 'flash_text', 'flash_rodata','sram_text', 'sram_rodata', 'sram_data', 'sram_bss', 
                        'data(sram noload)', 'bss(sram noload)', 'module'), file=file_result)
        print('{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}{:<20}{:<20}{:<13}'.format(
            str(total_section_size['image_total']), 
            str(total_section_size['flash_total']), 
            str(total_section_size['sram_total']),
            str(total_section_size['text']), 
            str(total_section_size['rodata']), 
            str(total_section_size['data']),
            str(total_section_size['bss']),
            str(total_section_size['data_sram']),
            str(total_section_size['bss_sram']),
            str(total_section_size['noload_data_sram']),
            str(total_section_size['noload_bss_sram']),
            '(TOTALS)'), file=file_result)
        total_size = total_section_size['text'] + total_section_size['rodata'] + total_section_size['data'] + total_section_size['bss'] + total_section_size['data_sram'] + total_section_size['bss_sram']
    else:
        print('{:<13}{:<13}{:<13}{:<13}{:<13}'.format('text', 'rodata', 'data', 'bss', 'module'), file=file_result)
        print('{:<13}{:<13}{:<13}{:<13}{:<13}'.format(
                str(total_section_size['text']), 
                str(total_section_size['rodata']), 
                str(total_section_size['data']),
                str(total_section_size['bss']),
                '(TOTALS)'), file=file_result)
        total_size = total_section_size['text'] + total_section_size['rodata'] + total_section_size['data'] + total_section_size['bss']
    print('\n' + 'Image size:', file=file_result)
    print(str(hex(total_size)) + '\t\t\t' + str(total_size) + '\n', file=file_result)

    file_result.close()
    f.close()
    return

if os.path.exists(text_filepath):
    get_base_addr()
    parse_img2_ld()
    parse_sections()
    obj_list_gen()
    str_list = ['flash', 'sram', 'image']
    for strr in str_list:
        sort_modules(strr)
        merge_size_and_objs_2(strr)
    
    # remove temp files
    os.remove('obj_list.map')
    os.remove('parse_sections_temp.map')
    os.remove('parse_sections_flash.map')
    os.remove('parse_sections_sram.map')
    os.remove('parse_sections_image.map')
    os.remove('parse_sections_flash_n.map')
    os.remove('parse_sections_sram_n.map')
    os.remove('parse_sections_image_n.map')
    os.remove('sort_temp_file.map')

    
    if os.path.exists('image/code_size_ram.map'):
        os.remove('image/code_size_ram.map')
    if os.path.exists('image/code_size_flash.map'):
        os.remove('image/code_size_flash.map')
    if os.path.exists('image/code_size_image.map'):
        os.remove('image/code_size_image.map')
    shutil.move('code_size_ram.map', 'image')
    shutil.move('code_size_flash.map', 'image')
    shutil.move('code_size_image.map', 'image')
