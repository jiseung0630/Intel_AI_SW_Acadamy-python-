from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
import os.path
import math
from tkinter.simpledialog import *
##함수부

#**************
#공통 함수부
#**************

def malloc2D(h, w, initValue=0) :
    memory = [[initValue for _ in range(w)] for _ in range(h)]
    return memory
def maskcircleImage():
    global window, canvas, paper, fullname, fullname1
    global inImage, outImage, maskcircle, inH, inW, outH, outW, maskcircleH, maskcircleW
    fullname1 = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    # 중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname1)  # 파일 크기(Byte)
    maskcircleH = maskcircleW = int(math.sqrt(fsize))
    # 메모리 할당
    maskcircle = malloc2D(maskcircleH, maskcircleW)
    # 파일 --> 메모리
    rfp = open(fullname1, 'rb')
    for i in range(maskcircleH):
        for k in range(maskcircleW):
            mask[i][k] = ord(rfp.read(1))
    rfp.close()

def openImage():
    global  window, canvas, paper, fullname
    global  inImage, outImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    #중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname) #파일 크기(Byte)
    inH = inW = int(math.sqrt(fsize))
    #메모리 할당
    inImage = malloc2D(inH,inW)
    #파일 --> 메모리
    rfp = open(fullname, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(rfp.read(1))
    rfp.close()
    equalImage()

def saveImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    if ( outImage == None or len(outImage)==0) : #영상처리를 한적이 없다면...
        return
    wfp = asksaveasfile(parent=window, mode ='wb',defaultextension="*.raw",
                        filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    import struct
    for i in range(outH) :
        for k in range(outW) :
            wfp.write(struct.pack("B", outImage[i][k]))
        wfp.write()
        messagebox.showinfo("성공", wfp.name + "저장완료!")

def displayImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    ##기존에 이미지를 오픈한 적이 있으면, 캔버스 뜯어내기
    if(canvas != None):
        canvas.destroy()

    ##벽, 캔버스, 종이 설정
    window.geometry(str(outH)+'x'+str(outW)) #512x512
    canvas = Canvas(window, height=outH, width=outW, bg='yellow')  # 칠판
    paper = PhotoImage(height=outH, width=outW)  # 종이
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')
    ##메모리 --> ghkaus
    # for i in range(outH):
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]
    #         paper.put('#%02x%02x%02x' % (r, g, b), (k, i))
    #더블 버퍼링... 비슷한 기법( 모두다 메모리상에 출력형태로 생성항 후에, 한방에 출력)
    rgbString ="" #전체에 대한 16진수 문자열
    for i in range(outH) :
        oneString = "" # 한줄에 대한 16진수 문자열
        for k in range(outW):
            r=g=b=outImage[i][k]
            oneString += '#%02x%02x%02x ' % (r, g, b)
        rgbString += "{" + oneString + "} "
    paper.put(rgbString)
    canvas.pack()

#**************
#영상처리 함수부
#**************

def equalImage(): #동일 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    #중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    #메모리 할장
    outImage = malloc2D(outH,outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
##########################
    displayImage()

def addImage(): #밝게 어둡게 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    #중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    #메모리 할장
    outImage = malloc2D(outH,outW)
    ### 진짜 영상처리 알고리즘 ###
    value = askinteger('정수입력', '-255~255 입력', maxvalue=255, minvalue=-255)
    for i in range(inH):
        for k in range(inW):
            px = inImage[i][k] + value
            if(px > 255):
                px = 255
            if(px < 0):
                px =0
            outImage[i][k] = px
##########################
    displayImage()

def opImage():##반전 함수
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()

def blackImage():
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## inImage픽셀의 평균값 구하기
    hap = 0 ##inImage 픽셀의 합
    avg = 0 ##inImage 픽셀의 평균값
    for i in range(inH):
        for k in range(inW):
            hap += inImage[i][k]
    avg = hap/(inH*inW)
    ### 진짜 영상 처리 알고리즘###
    for i in range(outH):
        for k in range(outW):
            if(inImage[i][k] > avg):
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    ######################
    displayImage()

def orImage():
    global inImage, outImage, maskcircle, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ##마스크에 크기 할당 후 값넣어 놓기
    maskcircleImage()
    ### 진짜 영상 처리 알고리즘###
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i][k] | maskcircle[i][k]
    ######################
    displayImage()

def andImage():
    global inImage, outImage, maskcircle, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ##마스크에 크기 할당 후 값넣어 놓기
    maskcircleImage()
    ### 진짜 영상 처리 알고리즘###
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i][k] & maskcircle[i][k]
    ######################
    displayImage()

def xorImage():
    global inImage, outImage, mask, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ##비교값 입력 받기
    value = askinteger('정수입력', '0~255 입력', maxvalue=255, minvalue=0)
    ### 진짜 영상 처리 알고리즘###
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i][k] ^ value
    ######################
    displayImage()

def Threshold():
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    value = askinteger('경계값 입력', '0~255 입력', maxvalue=255, minvalue=0)
    ### 진짜 영상처리 알고리즘 ###

    for i in range(outH):
        for k in range(outW):
            if(inImage[i][k] >= value):
                outImage[i][k] = 255
            if(inImage[i][k] < value):
                outImage[i][k] = 0
    displayImage()

