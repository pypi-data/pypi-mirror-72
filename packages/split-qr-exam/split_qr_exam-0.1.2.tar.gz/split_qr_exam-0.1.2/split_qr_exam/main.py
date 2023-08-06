#!/usr/bin/env python3

"""
split_qr_exam
=============

This script splits a pdf composed of scanned exams. The input is a pdf file containing multiple
scanned exames. On each exam cover there should be a QR code identifying the student writing this
exam.
For each part of the exam a folder will be created and for each student a pdf will be created in
that folder to allow for parallel evaluation. To ensure pseudonymity the files are named with the
sha256 hash of the student id.

For this to work, you have to specify all the parts of the exam with the corresponding amount of
pages.
"""

import sys
import os
import logging
import math
import argparse
import hashlib

import numpy as np

import fitz
import cv2

#def show_img(img):
#    cv2.imshow("image", img)
#    cv2.waitKey(3000)
#    cv2.destroyAllWindows()

class NoQRCodeFoundException(Exception):
    """Exception thrown if no QR code is found on a page.

    Should only be thrown, if multiple attempts at multiple thresholds were attempted."""

class NoCoverFoundException(Exception):
    """Exception thrown if no page with a QR code is found.

    Should only be thrown, if all pages of an exam are tested."""

class QRScanner:
    """Class that handles the scanning of QR codes

    Intended use is creating an instance of the class once, and using it to process all neccessary
    images.

    Attributes:
        threshold: A value between 0 and 255, indicating what amount of grey will be interpreted
                   as black or white. Higher values lead to more black, lower values lead to more
                   white. No threshold will be applied, if the value is None.
        shrink: Shinks the image to this width in the detection phase.
        crop: A tuple of fraction coordinates, representing the area to crop the image to before
              scanning for QR codes. The first element represents the upper left corner of the area
              the second element represents the lower right corner.
              E.g.: ((0,0),(0.5,0.5)) would take the top left quartal of the image,
                    ((0,0.5),(0,1)) would take the left half of the image,
                    ((0.25,0.25), (0.75, 0.75)) would take the center of the image.
              If any value is greater than 1 or less than 0, it will be set to 1 or 0 respectively.

    Example use:
        qr_scanner = QRScanner(127, 600)
        try:
            qr_string = qr_scanner.get_qr_string(image)
            print(qr_string)
        except NoQRCodeFoundException:
            print("Could not find any QR codes :(")
    """

    def __init__(self, threshold, shrink, crop):
        """Initializes all attributes of the object"""

        self.threshold = threshold
        if self.threshold is not None and self.threshold > 255:
            logging.warning("Threshold above 255, setting to 255")
            self.threshold = 255
        elif self.threshold is not None and self.threshold < 0:
            logging.warning("Threshold below 0, setting to 0")
            self.threshold = 0
        self.shrink = shrink
        self._qr_instance = cv2.QRCodeDetector()
        if crop is not None:
            if crop[0][0] > 1:
                crop[0][0] = 1
            if crop[0][0] < 0:
                crop[0][0] = 0
            if crop[0][1] > 1:
                crop[0][1] = 1
            if crop[0][1] < 0:
                crop[0][1] = 0
            if crop[1][0] > 1:
                crop[1][0] = 1
            if crop[1][0] < 0:
                crop[1][0] = 0
            if crop[1][1] > 1:
                crop[1][1] = 1
            if crop[1][1] < 0:
                crop[1][1] = 0
        self.crop = crop

    def get_qr_string(self, image):
        """Decodes a QR code on page `pagenr` and returns the string.

        Args:
            image: The image to extract the string from.

        The image is first cropped, shrunk down and cleaned up, to improve performance and accuracy.
        If no code can be found after using these two operations, a second attempt is made for each
        threshold between 0 and 255, but not shrinking down the image.

        Returns:
            The string encoded in the QR code in the image

        Raises:
            NoQRCodeFoundException: If no QR code can be found
        """

        cropped_image = self.crop_image(image)
        qr_coordinates = self.detect_qr_code(cropped_image)
        if qr_coordinates is None:
            qr_coordinates = self.detect_qr_code_slow(cropped_image)
            if qr_coordinates is None:
                raise NoQRCodeFoundException()
        return self.decode_qr_code(cropped_image, qr_coordinates)

    def crop_image(self, image):
        """Croppes the image

        This operation does not create a new image. It returns a slice view of the original image.
        Relevant attributes for this method are: self.crop

        Args:
            image: The image to slice

        Returns:
            A cropped portion of the image. Or the original image, if self.crop is None.
        """

        if self.crop is None:
            return image
        width, height, _ = image.shape
        x_start, new_width = int(self.crop[0][0] * width), int(self.crop[1][0] * width)
        y_start, new_height = int(self.crop[0][1] * height), int(self.crop[1][1] * height)
        return image[x_start:new_width, y_start:new_height]

    def shrink_image(self, image):
        """Resizes an image to a width of `self.shrink`

        This function creates a new, resized image with width `self.shrink`. This operation
        preserves the aspect ratio of the input image.

        Args:
            image: The image to shrink

        Returns:
            A tuple consisting of
              * The input image shrunk to the width of `self.shrink`
              * The floating point scaling factor used to shrink the image
        """

        factor = image.shape[0] / self.shrink
        returns = cv2.resize(image, None, fx=(1/factor), fy=(1/factor)), factor
        return returns


    def clean_up(self, image, overwrite_threshold=None):
        """Cleans up a greyscale image by removing the grey parts

        The higher the threshold, the more grey is interpreted as black. The lower the threshold,
        the more grey is interpreted as white.

        Args:
            image: The image to clean up
            overwrite_threshold: If set, use this value instead of `self.threshold`.

        Returns:
            A new monochrome image.
        """

        threshold = self.threshold if overwrite_threshold is None else overwrite_threshold

        return cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    def detect_qr_code(self, image, no_shrink=False, overwrite_threshold=None):
        """Finds the location of a QR code in an image using an optimized method.

        First a shrinking operation is performed. Since the mere detection of a QR code does not
        need all the details of the image, this operation does not impact the accuracy of the
        detection severly, but helps greatly to improve the performance.
        Then a clean up operation is performed. This converts the greyscale input image to a black
        and white image, thereby cleaning up the QR code and improve the accuracy of the scan.

        Args:
            image: The image to process
            no_shrink: If True, skips the shrinking operation
            overwrite_threshold: If set, uses this value instead of `self.threshold` in the
                                 clean_up phase

        Returns:
            A numpy float array of coordinates if a QR code is found, otherwise it returns None.
            If more than one QR code is found... that would be undefined behaviour.
        """

        mini_image, factor = self.shrink_image(image) \
            if self.shrink is not None and not no_shrink else (image, 1)
        mini_cleaned_up = self.clean_up(
            mini_image, overwrite_threshold=overwrite_threshold
        ) if self.threshold is not None else image
        found, coordinates = self._qr_instance.detect(mini_cleaned_up)
        if not found:
            return None
        return coordinates * factor

    def detect_qr_code_slow(self, image):
        """Finds a QR code in in an image

        This should only be called, if a call to `detect_qr_code` was unsuccessful.

        Instead of shrinking and cleaning the image up, this method only tries to clean the image
        up, thereby maximizing the accuracy. Also, instead of only using a fix threshold, all
        possible thresholds, starting with `self.threshold` will be tried, until one run yields a
        result.

        Args:
            image: The image to detect a QR code in


        Returns:
            A numpy float array of coordinates if a QR code is found, otherwise it returns None.
        """

        thresh = self.threshold
        coordinates = None
        while coordinates is None:
            coordinates = self.detect_qr_code(image, no_shrink=True, overwrite_threshold=thresh)
            thresh += 1
            if thresh == 256:
                thresh = 0
            if thresh == self.threshold - 1:
                return None
        return coordinates


    def decode_qr_code(self, image, coordinates):
        """Given an image and the coordinates of a QR code, returns the string of the QR code.

        Args:
            image: An image with a QR code
            coordinates: Coordinates found with `self.detect_qr_code()` or
                         `self.detect_qr_code_slow()`

        Returns:
            The string encoded in the QR code, or an empty string, if no string could be decoded.
        """

        return self._qr_instance.decode(image, coordinates)[0]



