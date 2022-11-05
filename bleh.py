# from PIL import Image
# img = Image.open("test.png")
# img2 = img.crop((852, 766 , 1065 ,970 ))
# img2.save("test_crop.png")
# img2.show()


a

def compute():
    # pixel level computation

    rdiff = decimal.Decimal(0)
    gdiff = decimal.Decimal(0)
    bdiff = decimal.Decimal(0)
    n = 0
    x = 1

    frames = os.listdir(data_path)  # directory containing the frames of the video
    frames = natsorted(frames)  # sorting the files in order
    for frame in frames:
        file = pathlib.Path('data' + '/' + str(x) + '.jpg')
        if file.exists():
            pic = imageio.imread('data' + '/' + str(n) + '.jpg')
            pic1 = imageio.imread('data' + '/' + str(x) + '.jpg')
            height = int(format(pic.shape[0]))
            width = int(format(pic.shape[1]))
            tcount = height * width
            print('total number of pixels: ' + str(tcount))
            print('Computing Frames: ' + str(n) + ' and ' + str(x))

            # get diff of R, G and B channels:
            # pixel level computation
            for i in range(pic.shape[0]):
                for j in range(pic.shape[1]):
                    # RGB values of fist frame:
                    R1 = int(format(pic[i, j, 0]))
                    G1 = int(format(pic[i, j, 1]))
                    B1 = int(format(pic[i, j, 2]))

                    # RGB values of second frame:
                    R2 = int(format(pic1[i, j, 0]))
                    G2 = int(format(pic1[i, j, 1]))
                    B2 = int(format(pic1[i, j, 2]))

                    rdiff += abs(R2 - R1) / decimal.Decimal('255')  # getting a decimal value between 0 and 1
                    gdiff += abs(G2 - G1) / decimal.Decimal('255')
                    bdiff += abs(B2 - B1) / decimal.Decimal('255')

            # average values of each channel:
            rdiff = rdiff / decimal.Decimal(tcount)
            gdiff = gdiff / decimal.Decimal(tcount)
            bdiff = bdiff / decimal.Decimal(tcount)

            difference = float(rdiff + gdiff + bdiff) / 3

            if (difference >= threshold):
                key_frames.append(str(x))
                n = x
            x += 1

    print('Computation completed , yaaaaaaaaaaaaaaaaaaaaaaaay')




###############################################################################



rdiff = decimal.Decimal(0)
gdiff = decimal.Decimal(0)
bdiff = decimal.Decimal(0)

gt = Image.open('4820.png')
gt_crop = Image.open('test_crop.png')



height, width = gt_crop.size

tcount = height * width

#create a temp crop from the gt image
temp_crop = gt.crop((852, 766 , 1065 ,970 ))
temp_crop.show()

rgb_temp_crop = temp_crop.convert('RGB')
rgb_gt_crop = gt_crop.convert('RGB')


for i in range(height):
    for j in range(width):
        # R1 = int(format(gt_crop[i, j, 0]))
        # G1 = int(format(gt_crop[i, j, 1]))
        # B1 = int(format(gt_crop[i, j, 2]))

        R1, G1, B1 = rgb_gt_crop.getpixel((i,j))

        # RGB values of second frame:
        # R2 = int(format(temp_crop[i, j, 0]))
        # G2 = int(format(temp_crop[i, j, 1]))
        # B2 = int(format(temp_crop[i, j, 2]))

        R2, G2, B2 = rgb_temp_crop.getpixel((i,j))

        rdiff += round((abs(R2 - R1) / decimal.Decimal('255')),1)  # getting a decimal value between 0 and 1
        gdiff += round((abs(G2 - G1) / decimal.Decimal('255')),1)
        bdiff += round((abs(B2 - B1) / decimal.Decimal('255')),1)

        print(rdiff, gdiff, bdiff)

# average values of each channel:
rdiff = rdiff / decimal.Decimal(tcount)
gdiff = gdiff / decimal.Decimal(tcount)
bdiff = bdiff / decimal.Decimal(tcount)

difference = float(rdiff + gdiff + bdiff) / 3

print(rdiff, gdiff, bdiff)

print(difference)
