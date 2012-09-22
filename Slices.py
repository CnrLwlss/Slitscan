import numpy,PIL,os,psutil
from PIL import Image
#inroot="Q:\\TronBR\\FRAMES\\TRON%05d.png"
#outdir="Q:\\TronBR\\OUT\\"

inroot="F:\\Videos\\SlitscanTest\\Frames\\Frame%05d.png"
outdir="Q:\\Slitscan\\"

# Count the available frames
frameno=0
while 1:
    if os.path.exists(inroot%frameno):
        frameno+=1
    else:
        break

# Load first frame & check size
print("Creating empty array....")
first=Image.open(inroot%0)
w,h=first.size

# Assess memory requirements and availability
reqGb=float(frameno*w*h*3)/float(1024*1024*1024)
availGb=float(psutil.virtual_memory().available)/float(1024*1024*1024)
fracallowed=0.9
if (reqGb>fracallowed*availGb):
    frameno=int(round(float(frameno)*fracallowed*availGb/reqGb))
print("Using this number of frames: "+str(frameno))
# Create master storage array
mastarr=numpy.zeros((frameno,h,w,3),numpy.uint8)

# Fill master storage array
print("Loading data into array....")
for frame in xrange(frameno):
    if frame%500==0:
        print ("%05d out of %05d"%(frame,frameno))
    im=Image.open(inroot%frame)
    arr=numpy.array(im,numpy.uint8)
    del im
    mastarr[frame,:,:,:]=arr
    del arr

### Horizontal slices through all available frames
##outw,outh=w,frameno
##outarr=numpy.zeros((outh,outw,3),numpy.uint8)
##print("Creating output images for horizontal slice...")
##for H in xrange(h):
##    if H%10==0:
##        print ("%05d out of %05d"%(H,h))
##    outarr=mastarr[H,:,:,:]
##    image=Image.fromarray(outarr)
##    image.save(os.path.join(outdir,"OpeningCredits%05d.png"%H))

# A diagonal slice through images to make a HD frame
outw,outh=w,min(h,frameno)
posarr=numpy.zeros((outh,outw,3),numpy.uint8)
negarr=numpy.zeros((outh,outw,3),numpy.uint8)
print("Creating output images for diagonal horizontal slices...")
for frm in xrange(0,frameno-outh+1):
    for H in xrange(0,outh):
        posarr[H,:,:]=mastarr[frm+H,H,:,:]
        negarr[H,:,:]=mastarr[frm+outh-1-H,H,:,:]
    posimage=Image.fromarray(posarr)
    posimage.save(os.path.join(outdir,"DiagonalPos%05d.png"%frm))
    negimage=Image.fromarray(negarr)
    negimage.save(os.path.join(outdir,"DiagonalNeg%05d.png"%frm))
