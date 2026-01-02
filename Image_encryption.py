from PIL import Image
import numpy as np 

image = Image.open(r"key_image.jpg")

# image.show()

px = np.array(image)

height, width = px.shape[:2]

# print(height,width)

matrix = []

for i in range(height):
    for j in range(width):
        r,g,b = px[i,j]
        sum = (((r + g)%256 + b) % 256)
        if sum not in matrix:
            matrix.append(sum)

print(matrix)

print(len(matrix))


inputimg = Image.open(r"image.jpg").convert("RGB")

inputimg.show()

pixelate = np.array(inputimg)

h,w = pixelate.shape[:2]

# print(h,w)

rmatrix = []
gmatrix = []
bmatrix = []

for i in range(h):
    for j in range(w):
        r,g,b = pixelate[i,j]
        rmatrix.append(r)
        gmatrix.append(g)
        bmatrix.append(b)

# print("Rmatrix : \n",rmatrix)
# print(gmatrix)
# print(bmatrix)
# print("\n\n\n")

###
# rmatrix = np.array(rmatrix).reshape(h,w)
# gmatrix = np.array(gmatrix).reshape(h,w)
# bmatrix = np.array(bmatrix).reshape(h,w)

# realrgb = np.dstack((rmatrix,gmatrix,bmatrix))
# realimage = Image.fromarray(realrgb.astype('uint8'), 'RGB')

# realimage.show()
###

def encryption(p,q):
    # print("Encryption function.")
    # print("Encrypting...")

    xindex = matrix.index(p)
    yindex = matrix.index(q)

    if ((xindex//16) == (yindex//16)):
        xindex = xindex + 1
        yindex = yindex + 1

        if ((xindex%16) == 0): xindex -= 16
        if ((yindex%16) == 0): yindex -= 16
    elif ((xindex%16) == (yindex%16)):
        xindex = ((xindex+16)%256)
        yindex = ((yindex+16)%256)
    else :
        if (xindex%16) < (yindex%16):
            temp = (yindex%16) - (xindex%16)
            xindex += temp
            yindex -= temp
        else :
            temp = (xindex%16) - (yindex%16)
            xindex -= temp
            yindex += temp
    return (matrix[xindex],matrix[yindex])

for x in range(0,h*w,2):
    if (x == ((h*w)-1)):continue; #for handling error
    p1 = rmatrix[x]
    q1 = gmatrix[x]
    rmatrix[x],gmatrix[x] = encryption(p1,q1)

    p2 = bmatrix[x]
    q2 = rmatrix[x+1]
    bmatrix[x],rmatrix[x+1] = encryption(p2,q2)

    p3 = gmatrix[x+1]
    q3 = bmatrix[x+1]
    gmatrix[x+1],bmatrix[x+1] = encryption(p3,q3)

# print("\n\n\n")

# print("After Encryption : ", rmatrix)
# print("After Encryption : ",gmatrix)
# print("After Encryption : ", bmatrix)


def shuffling(matt):
    newmatrix = []
    mid = len(matt)//2
    first = matt[:mid]
    second = matt[mid:]

    for n,m in zip(first,second):
        newmatrix.append(n)
        newmatrix.append(m)
    
    return newmatrix

rmatrix, gmatrix, bmatrix = shuffling(rmatrix), shuffling(gmatrix), shuffling(bmatrix)

rmatrix = np.array(rmatrix).reshape(h,w)
gmatrix = np.array(gmatrix).reshape(h,w)
bmatrix = np.array(bmatrix).reshape(h,w)

encryptedrgb = np.dstack((rmatrix,gmatrix,bmatrix))

encryptedimage = Image.fromarray(encryptedrgb.astype('uint8'),'RGB')

encryptedimage.show()

encryptedimage.convert("RGB")

encryptedimage.save(r"encrypted_image.png")



### Decryption start from here 

decryptionimage = Image.open(r"encrypted_image.png").convert("RGB")

decryptpixel = np.array(decryptionimage)

dh, dw = decryptpixel.shape[:2]

encryrmat = []
encrygmat = []
encrybmat = []

for k in range(dh):
    for l in range(dw):
        r,g,b = decryptpixel[k,l]
        encryrmat.append(r)
        encrygmat.append(g)
        encrybmat.append(b)

def decryption(p,q):
    # print("Decrypting the image ... " )
    xindex = matrix.index(p)
    yindex = matrix.index(q)

    if ((xindex//16) == (yindex//16)):
        if xindex%16 == 0: xindex += 15
        else:xindex = xindex - 1
        if yindex%16 == 0: yindex += 15
        else: yindex = yindex - 1
    elif (xindex%16) == (yindex%16):
        if xindex < 16: xindex = 240+(xindex%16)
        else : xindex -= 16
        if yindex < 16: yindex = 240+(yindex%16)
        else : yindex -= 16
    else :
        if (xindex%16) < (yindex%16):
            temp = (yindex%16) - (xindex%16)
            xindex += temp
            yindex -= temp
        else :
            temp = (xindex%16) - (yindex%16)
            xindex -= temp
            yindex += temp
    
    return (matrix[xindex],matrix[yindex])

def unshuffling(matt):
    realmatrix = []
    first = matt[0::2]
    second = matt[1::2]

    realmatrix = first + second

    return realmatrix

encryrmat, encrygmat, encrybmat = unshuffling(encryrmat), unshuffling(encrygmat), unshuffling(encrybmat)

for y in range(0,h*w, 2):
    if y == (h*w)-1:continue
    p1 = encryrmat[y]
    q1 = encrygmat[y]
    encryrmat[y], encrygmat[y] = decryption(p1,q1)

    p2 = encrybmat[y]
    q2 = encryrmat[y+1]
    encrybmat[y], encryrmat[y+1] = decryption(p2,q2)

    p3 = encrygmat[y+1]
    q3 = encrybmat[y+1]
    encrygmat[y+1], encrybmat[y+1] = decryption(p3,q3)

encryrmat = np.array(encryrmat).reshape(h,w)
encrygmat = np.array(encrygmat).reshape(h,w)
encrybmat = np.array(encrybmat).reshape(h,w)

decryptrgb = np.dstack((encryrmat, encrygmat, encrybmat))

decryptimg = Image.fromarray(decryptrgb.astype('uint8'),'RGB')

decryptimg.show()
