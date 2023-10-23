from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

#hàm tải ảnh
def loadimage(fileName):
    img = Image.open(fileName)
    data = np.array(img)
    return data

#hàm lưu ảnh cùng thư mục với ảnh gốc
def saveImage(fileName, image, method):
    splitPos = fileName.rfind(".")#tìm index của dấu chấm cuói cùng trong đường dẫn của ảnh(trước đuôi file)
    saveName  = fileName[:splitPos] + "_" + method + fileName[splitPos:]#chèn thêm tên phương thức thực hiện với ảnh
    #lưu ảnh
    s = Image.fromarray(image)
    s.save(saveName)

#hàm thay đổi độ sáng ảnh
def changeBrightness(data, alpha):
    height = data.shape[0]#lưu lại kích thước ban đầu để sau này chuyển đổi lại
    width = data.shape[1]
    data = data.flatten().reshape(-1, 3) #chuyển thành 1d aray để dễ xử lí

    result = []
    for x in data:
        pixel = []
        for y in x:
            if y + alpha <= 255 and y + alpha >= 0:#giá trị tối đa sau khi cộng là 255
                pixel.append(y + alpha)
            else:
                if y + alpha > 255:
                    pixel.append(255)
                elif y + alpha < 0:
                    pixel.append(0)
        result.append(pixel)
    result =  np.array(result, np.uint8)
    result = result.flatten().reshape(height, width, 3)#chuyển ảnh về shape ban đầu

    return result

#hàm thay đổi độ tương phản ảnh
def changeContrast(data, alpha):
    height = data.shape[0]#lưu lại kích thước ban đầu để sau này chuyển đổi lại
    width = data.shape[1]
    data = data.flatten().reshape(-1, 3) #chuyển thành 1d aray để dễ xử lí

    result = []
    for x in data:
        pixel = []
        for y in x:
            if int(y * alpha) <= 255:#giá trị tối đa sau khi nhân là 255
                pixel.append(y * alpha)
            else:
                pixel.append(255)
        result.append(pixel)
    result =  np.array(result, np.uint8)
    result = result.flatten().reshape(height, width, 3)#chuyển ảnh về shape ban đầu

    return result

#hàm lật ảnh ngang/dọc
def flip(data, direction):
    if direction != 1 and direction != 2:#1: vertical / 2: horizontal 
        print("Flip: invalid direction")
        return
    
    if direction == 1:#dọc
        result = []
        for x in data:
            result.insert(0, x)
    elif direction == 2:#ngang
        result = []
        for x in data:
            row = []
            for y in x:
                row.insert(0, y)
            result.append(row)
    
    result =  np.array(result, np.uint8)

    return result

#hàm chuyển ảnh thành ảnh xám/sepia
def convertGS(data, type):
    if type != 1 and type != 2:#1: grayscale / 2: sepia 
        print("convertGS: invalid type")
        return
    
    if type == 1:#xám
        result = []
        for x in data:
            row = []
            for y in x:
                pixel = int(1/3*y[0] + 1/3*y[1] + 1/3*y[2])
                
                row.append(pixel)
            result.append(row)
    elif type == 2:#sepia
        result = []
        for x in data:
            row = []
            for y in x:
                tr = int(0.393*y[0] + 0.769*y[1] + 0.189*y[2])
                tg = int(0.349*y[0] + 0.686*y[1] + 0.168*y[2])
                tb = int(0.272*y[0] + 0.534*y[1] + 0.131*y[2])
                if tr > 255:
                    tr = 255
                if tg > 255:
                    tg = 255
                if tb > 255:
                    tb = 255
                pixel = [tr, tg, tb]
                row.append(pixel)
            result.append(row)

    result =  np.array(result, np.uint8)

    return result

#hàm cắt ảnh ở trung tâm 
def crop(data, width, height):
    if height > data.shape[0] or width > data.shape[1]: 
        print("invalid size")
        return
    m = (data.shape[1] - width) // 2
    n = (data.shape[0] - height) // 2

    result = []
    for x in range(height):
        row = []
        for y in range(width):
            row.append(data[x + n][y + m])
        result.append(row)

    result =  np.array(result, np.uint8)

    return result

