# %%
import os
from PIL import Image
pixW = 48  # height of each sprite
pixH = 48  # width of each sprite
modW = 0   # if the height and width are not the same, use this to adding padding to both side
modH = 0
totalImgToMerge = 3  # images to merge into one horizontally
imgType = ".png"
inputDir = "./input/"
outputDir = "./output/"
mergedDir = "./merged/"
separatedDir = "./seperated/"
# For standard RPG Maker sprites use line 12 and 91, if not standard RPG Maker spirit use line 13 and 92
stateName = ["front", "left", "right", "back", "death"]
# spriteRowCount = 0

# %%
# Create folders to hold output and merged images
if not os.path.exists(mergedDir):
    os.mkdir(mergedDir)

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

if not os.path.exists(separatedDir):
    os.mkdir(separatedDir)

# Open the image
imgFiles = [f for f in os.listdir(inputDir) if f.endswith(imgType)]

# Initialize a counter for the output file names
count = 0

for image in imgFiles:
    img = Image.open(inputDir + image)

    # get image Name
    imgName = image[:-4]

    # Get the width and height of the image
    width, height = img.size

    # Calculate the number of rows and columns
    rows = height // pixH
    cols = width // pixW

    # Slice the image into 48 by 48 pixels and save each slice
    for row in range(rows):
        for col in range(cols):
            left = col * pixW
            top = row * pixH
            right = left + pixW
            bottom = top + pixH
            crop = img.crop((left, top, right, bottom))
            outputFilename = outputDir + \
                f"{imgName}_{str(row).zfill(3)}_{str(col).zfill(3)}{imgType}"
            crop.save(outputFilename)
            separatedFilename = separatedDir + \
                f"{imgName}_{str(row).zfill(3)}_{str(col).zfill(3)}{imgType}"
            crop.save(separatedFilename)

    # Get a list of all the image files in the outputDir
    imgFiles = [f for f in os.listdir(outputDir) if f.endswith(imgType)]

    # Sort the image files by name
    imgFiles.sort()

    # Assuming all images are the same size
    modImgW = pixW + modW*2
    modImgH = pixH + modH*2

    # create an empty image for merging
    merged = Image.new("RGBA", ((modImgW*totalImgToMerge, modImgH)))

    while len(imgFiles) >= totalImgToMerge:
        for x in range(totalImgToMerge):
            # Open the image to be merged
            img = Image.open(outputDir + imgFiles.pop(0))

            # Create a new image to deal with height/width mismatch
            imgNew = Image.new('RGBA', (modImgW, modImgH), (0, 0, 0, 0))

            # past the original to the center of the new image
            imgNew.paste(img, (modW, modH))

            # Paste the modified image to the final image
            merged.paste(imgNew, (modImgW*x, 0))

        # Save the merged image with the next output filename
        mergedFilename = mergedDir + f"{imgName}_{stateName[count]}{imgType}"
        # mergedFilename = mergedDir + f"{imgName}_{str(count).zfill(3)}_merged{imgType}"
        merged.save(mergedFilename)
        count += 1

    # Remove all the image files from the outputDir for the next image
    for f in os.listdir(outputDir):
        os.remove(os.path.join(outputDir, f))

    # increment leadingCount to distinguish images from different source files
    count = 0
