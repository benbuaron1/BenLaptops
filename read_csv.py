import csv
import os
import random
import re

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',"LaptopStore.settings")
django.setup()

from lapotp_app.models import *



def get_resolution(res_text):
    resolution_match = re.search(r".*(\d{4})x(\d{3,5}).*", res_text)
    w, h = None, None
    if resolution_match:
        w = resolution_match.group(1)
        h = resolution_match.group(2)
    else:
        print(f"No resolution for {res_text}")
    return w, h

def get_ram_memory(ram_text):
    ram_memory_match = re.search(r"\d{1,2}",ram_text)
    ram = None
    if ram_memory_match:
        ram = int(ram_memory_match.group())
    else:
        print(f"No ram for {ram_text}")
    return ram

def get_memory(mem_text):
    mem_num = re.search(r"(\d{3}|\d{2}|\d{1})",mem_text)
    mem_kind = re.search(r"\D{1,2}",mem_text)
    mem_type = re.search(r"\s{1}\D+",mem_text)
    tup = None
    if mem_type and mem_num and mem_kind:
        tup = (int(mem_num.group()), mem_kind.group(), mem_type.group())
    else:
        print(f"No memory for {mem_text}")
    return tup

def get_manufactorer(manu):
    existing_manu = Manufacurer.objects.all()
    found_manu = None
    for m in existing_manu:
        if m.name == manu:
            found_manu = m
            return found_manu
    if not found_manu:
        manufactorer = Manufacurer(name=manu)
        manufactorer.save()
        return manufactorer

    # if manu in Manufacurer.objects.all():
    #     return manu
    # else:
    #     manu = Manufacurer(name=manu)
    #     manu.save()
    #     return manu


def load_laptops():
    with open('laptops.csv','rt',encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if '+' in row[8]:
                memory_field = row[8].split(sep='+  ')
                mem1 = get_memory(memory_field[0])
                mem2 = get_memory(memory_field[1])
            else:
                mem1 = get_memory(row[8])
                mem2 = ('None','None','None')
            try:
                laptop = Laptop(
                    manufacturer=get_manufactorer(row[1]),
                    product= row[2],
                    type=row[3],
                    inches=row[4],
                    screen_width=int(get_resolution(row[5])[0]),
                    screen_height=int(get_resolution(row[5])[1]),
                    cpu=row[6],
                    ram=get_ram_memory(row[7]),
                    memory1_storage=(mem1[0]),
                    memory1_GOT=(mem1[1]),
                    memory1_type=(mem1[2]),
                    memory2_storage=(mem2[0]),
                    memory2_GOT=(mem2[1]),
                    memory2_type=(mem2[2]),
                    gpu=row[9],
                    os=row[10],
                    weight_kg=row[11],
                    price_euro=row[12],
                    stock_amount=random.randint(0,10),
                )
                laptop.save()
            except Exception as error:
                print(f"was an {error}")


# load_laptops()