#hàm làm mờ ảnh
def blur(data):
    #sao chép lại mảng hình ảnh, thêm viền là các pixel [0, 0, 0]
    copy = data.copy()
    copy = copy.tolist()
    add = []
    for i in range(data.shape[1]):
        add.append([0, 0, 0])
    copy.insert(0, add)
    copy.append(add)
    for j in copy:
        j.insert(0, [0, 0, 0])
        j.append([0, 0, 0])

    result = []
    for x in range(data.shape[0]):
        row = []
        for y in range(data.shape[1]):
            n = 9#số pixel tính trung bình

            #nếu ở biên thì chỉ tính trung bình 6 pixels
            if (x == 0 and y != 0 and y != data.shape[1] - 1) or (x != 0 and x != data.shape[0] - 1 and y == data.shape[1] - 1) or (x == data.shape[0] - 1 and y != 0 and y != data.shape[1] - 1) or (x != 0 and x != data.shape[0] - 1 and y == 0):
                n = 6
            #nếu ở góc thì chỉ tính trung bình 4 pixels
            if (x == 0 and y == 0) or (x == 0 and y == data.shape[1] - 1) or (x == data.shape[0] - 1 and y == 0) or (x == data.shape[0] - 1 and y == data.shape[1] - 1):
                n = 4

            #có thêm viền nên cách tính vị trí các pixel xung quanh thay đổi
            #t:top b:bottom l:left r:right 
            pixel = []
            tl = copy[x][y]
            tc = copy[x][y + 1]
            tr = copy[x][y + 2]
            cl = copy[x + 1][y]
            cc = copy[x + 1][y + 1]
            cr = copy[x + 1][y + 2]
            bl = copy[x + 2][y]
            bc = copy[x + 2][y + 1]
            br = copy[x + 2][y + 2]
            
            pixel.append(tl[0] / n + tc[0] / n + tr[0] / n + cl[0] / n + cc[0] / n + cr[0] / n + bl[0] / n + bc[0] / n + br[0] / n)
            pixel.append(tl[1] / n + tc[1] / n + tr[1] / n + cl[1] / n + cc[1] / n + cr[1] / n + bl[1] / n + bc[1] / n + br[1] / n)
            pixel.append(tl[2] / n + tc[2] / n + tr[2] / n + cl[2] / n + cc[2] / n + cr[2] / n + bl[2] / n + bc[2] / n + br[2] / n)
            row.append(pixel)
        result.append(row)
            
    result =  np.array(result, np.uint8)

    return result

#hàm làm sắc nét ảnh
def sharpen(data):
    copy = data.copy()
    copy = copy.tolist()
    add = []
    for i in range(data.shape[1]):
        add.append([0, 0, 0])
    copy.insert(0, add)
    copy.append(add)
    for j in copy:
        j.insert(0, [0, 0, 0])
        j.append([0, 0, 0])

    result = []
    for x in range(data.shape[0]):
        row = []
        for y in range(data.shape[1]):
            #có thêm viền nên cách tính vị trí các pixel xung quanh thay đổi
            #t:top b:bottom l:left r:right c:center
            pixel = []
            t = copy[x][y + 1]
            l = copy[x + 1][y]
            c = copy[x + 1][y + 1]
            r = copy[x + 1][y + 2]
            b = copy[x + 2][y + 1]
            
            pixel.append(c[0]*5 - t[0] - r[0] - b[0] - l[0])
            pixel.append(c[1]*5 - t[1] - r[1] - b[1] - l[1])
            pixel.append(c[2]*5 - t[2] - r[2] - b[2] - l[2])
            #kiểm tra lại giá trị vừa tính
            for i in range(len(pixel)):
                if pixel[i] > 255:
                    pixel[i] = 255
                elif pixel[i] < 0:
                    pixel[i] = 0
            row.append(pixel)
        result.append(row)
    result =  np.array(result, np.uint8)

    return result