class QRKlausurProcessor:
    """Processeses one single pdf file containing all the scanned exams.

    For each student, a folder is created containing a pdf file for each
    part defined. A student is identified by a QR code in the top left
    part of the cover sheet.

    If a student cannot be identified, the exam will be placed in a seperate folder
    and a warning will be issued. This exam needs to be processed manually.

    Some errors, that can occur in the scanning process will be fixed however. If
    an exam has fewer pages than defined, because the scanner skipped a page for some reason,
    the rest of the exams wont be aligned to the total number of pages per exam. In such a case
    an offset is calculated going forward and the problematic exam will be put in a seperate folder
    for manual processing.

    Attributes:
        pdf_file: A pymupdf-object, containing all the exams in sequence
        destpath: The output folder. If it does not exist, it will be created.
        parts: A list of tupels describing the parts of the exam together
               with the first and last page of the part. E.g.
               [("Cover", 0, 2), ("Task 1", 2, 4), ("Bonuspage_1", 4, 6), ("Bonuspage_2", 6, 8)]
        qr_scanner: An instance of `QRScanner`
    """

    def __init__(self, filename, destpath, parts, qr_scanner):
        """Initializes the object.

        Opens the file `filename` as a pymupdf-object. If the number of pages in the input document
        is not divisible by the number of pages per exam (given by the `parts` list), a warning is
        issued. Manual intervention may be needed.

        Args:
            filename: The name of the file to open
            destpath: see corresponding Attribute
            parts: see corresponding Attribute
            qr_scanner: see corresponding Attribute

        Raises:
            RuntimeError, if filename does not exist or is not readable
        """
        self.qr_scanner = qr_scanner
        self.pdf_file = fitz.open(filename)
        self.destpath = destpath
        self._offset = 0
        self._old_string = None

        self.parts = parts
        self._nrpages = self.parts[-1][2] + 1
        if self.pdf_file.pageCount % self._nrpages:
            logging.warning(
                "Number of pages of the scan is not divisible by the number of pages of the exam"
            )


    def process_exams(self):
        """Processes all exams in order"""

        for examnr in range(math.ceil(self.pdf_file.pageCount / self._nrpages)):
            try:
                while not self.process_exam(examnr):
                    pass
            except NoCoverFoundException:
                logging.error("Could not find cover for exam %d, giving up.", examnr)


    def process_exam(self, examnr):
        """Processes a single exam.

        Its QR code is decoded and all parts will be splitted. The resulting parts are stored in
        folders for each part, named after the sha256sum of the student id to ensure pseudonymity.

        If the scanned exam includes the backsides, all parts (except the cover) will also contain
        the backside of the last page of the last part, meaning this page will occur in more than
        one pdf.

        If the last part consist of bonus pages, each of this pages will be a seperate pdf file.

        The page number of the cover page is computed by multiplying the `examnr` with the number
        of pages per exam. If no QR code is found at the cover page, a warning is issued. All pages
        up to and excluding the last cover page will be scanned for QR codes. If such a code is
        found, it will be assumed, that the previos exam has missing pages. Going forward the page
        numbers of the cover pages will be computed with an offset.

        Args:
            examnr: The running number of the exam

        Returns:
            True, if a code was Found on the first + self._offset page of the exam
            False, if no code was found

        Raises:
            NoCoverFoundException: If the offset matches the length of the exam, it is assumed,
                                   that there is no valid cover for this exam, and this exception
                                   is raised.
        """

        first_page = examnr * self._nrpages + self._offset
        try:
            image = self.get_image_for_page(first_page)
            student_id = self.qr_scanner.get_qr_string(image)
            self._old_string = student_id
            print(f"Exam number {examnr}, studentid: {student_id}")
            #student_path = os.path.join(self.destpath, student_id)
            for part_name, part_start, part_end in self.parts:
                part_folder = os.path.join(self.destpath, part_name)
                hash_id = hashlib.sha256(bytes(student_id, encoding='utf8')).hexdigest()
                os.makedirs(part_folder, exist_ok=True)
                part_path = os.path.join(part_folder, f"{hash_id}_{part_name}.pdf")
                print(f"{part_path} - {part_start}:{part_end}")

                part_pdf = fitz.open()
                part_pdf.insertPDF(self.pdf_file
                                   , from_page=first_page + part_start
                                   , to_page=first_page + part_end)
                part_pdf.save(part_path)
            return True

        except NoQRCodeFoundException:
            if examnr == 0:
                logging.warning("No QR code found on page %d. Skipping pages, until we find a "
                                "scannable cover page", first_page)
                if self._offset == self._nrpages:
                    self._offset = 0
                    raise NoCoverFoundException()
                self._offset += 1
            else:
                logging.warning("No QR code found on page %d. This may be due to an inconsistent "
                                "number of pages from a previous scan. Please check exam %d (%s) "
                                "manually.",
                                first_page, (examnr - 1), self._old_string)
                if self._offset == -self._nrpages:
                    self._offset = 0
                    raise NoCoverFoundException()
                self._offset -= 1
            return False



    def get_image_for_page(self, pagenr):
        """Renders the page `pagenr` and returns a numpy array containing the imagedata"""

        #images = self.pdf_file.getPageImageList(pagenr)
        #print(images)
        #if len(images) == 0:
        #    raise RuntimeError(f"Could not find an image on page {pagenr}")
        #if len(images) > 1:
        #    raise RuntimeError(f"Multiple images on page {pagenr}")
        #pix = fitz.Pixmap(self.pdf_file, images[0][0])
        pix = self.pdf_file[pagenr].getPixmap()
        image = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
        return np.ascontiguousarray(image[..., [2, 1, 0]])  # rgb to bgr

