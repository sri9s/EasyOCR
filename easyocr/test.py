import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import re
import easyocr
import time

reader = easyocr.Reader(['id', 'en']) # need to run only once to load model into memory
image_folder = '/data/jayachs1/outputs/EasyOCR/easyocr/images'
image_list = os.listdir(image_folder)
n=0
nama_regex_list = ["Na.a.*"]
r=re.compile("Na..?a.*")
no_images = 0
nama_count_detected = 0
gender_count_detected = 0
dob_count_detected = 0
for image in image_list:
    no_images=no_images+1
    print(no_images)
    image_path = os.path.join(image_folder,image)
    start = time.time()
    print(image)
    result = reader.readtext(image_path, decoder = 'wordbeamsearch', beamWidth= 4, batch_size = 1,\
                 workers = 0, allowlist = None, blocklist = None, detail = 0,\
                 rotation_info = None, paragraph = False, min_size = 20,\
                 contrast_ths = 0.5,adjust_contrast = 0.5, filter_ths = 0.003,\
                 text_threshold = 0.65, low_text = 0.4, link_threshold = 0.4,\
                 canvas_size = 2560, mag_ratio = 1.,\
                 slope_ths = 0.1, ycenter_ths = 0.5, height_ths = 0.5,\
                 width_ths = 0.5, y_ths = 0.5, x_ths = 1.0, add_margin = 0.1, output_format='standard') 
    # print(f'Time: {time.time() - start}')
    
    # print(result)
    newlist = list(filter(r.match, result)) # Read Note below
    # print(newlist)
    if 'Nama' in result:
        nama_count_detected+=1
        print('Nama: 1', end=" ")
        print(result[result.index('Nama')+1])
    elif len(newlist)>0:
        nama_count_detected+=1
        print(newlist, end=" ")
    else:
        print('Nama: 0', end=" ")
    if 'Tgl.Lahir' in result:
        print('DOB: 1', end=" ")
        dob_count_detected+=1
    else:
        print('DOB: 0', end=" ")
    if 'Alamat' in result:
        print('Alamat: 1', end=" ")
    else:
        print('Alamat: 0', end=" ")
    if 'WANITA' in result:
        print('Gender: Female')
        gender_count_detected=+1
    elif 'PRIA' in result:
        print('Gender: Male')
        gender_count_detected+=1
    else:
        print('Gender: 0')
print('nama detected:', nama_count_detected) 
print('nama detected%: ', (nama_count_detected/no_images))

print('gender detected:', gender_count_detected) 
print('gender detected%: ', (gender_count_detected/no_images))

print('dob detected:', dob_count_detected) 
print('dob detected%: ', (dob_count_detected/no_images))

print('no of images: ', no_images)
      