import csv
import os
import time

import cv2 as cv
import pandas as pd
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from skimage.metrics import structural_similarity

import imutils


class WatchUI:
    """WatchUI - Custom library for comparing images with use in Robot Framework.

    = Table of Contents =

    - `Usage`
    - `Importing`
    - `Examples`
    - `Keywords`

    = Usage =

    This library allows for automated visual testing of web frontends.
    Currently, this library is not officialy supported, so best way is to
    clone the repository and copy the WatchUI.py library file into your project and then
    import it - see Importing section.

    However, you can also install it via command *pip install WatchUI* and then import it.

    *IMPORTANT*: When using keywords of this library, please remember, that screenshots have to have same resolution!

    = Examples =
    Import library
    | `Library` | <path_to_library file> | outputs_folder= | ssim_basic= |

    Compare Images
    | Compare Images | path1 | path2 | save_folder= | ssim= |

    """

    save_folder_path = "../Outputs"
    starts_ssim = 1.0
    starts_format_image = "png"

    def __init__(self, outputs_folder=save_folder_path, ssim_basic=starts_ssim, format_image=starts_format_image):
        """Library can be imported either with default output folder and set lowest limit of difference between images (ssim), or
        you can provide your own values.

        Keyword Arguments:

            outputs_folder {str} -- path, where you want to save images with highlighted differences (default: "../Outputs")

            ssim_basic {float} -- threshold value in the interval (0, 1>. Tests are passed, if ssim value returned by keyword test functions is bigger than this (default: 1.0)

            format_image {str} -- Format for saving picture/screenshot (png, jpg etc.) Example: format_image=jpg (default: png)

        Examples:

        | =Setting= | =Value= | =Value= | =Value= | =Comment= |
        | Library   | WatchUI.py |      |  | # Uses default values of keyword arguments |
        | Library   | WatchUI.py | outputs_folder=<path_to_folder> | | # changes folder to different one |
        | Library   | WatchUI.py | outputs_folder=<path_to_folder> | ssim_basic=<float> | # changes output folder and ssim threshold |

        """
        self.outputs_folder = outputs_folder
        self.ssim_basic = float(ssim_basic)
        self.image_format = str(format_image)
        # when libdoc builds documentation, this would lead to exception, since robot cannot access execution context,
        # since nothing really executes
        try:
            self.seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
            self.robotlib = BuiltIn().get_library_instance("BuiltIn")
        except RobotNotRunningError as e:
            print(
                f"If you are trying to build documentation, than this exception is just nuisance, skipping...\n{str(e)}"
            )
            pass
        self.score = None
        self.cnts = None
        self.img1 = None
        self.img2 = None

    def _check_dir(self, save_folder):
        """Checks, if given <save_folder> exists, if not, creates it.

        Arguments:
            save_folder {str} -- path to <save_folder>
        """
        if save_folder != self.save_folder_path:
            if os.path.exists(save_folder):
                self.save_folder = save_folder
            else:
                os.mkdir(save_folder)
                self.save_folder = save_folder
        else:
            if os.path.exists(self.outputs_folder):
                self.save_folder = self.outputs_folder
            else:
                os.mkdir(self.outputs_folder)
                self.save_folder = self.outputs_folder

    def _check_ssim(self, ssim):
        """Checks, if ssim equals default, returns ssim value.

        Arguments:
            ssim {float} -- provided ssim value

        Returns:
            self.ssim {float} -- ssim value as instance attribute
        """
        if ssim == 1.0:
            self.ssim = float(self.ssim_basic)
        else:
            self.ssim = float(ssim)

    def _check_image_format(self, format):
        """Checks, which format setup for saving picture.

        Arguments:
            format_image {str} -- Image format as png, jpg etc.

        Returns:
            self.format {float} -- format for setup image type
        """
        if str(format) == 'png':
            self.format = '.' + self.image_format
        else:
            self.format = '.' + format

    def _compare_images(self, path1, path2):
        """Compares two images.

        Arguments:
            path1 { str } -- filepath to image 1
            path2 { str } -- filepath to image 2
        """
        self.img1 = cv.imread(path1, 1)
        self.img2 = cv.imread(path2, 1)

        # convert to grey
        gray_img1 = cv.cvtColor(self.img1, cv.COLOR_BGR2GRAY)
        gray_img2 = cv.cvtColor(self.img2, cv.COLOR_BGR2GRAY)

        # SSIM diff Img
        (self.score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
        diff = (diff * 255).astype("uint8")

        # Threshold diff Img
        thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(cnts)

    def compare_images(
            self, path1, path2, save_folder=save_folder_path, ssim=starts_ssim, image_format=starts_format_image
    ):
        """Comparing images

        It compares two images from the two paths and, if there are differences, saves the image with the errors highlighted
        in the folder: ../Save Image

        path1 = path to the first image to be compared
        path2 = path to the second image to be compared

        Example: Compare two image ../image1.png ../Image2.png
        """
        self._check_dir(save_folder)
        self._check_ssim(ssim)
        self._check_image_format(image_format)

        if os.path.exists(path1) and os.path.exists(path2):
            # Compare image
            self._compare_images(path1, path2)

            # Create frame in diff area
            for c in self.cnts:
                (x, y, w, h) = cv.boundingRect(c)
                cv.rectangle(self.img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.rectangle(self.img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Show image

            if float(self.score) < self.ssim:
                self.robotlib.log_to_console(self.ssim)
                self.robotlib.log_to_console(self.score)
                cv.imwrite(
                    self.save_folder + "/Img" + str(time.time()) + self.format, self.img2
                )
                self.robotlib.fail("*INFO* Save file with difference")
            else:
                img_diff = cv.hconcat([self.img1, self.img2])
                time_ = str(time.time())
                self.seleniumlib.capture_page_screenshot(
                    save_folder + "/Img" + time_ + self.format
                )
                cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                self.robotlib.log_to_console(
                    "Image has diff: {} ".format(self.score)
                )
        else:
            raise AssertionError("Path doesnt exists")

    def compare_screen(self, path1, save_folder=save_folder_path, ssim=starts_ssim, image_format=starts_format_image):
        """	Compare the already save image with the browser screen

        Compares the already saved image with the screen that is on the screen. If there is a difference, it saves the
        highlighted image to the: ../Save Image

        path1 = path to the image to be compared to screen

        Example: Compare screen ../image1.png
        """
        self._check_dir(save_folder)
        self._check_ssim(float(ssim))
        self._check_image_format(image_format)
        save_folder = self.save_folder
        self.seleniumlib.capture_page_screenshot(save_folder + "/testscreen.png")
        path2 = save_folder + "/testscreen.png"
        if os.path.exists(path1):
            if os.path.exists(path2):
                # Compare image
                self._compare_images(path1, path2)

                # Create frame in diff area
                for c in self.cnts:
                    (x, y, w, h) = cv.boundingRect(c)
                    cv.rectangle(self.img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv.rectangle(self.img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # Show image

                self.robotlib.log_to_console(self.ssim)
                if float(self.score) < self.ssim:
                    self.robotlib.log_to_console(self.ssim)
                    img_diff = cv.hconcat([self.img1, self.img2])
                    time_ = str(time.time())
                    score_percen = float(self.score) * 100
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img" + time_ + self.format
                    )
                    cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                    self.robotlib.fail("Image has diff: {} %".format(score_percen))
                else:
                    img_diff = cv.hconcat([self.img1, self.img2])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img" + time_ + self.format
                    )
                    cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                    self.robotlib.log_to_console(
                        "Image has diff: {} ".format(self.score)
                    )
            else:
                raise AssertionError("Path2 doesnt found:" + path2)
        else:
            raise AssertionError("Path1 doesnt found" + path1)
        if os.path.exists(save_folder + "/testscreen.png"):
            os.remove(save_folder + "/testscreen.png")

    def create_area(
            self, x1, y1, x2, y2, save_folder=save_folder_path, screen_name="screen", image_format=starts_format_image
    ):
        """  Creates a cut-out from the screen

        Creates a cut-out from the screen that is on screen and saves it in the folder: ../Create area

        x1 a y1 = x and y coordinates for the upper left corner of the square
        x2 and y2 = x and y coordinates for the bottom right corner of the square

        Example: Compare making area 0 0 25 25
        """
        self._check_dir(save_folder)
        save_folder = self.save_folder
        self._check_image_format(image_format)

        self.seleniumlib.capture_page_screenshot(save_folder + '/testscreen.png')
        img = save_folder + '/testscreen.png'
        img_crop = cv.imread(img)
        crop_img = img_crop[
                   int(x1): int(y2), int(y1): int(x2)
                   ]  # Crop from {x, y, w, h } => {0, 0, 300, 400}
        if screen_name == "screen":
            cv.imwrite(save_folder + '/screen' + str(time.time()) + self.format, crop_img)
        else:
            cv.imwrite(save_folder + '/' + screen_name + self.format, crop_img)

    def create_screens(
            self, *resolution, save_folder=save_folder_path, screen_name="screen", image_format=starts_format_image
    ):
        """ Creates a screenshot on the screen

        Creates a screenshot on the screen, that corresponds to the specified resolution, so it is possible to create on one
        page an infinite number of screens with different resolutions.
        Screens are stored in the folder: ../Create rescreens

        *resolutin = The specified resolution in width and height format, you can enter as many as needed

        Warning: When you create one screen, name will be screen.png, but when you create more than one screen from same 4
        page, name will be screen screen_name_width_height.png

        Example: compare making rescreens 800 600 1280 800 1440 900 Creates 3 screens in 800x600 1280x800 and 1440x90
        """
        self._check_dir(save_folder)
        save_folder = self.save_folder
        self._check_image_format(image_format)

        leng_reso = len(resolution)
        if leng_reso % 2 == 0:
            if (leng_reso / 2) == 1:
                self.seleniumlib.set_window_size(int(resolution[0]), int(resolution[1]))
                time.sleep(1)
                self.seleniumlib.capture_page_screenshot(
                    save_folder
                    + "/"
                    + screen_name
                    + self.format
                )
            else:
                x = leng_reso / 2
                i = 0
                a = 0
                while i < x:
                    width = int(resolution[0 + a])
                    height = int(resolution[1 + a])
                    self.seleniumlib.set_window_size(width, height)
                    time.sleep(1)
                    self.seleniumlib.capture_page_screenshot(
                        save_folder
                        + "/"
                        + screen_name
                        + str(width)
                        + "x"
                        + str(height)
                        + self.format
                    )
                    a += 2
                    i += 1
        else:
            raise AssertionError("Bad numbers of resolution")

    def compare_screen_areas(
            self, x1, y1, x2, y2, path1, save_folder=save_folder_path, ssim=starts_ssim, image_format=starts_format_image
    ):
        """Creates a cut-out from the screen

        Creates a cut-out from the screen that is on the screen and compares it to a previously created

        x1 and y1 = x and y coordinates for the upper left corner of the square
        x2 and y2 = x and y coordinates for the bottom right corner of the square
        path1 = Path to an already created viewport with which we want to compare the viewport created by us

        Example: Compare screen area 0 0 25 25 ../Crop_Image1.png Creates Crop_Image1.png from 0, 0, 25, 25
        """
        self._check_dir(save_folder)
        self._check_ssim(ssim)
        self._check_image_format(image_format)
        save_folder = self.save_folder
        self.seleniumlib.capture_page_screenshot(save_folder + '/test1.png')
        path2 = save_folder + '/test1.png'

        if os.path.exists(path1):
            if os.path.exists(path2):
                # load img
                img1 = cv.imread(path1, 1)  # img from docu
                img2 = cv.imread(path2, 1)  # img from screenshot

                # convert to grey
                gray_img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                gray_img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

                # spliting area
                crop_img = gray_img2[
                           int(x1): int(y2), int(y1): int(x2)
                           ]  # Crop from {x, y, w, h } => {0, 0, 300, 400}

                # SSIM diff img
                (self.score, diff) = structural_similarity(
                    gray_img1, crop_img, full=True
                )
                diff = (diff * 255).astype('uint8')

                # Threshold diff img
                thresh = cv.threshold(
                    diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU
                )[1]
                cnts = cv.findContours(
                    thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
                )
                cnts = imutils.grab_contours(cnts)

                crop_img_color = img2[int(x1): int(y2), int(y1): int(x2)]
                # Create frame in diff area
                for c in cnts:
                    (x, y, w, h) = cv.boundingRect(c)
                    cv.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv.rectangle(crop_img_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Show image
                if float(self.score) < self.ssim:
                    self.robotlib = BuiltIn().get_library_instance('BuiltIn')
                    img_diff = cv.hconcat([img1, crop_img_color])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + '/img' + time_ + '.png'
                    )
                    cv.imwrite(save_folder + '/img' + time_ + self.format, img_diff)
                    self.robotlib.fail('Image has diff: {} '.format(self.score))
                    score_percen = float(self.score) * +100
                    self.robotlib.fail('Image has diff: {} %'.format(score_percen))
                else:
                    img_diff = cv.hconcat([self.img1, self.img2])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img" + time_ + self.format
                    )
                    cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                    self.robotlib.log_to_console(
                        "Image has diff: {} ".format(self.score)
                    )
            else:
                raise AssertionError("New screen doesnt exist anymore")
        else:
            raise AssertionError("You put bad path")
        if os.path.exists(save_folder + '/test1.png'):
            os.remove(save_folder + '/test1.png')

    def compare_screen_without_areas(
            self, path1, *args, save_folder=save_folder_path, ssim=starts_ssim, image_format=starts_format_image
    ):
        """
        Compares two pictures, which have parts to be ignored
        x1 and y1 = x and y coordinates for the upper left corner of the ignored area square
        x2 and y2 = x and y coordinates for the lower right corner of the square of the ignored part

        Attention! It is always necessary to enter in order x1 y1 x2 y2 x1 y1 x2 y2 etc ...

        Compare screen without areas ../Image1.png 0 0 30 40 50 50 100 100
        Creates 2 ignored parts at 0,0, 30,40 and 50, 50, 100, 100
        """
        self._check_dir(save_folder)
        self._check_ssim(ssim)
        self._check_image_format(image_format)
        save_folder = self.save_folder

        self.seleniumlib.capture_page_screenshot(save_folder + "/test1.png")
        path2 = save_folder + "/test1.png"
        if os.path.exists(path1) and os.path.exists(path2):
            lt = len(args)
            img1 = cv.imread(path1, 1)
            img2 = cv.imread(path2, 1)
            if lt % 4 == 0:
                x = lt / 4
                self.robotlib.log_to_console(x)
                i = 0
                a = 0
                while i < x:
                    color = (0, 0, 0)
                    x1 = int(args[0 + a])
                    y1 = int(args[1 + a])
                    x2 = int(args[2 + a])
                    y2 = int(args[3 + a])

                    cv.rectangle(img1, (x1, y1), (x2, y2), color, -1)
                    cv.rectangle(img2, (x1, y1), (x2, y2), color, -1)
                    a += 4
                    i += 1
                cv.namedWindow("image", cv.WINDOW_NORMAL)

                # convert to grey
                gray_img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                gray_img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

                # SSIM diff Img
                (self.score, diff) = structural_similarity(
                    gray_img1, gray_img2, full=True
                )
                diff = (diff * 255).astype("uint8")

                # Threshold diff Img
                thresh = cv.threshold(
                    diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU
                )[1]
                cnts = cv.findContours(
                    thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
                )
                cnts = imutils.grab_contours(cnts)

                # Create frame in diff area
                for c in cnts:
                    (x, y, w, h) = cv.boundingRect(c)
                    cv.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Show image
                if float(self.score) < self.ssim:
                    img_diff = cv.hconcat([img1, img2])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img" + time_ + self.format
                    )
                    cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                    self.robotlib.fail("Image has diff: {} ".format(self.score))
                else:
                    img_diff = cv.hconcat([img1, img2])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img" + time_ + self.format
                    )
                    cv.imwrite(save_folder + "/Img" + time_ + self.format, img_diff)
                    self.robotlib.log_to_console(
                        "Image has diff: {} ".format(self.score)
                    )
        else:
            raise AssertionError("Path doesnt exists")

    def compare_screen_get_information(
            self,
            path1,
            save_folder=save_folder_path,
            folder_csv="../CSV_ERROR",
            ssim=starts_ssim,
            image_format=starts_format_image
    ):
        """	Compare the already save image with the browser screen

        Compares the already saved image with the screen that is on the screen. If there is a difference, it saves the
        highlighted image to the: ../Save Image and making csv file with coordinates and elements which exist on this
        coordinates

        path1 = path to the image to be compared to screen

        Example: Compare screen ../image1.png
        """
        self._check_dir(save_folder)
        self._check_dir(folder_csv)
        self._check_ssim(ssim)
        self._check_image_format(image_format)
        save_folder = self.save_folder
        # Making screen
        self.seleniumlib.capture_page_screenshot(save_folder + "/test1.png")
        path2 = save_folder + "/test1.png"
        if os.path.exists(path1):
            if os.path.exists(path2):
                # load Img
                self._compare_images(path1, path2)

                # write coordinate
                with open(folder_csv + "/bug_coordinates.csv", "w") as csvfile:
                    writer = csv.writer(csvfile)
                    a = "path", "x_center", "y_center", "x", "y", "x1", "y1"
                    writer.writerow(a)

                    # Create frame in diff area
                    for c in self.cnts:
                        (x, y, w, h) = cv.boundingRect(c)
                        cv.rectangle(self.img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv.rectangle(self.img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        x2 = x + w
                        y2 = y + h
                        x_center = x + ((x2 - x) / 2)
                        y_center = y + ((y2 - y) / 2)
                        f = path1, x_center, y_center, x, y, x2, y2
                        writer.writerow(f)

                # Save image and show report
                if float(self.score) < self.ssim:
                    img_diff = cv.hconcat([self.img1, self.img2])
                    time_ = str(time.time())
                    self.seleniumlib.capture_page_screenshot(
                        save_folder + "/Img{0}.{1}".format(time_, self.format)
                    )
                    cv.imwrite(save_folder + "/Img{0}.{1}".format(time_, self.format), img_diff)

                    # start reading coordinates and saving element from coordinate
                    df = pd.read_csv(r"" + folder_csv + "/bug_coordinates.csv")
                    with open(
                            folder_csv + "/bug_co_and_name{0}.csv".format(str(time.time())),
                            "w",
                    ) as csv_name:
                        writer = csv.writer(csv_name)
                        a = "web-page", "x_center", "y_center", "class", "id", "name"
                        writer.writerow(a)

                        # Get information from position
                        for i in range(len(df)):
                            x_center = df.values[i, 1]
                            y_center = df.values[i, 2]
                            driver = self.seleniumlib.driver
                            elements = driver.execute_script(
                                "return document.elementsFromPoint(arguments[0], arguments[1]);",
                                x_center,
                                y_center,
                            )
                            for element in elements:
                                e_class = element.get_attribute("class")
                                e_id = element.get_attribute("id")
                                e_name = element.get_attribute("name")
                                f = path1, x_center, y_center, e_class, e_id, e_name
                                writer.writerow(f)

                    score_percen = float(self.score) * 100
                    self.robotlib.fail("Image has diff: {} %".format(score_percen))
            else:
                raise AssertionError("Bad or not exists path for picture or screen")
        else:
            raise AssertionError("Bad or not exists path for picture or screen")