def create_parts(part_strings, is_double_sided, last_part_is_bonus):
    """Takes a list of parts with lengths encoded in a string and creates a list of tupels with
    start and end page"""

    part_lengths = [(part[0], int(part[1])) for part in [part.split(":") for part in part_strings]]
    if last_part_is_bonus:
        bonus_parts = \
            [(part_lengths[-1][0] + "_" + str(page), 1) for page in range(part_lengths[-1][1])]
        part_lengths = part_lengths[:-1] + bonus_parts
    parts = []
    part_start = 0
    for part_name, part_length in part_lengths:
        part_end = part_start + (part_length - 1)

        if is_double_sided:
            part_end += part_length
            if part_start != 0:
                part_start -= 1
        parts += [(part_name, part_start, part_end)]
        part_start = part_end + 1
    return parts

def parse_cropping(crop_string, no_crop):
    """Parses a string formatted like "x1,y1:x2,y2" into the tuple ((x1,y1), (x2,y2))
    where x1, x2, y1, y2 are floating point numbers."""

    if no_crop:
        return None
    coord_x, coord_y = crop_string.split(":")
    start_x, end_x = coord_x.split(",")
    start_y, end_y = coord_y.split(",")
    return ((float(start_x), float(end_x)), (float(start_y), float(end_y)))

