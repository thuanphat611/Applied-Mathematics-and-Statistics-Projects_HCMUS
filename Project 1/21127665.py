from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

#hàm kiểm tra xem centroids sau 1 lần lặp có thay đổi không đáng kể hay không
def notChangedMuch(old, new):
    if old is None:# bỏ qua lần lăp đầu tiên
        return False
    change = np.sum(np.subtract(old, new)**2, axis = 1)**(1/2)#tính khoảng cách giữa giá trị cũ và mới của các centroids
    if np.all(change <= 3):#ở đây em xem như nếu khoảng cách <= 3 thì coi như thay đổi không đáng kể
        return True
    else:
        return False

#thuật toán K-means
def kmeans(img, k, maxIterations, initCentroids = "random"):
    if initCentroids == 'in_pixels':
        randomPixels = []
        for x in range(k):
            randomPixels.append(img[np.random.randint(img.shape[0])])#lấy ngẫu nhiên k pixel từ ảnh gốc
        centroids = np.array(randomPixels)
    else:
        centroids = np.array(np.random.randint(255, size=(k, img.shape[1])))# khởi tạo ndarray với giá trị ngẫu nhiên từ 0 tới 255

    countIterations = 0
    oldCentroids = None

    while (countIterations <= maxIterations) and not notChangedMuch(oldCentroids, centroids):
        oldCentroids = centroids
        countIterations += 1

        labels = []
        for x in img:
            distances = []
            for c in centroids:
                distances.append(np.sum((x - c)**2, axis = 0))#tính khoảng cách tới các centroids, có căn hay không cũng không ảnh hưởng
            label = distances.index(min(distances))# tìm centroid gần nhất
            labels.append(label)#cập nhật label
        
        centroids = []
        for j in range(k):
            pixelIndexes = [i for i in range(len(labels)) if labels[i] == j]#tìm những pixel có nhãn là index của centroid j
            if (pixelIndexes):
                centroid_j = img[pixelIndexes].mean(axis=0)#tính giá trị mới của centroid j
                centroids.append(centroid_j)#cập nhật giá trị
            else:#nếu không có pixel có nhãn là j thì giữ nguyên giá trị cũ
                centroids.append(oldCentroids[j])
    result = []
    for i in labels:
        result.append(centroids[i])
    return np.array(result,np.uint8)

#hàm main
def main():
    #tham số cho thuật toán K-means
    k_clusters = 7
    maxIterations = 100
    initType = 'ramdom'

    #nhập thông tin 
    fileName = input('Enter image name:')
    outputName = input('Enter output name:')
    while True:#nhập lại type nếu người dùng nhập sai(phải là 1 hoặc 2)
        type = int(input('Choose output type(input 1 for png, 2 for pdf):'))
        if (type != 1) and (type != 2):
            print('invalid output type')
            continue
        else:
            break

    img = Image.open(fileName)
    data = np.array(img)
    height = data.shape[0]#lưu lại kích thước ban đầu để sau này chuyển đổi lại
    width = data.shape[1]
    data = data.flatten().reshape(-1, 3) #chuyển thành 1d aray

    #sử dụng thuật toán k-means
    output = kmeans(data, k_clusters, maxIterations, initType)
    output = output.flatten().reshape(height, width, 3)
    
    #xác định tên file để lưu
    if type == 1:
        saveName = outputName + ".png"
    else:
        saveName = outputName + ".pdf"

    plt.imsave(saveName, output)
    print('Execution finished')

main()