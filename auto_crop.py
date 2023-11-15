import os
import cv2
import sys
import dlib
import threading
import argparse
import queue
from imutils import face_utils


class color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    WHITE = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def crop_boundary(top, bottom, left, right, faces):
    if faces:
        top = max(0, top - 300)
        left = max(0, left - 300)
        right += 300
        bottom += 300
    else:
        top = max(0, top - 50)
        left = max(0, left - 50)
        right += 50
        bottom += 50

    return (top, bottom, left, right)


def crop_face(imgpath, dirName):
    frame = cv2.imread(imgpath)
    basename = os.path.basename(imgpath)
    basename_without_ext = os.path.splitext(basename)[0]
    extName = os.path.splitext(basename)[1]
    if frame is None:
        return print(f"{color.RED}Invalid file path{color.END}: [{imgpath}]")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_detect = dlib.get_frontal_face_detector()
    rects = face_detect(gray, 1)
    if not len(rects):
        return print(f"{color.RED}Sorry{color.END}. HOG could not detect any faces from your image.\n[{imgpath}]")
    for i, rect in enumerate(rects):
        (x, y, w, h) = face_utils.rect_to_bb(rect)

        top, bottom, left, right = crop_boundary(y, y + h, x, x + w, len(rects) <= 2)
        crop_img_path = os.path.join(dirName, f"{basename_without_ext}_crop_{i}{extName}")
        crop_img = frame[top:bottom, left:right]
        cv2.imwrite(crop_img_path, cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR))
    return print(f"{color.GREEN}SUCCESS{color.END}: [{basename}]")


def worker(run_event, q, output):
    while run_event.is_set():
        try:
            item = q.get(block=False)
        except queue.Empty:
            break
        crop_face(item, output)
        q.task_done()


def main(args):
    os.makedirs(args.output, exist_ok=True)
    q = queue.Queue()
    for imgpath in args.image:
        if os.path.isdir(imgpath):
            for img in os.listdir(imgpath):
                img = os.path.join(imgpath, img)
                if os.path.isfile(img):
                    q.put(img)
        else:
            q.put(imgpath)

    run_event = threading.Event()
    run_event.set()
    for i in range(args.thread):
        t = threading.Thread(target=worker, args=(run_event, q, args.output))
        t.start()

    try:
        q.join()
    except KeyboardInterrupt:
        print(f"{color.RED}Keyboard Interrupt{color.END}: Terminating all threads and exit.")
        run_event.clear()
        sys.exit(1)

    return print(f"{color.GREEN}DONE{color.END}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto crop faces from images.")
    parser.add_argument("-t", "--thread", type=int, default=1, help="number of threads (default: 1)")
    parser.add_argument("-o", "--output", type=str, default="result", help="output directory (default: result)")
    parser.add_argument("image", nargs="+", help="image file or directory path")
    args = parser.parse_args()

    main(args)