#hàm cắt ảnh hình tròn(đường kính là kích thước nhỏ nhất giữa chiều dài và chiều rộng)
def circle(data):
    blackColor = [0, 0, 0]
    radius = min(data.shape[0], data.shape[1]) / 2 #bán kính của ảnh mới sẽ là một nửa chiều dài ngắn nhất của ảnh
    #tìm tâm hình tròn
    centerX = int(data.shape[0] / 2)
    centerY = int(data.shape[1] / 2)
    #tìm số pixel dư ra ở mỗi chiều ngang, dọc

    result = []
    for x in range(data.shape[0]):
        row = []
        for y in range(data.shape[1]):
            distance  = (x - centerX) ** 2 + (y - centerY) ** 2 
            if distance <= radius ** 2:
                row.append(data[x][y])
            else:
                row.append(blackColor)
        result.append(row)

    result =  np.array(result, np.uint8)

    return result

#Phần hàm chính----------------------------------------------------------------
def main():
    print("1: increase brightness")
    print("2: increase contrast")
    print("3: flip")
    print("4: convert grayscale/sepia")
    print("5: blur/sharpen")
    print("6: crop")
    print("7: circle crop")
    print("0: do all")
    while True:
        method = int(input("Choose method: "))
        if method >= 0 and method <= 7:
            break
        else:
            continue
    name = input("File path: ")
    data = loadimage(name)

    if method == 1:
        output = changeBrightness(data, 64)
        saveImage(name, output, "changeBrightness")
    elif method == 2:
        output = changeContrast(data, 1.5)
        saveImage(name, output, "changeContrast")
    elif method == 3:
        direction = int(input("Direction(1: vertical/2: horizontal): "))
        output = flip(data, direction)
        if direction == 1:
            saveImage(name, output, "flip_vertical")
        else:
            saveImage(name, output, "flip_horizontal")
    elif method == 4:
        t = int(input("Type(1: grayscale/2: sepia): "))
        output = convertGS(data, t)
        if t == 1:
            saveImage(name, output, "grayscale")
        else:
            saveImage(name, output, "sepia")
            
    elif method == 5:
        while True:
            t = int(input("Method(1: blur/2: sharpen): "))
            if t == 1 or t == 2:
                break
        if t == 1:
            output = blur(data)
            saveImage(name, output, "blur")
        else:
            output = sharpen(data)
            saveImage(name, output, "sharpen")
    elif method == 6:
        width = int(input("Width: "))
        height = int(input("Height: "))
        output = crop(data, width, height)
        saveImage(name, output, "crop")
    elif method == 7:
        output = circle(data)
        saveImage(name, output, "circle")
    else:
        output = changeBrightness(data, 64)
        saveImage(name, output, "changeBrightness")

        output = changeContrast(data, 1.5)
        saveImage(name, output, "changeContrast")

        direction = int(input("Direction(1: vertical/2: horizontal): "))
        output = flip(data, direction)

        if direction == 1:
            saveImage(name, output, "flip_vertical")
        else:
            saveImage(name, output, "flip_horizontal")

        t1 = int(input("Type(1: grayscale/2: sepia): "))
        output = convertGS(data, t1)
        if t1 == 1:
            saveImage(name, output, "grayscale")
        else:
            saveImage(name, output, "sepia")

        while True:
            t2 = int(input("Method(1: blur/2: sharpen): "))
            if t2 == 1 or t2 == 2:
                break
        if t2 == 1:
            output = blur(data)
            saveImage(name, output, "blur")
        else:
            output = sharpen(data)
            saveImage(name, output, "sharpen")

        width = int(input("Width: "))
        height = int(input("Height: "))
        output = crop(data, width, height)
        saveImage(name, output, "crop")

        output = circle(data)
        saveImage(name, output, "circle")

    print("Executioon finished")

#gọi hàm main
main()