def run(filename, destpath, parts, config):
    """The main function. Given all neccessary parameters, processes every exam in the pdf"""

    qr_scanner = QRScanner(**config)
    qr_klausur_processor = QRKlausurProcessor(filename, destpath, parts, qr_scanner)
    qr_klausur_processor.process_exams()

def main():
    """Parses the arguments and calls run"""

    parser = argparse.ArgumentParser(
        description="Split a scanned examfile into folders for each student and tasks in "
                    "seperate pdf files. The input PDF should have a QR code identifying the "
                    "student on the cover of each exam."
        , epilog=f"Example of use:\n\t{sys.argv[0]} -p cover:1 -p task1:2 -p task2:3 "
                 "-p task3:1 -p bonus:3 -b -d scanned_exams.pdf ~/splitexams/\n"
        , formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-t", "--threshold", type=int, default=127,
                        help="Set the threshold for the cleanup phase. Values range from 0 to "
                             "255. Lower value means more grey is detected as white, higher "
                             "value means more grey is detected as black. Only impacts the QR "
                             "detection phase. Default: 127")
    parser.add_argument("-s", "--shrink", type=int, default=600,
                        help="Width of the image in pixel for the QR code detection phase. "
                             "Lower value means more performance, higher value means more "
                             "accuracy. Only impacts the QR detection phase, does not affect "
                             "the output PDF. Default: 600")
    parser.add_argument("-c", "--crop", default="0,0.5:0.5,1",
                        help="Fractional coordinates, that represent the area of the coverpage, "
                             "where the QR code is located. The format is \"x1,y1:x2,y2\" where "
                             "x1, x2, y1, y2 are values from 0 to 1. "
                             "Default is \"0,0.5:0.5,1\" which corresponds to the top right "
                             "quartal of the image.")
    parser.add_argument("-T", "--no-cleanup", action="store_true", help="Skip cleanup phase")
    parser.add_argument("-S", "--no-shrink", action="store_true", help="Skip shrinking phase")
    parser.add_argument("-C", "--no-crop", action="store_true", help="Skip cropping phase")
    parser.add_argument("-p", "--part", required=True, action="append",
                        help="Name and amount of pages for the parts of the exam, seperated by "
                             "a colon. Can (and should) be issued multiple times (Example \"-p "
                             "Cover:1 -p Task1:2\"). Should also include a part for the cover "
                             "sheet, and empty bonus sheets. The number of pages should not "
                             "include the backsides, if the document is scanned in duplex. Use "
                             "--is-double-sided instead")
    parser.add_argument("-d", "--is-double-sided", action="store_true", help="The exam is "
                        "scanned in duplex. The split output pdf will also include the last "
                        "backside of the previous part, since students tend to also write "
                        "solutions there")
    parser.add_argument("-b", "--last-part-is-bonus", action="store_true",
                        help="The last part are bonus sheets. There will be a seperate pdf for "
                             "each bonus sheet.")
    parser.add_argument("pdf", help="The pdf file to split")
    parser.add_argument("dest", default=".", help="Destination folder. Default is the current "
                        "directory", nargs='?')

    args = parser.parse_args()
    if args.no_shrink:
        args.shrink = None
    if args.no_cleanup:
        args.thresh = None

    args_parts = create_parts(args.part, args.is_double_sided, args.last_part_is_bonus)
    config = {"shrink": args.shrink,
              "crop": parse_cropping(args.crop, args.no_crop),
              "threshold": args.threshold}


    run(args.pdf, args.dest, args_parts, config)

if __name__ == "__main__":
    main()
