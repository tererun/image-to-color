import PIL
from PIL import Image
import cv2
import sklearn
from sklearn.cluster import KMeans
import glob
import json

def get_main_colors(img_path):
    cv2_img = cv2.imread(img_path)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    cv2_img = cv2_img.reshape(
        (cv2_img.shape[0] * cv2_img.shape[1], 3))
    
    cluster = KMeans(n_clusters=5)
    cluster.fit(X=cv2_img)
    cluster_centers_arr = cluster.cluster_centers_.astype(
        int, copy=False)

    colors = {
        "name": img_path[9:],
        "colors": []
    }

    for i, rgb_arr in enumerate(cluster_centers_arr):
        color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
        colors.get('colors').append(color_hex_str)
    
    return colors

blocks = []

for path in glob.glob('./images/*.png'):
    print(path + ' を処理中...')
    blocks.append(get_main_colors(img_path=path))

print('======================\n処理が完了しました!\n======================')

file = open('output.json', 'w', encoding='UTF-8')
file.write(json.dumps(blocks) + '\n')
file.close()