def emboss():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)

    #############
    ##화소영역처리
    #############
    mask = malloc2D(3,3) ## 임시입력메모리를초기화(127): 필요시 평균값
    mask = [[-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]]
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2,127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW): ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0; ##마스크 9개와 입력값 9개를 각각 곱해서 합한 값.

            for m in range (3):
                for n in range (3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S


    ##후처리(마스크값의 합계에 따라서...)
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def blur():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)
    value = askinteger('정수입력', '홀수 입력', minvalue=0)
    #############
    ##화소영역처리
    #############
    mask = malloc2D(value,value,1/(value*value)) ## 임시입력메모리를초기화(127): 필요시 평균값
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + (value-1), inW + (value-1),127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW): ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0

            for m in range (value):
                for n in range (value):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S


    # ##후처리(마스크값의 합계에 따라서...)
    # for i in range(outH):
    #     for k in range(outW):
    #         tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def sharppning():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)

    #############
    ##화소영역처리
    #############
    mask = malloc2D(3,3) ## 임시입력메모리를초기화(127): 필요시 평균값
    mask = [[-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]]
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2,127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW): ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0; ##마스크 9개와 입력값 9개를 각각 곱해서 합한 값.

            for m in range (3):
                for n in range (3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S


    # ##후처리(마스크값의 합계에 따라서...)
    # for i in range(outH):
    #     for k in range(outW):
    #         tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def hfsharppning():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)

    #############
    ##화소영역처리
    #############
    mask = malloc2D(3,3) ## 임시입력메모리를초기화(127): 필요시 평균값
    mask = [[-1/9, -1/9, -1/9],
            [-1/9, 8/9, -1/9],
            [-1/9, -1/9, -1/9]]
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2,127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW): ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0; ##마스크 9개와 입력값 9개를 각각 곱해서 합한 값.

            for m in range (3):
                for n in range (3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S


    ##후처리(마스크값의 합계에 따라서...)
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def edgeVer():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)

    #############
    ##화소영역처리
    #############
    mask = malloc2D(3, 3)  ## 임시입력메모리를초기화(127): 필요시 평균값
    mask = [[0, 0, 0],
            [-1, 1, 0],
            [0, 0, 0]]
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2, 127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW):  ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0;  ##마스크 9개와 입력값 9개를 각각 곱해서 합한 값.

            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S

    ##후처리(마스크값의 합계에 따라서...)
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def edgeHor():
    global inImage, outImage, inH, inW, outH, outW
    ##(중요!)출력이미지의크기를 결정 - --> 알고리즘에 의존
    outH = inH
    outW = inW
    ##메모리 할당
    outImage = malloc2D(outH, outW)

    #############
    ##화소영역처리
    #############
    mask = malloc2D(3, 3)  ## 임시입력메모리를초기화(127): 필요시 평균값
    mask = [[0, -1, 0],
            [0, 1, 0],
            [0, 0, 0]]
    ##임시 메모리할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2, 127)
    tmpOutImage = malloc2D(outH, outW)

    ##입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    ####회선 연산#####
    for i in range(inH):
        for k in range(inW):  ##마스크(3x3) 와 한점을 중심으로한 3x3을 곱하기
            S = 0.0;  ##마스크 9개와 입력값 9개를 각각 곱해서 합한 값.

            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]

            tmpOutImage[i][k] = S

    ##후처리(마스크값의 합계에 따라서...)
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127.0

    ##임시출력영상 --> 출력영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0):
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

### 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage, maskcircle = [], [], []
inH, inW, outH, outW, maskcircleH, maskcircleW = [0]*6
fullname = ''
fullname1 = ''

###메인 코드부
window = Tk() # 벽
window.geometry("500x500")
window.resizable(width=False, height=False)
window.title("영상처리(RC 1)")

# 메뉴 만들기
mainMenu = Menu(window) # 메뉴의 틀
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (파일)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openImage)
fileMenu.add_command(label='저장', command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label='종료',command=None)

pixelMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (화소점 처리)
mainMenu.add_cascade(label='화소점 처리', menu=pixelMenu)
pixelMenu.add_command(label='동일 이미지', command=equalImage)
pixelMenu.add_command(label='밝게/어둡게', command=addImage)
pixelMenu.add_command(label='반전', command=opImage)
pixelMenu.add_command(label='흑백', command=blackImage)
pixelMenu.add_command(label='OR', command=orImage)
pixelMenu.add_command(label='AND', command=andImage)
pixelMenu.add_command(label='XOR', command=xorImage)
pixelMenu.add_command(label='이진 프로그램', command=Threshold)

pixelAreaMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (화소점 처리)
mainMenu.add_cascade(label='화소영역 처리', menu=pixelAreaMenu)
pixelAreaMenu.add_command(label='엠보싱', command=emboss)
pixelAreaMenu.add_command(label='블러링', command=blur)
pixelAreaMenu.add_command(label='샤프닝', command=sharppning)
pixelAreaMenu.add_command(label='고주파 필터 샤프닝', command=hfsharppning)
pixelAreaMenu.add_command(label='수평엣지 검출', command=edgeHor)
pixelAreaMenu.add_command(label='수직엣지 검출', command=edgeVer)








window.mainloop()