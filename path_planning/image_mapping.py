import sys, os, json, time
import pygame, cv2
import numpy as np


DIM = (720, 720)



class PathFinder():
    def __init__(self):
        pass

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)
    
    def update(self):
        self.draw_active_cell()

class ImageMapping():
    def __init__(self):
        pass
    def create_img_and_matrix(self):
        filename_orig = ['warehouse_img_with_rob.png', 'warehouse_img_with_no_rob.png']
        filename = ['warehouse_img_with_rob2.png', 'warehouse_img_with_no_rob2.png']
        filename_bin = ['warehouse_img_with_rob3.png', 'warehouse_img_with_no_rob3.png']
        bin_matrix_dict = {
            '0': [],
            '1': []
        }
        gray_matrix_dict = {
            '0': [],
            '1': []
        }
        color_matrix_dict = {
            '0': [],
            '1': []
        }
        for file_ind in range(len(filename)):
            exist = os.path.isfile(filename[file_ind])
            if not exist:
                image = cv2.imread(filename_orig[file_ind], cv2.IMREAD_UNCHANGED)
                dim = DIM
                resized_img = cv2.resize(image, dim, interpolation= cv2.INTER_AREA)
                cv2.imwrite(filename[file_ind], resized_img)
            img_color = cv2.imread(filename[file_ind], cv2.IMREAD_UNCHANGED)
            thresh = 160
            img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            img_bin = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]
            exist_bin = os.path.isfile(filename_bin[file_ind])
            if not exist_bin:
                cv2.imwrite(filename_bin[file_ind], img_bin)
            matrix_value_gray = np.zeros((img_gray.shape[0],img_gray.shape[1]))
            matrix_value_bin = np.zeros((img_bin.shape[0],img_bin.shape[1]))
            for i in range(img_gray.shape[0]):
                for j in range(img_gray.shape[1]):
                    matrix_value_gray[i][j] = img_gray[i][j]
                    bin_val = img_bin[i][j]
                    if int(bin_val) == 255:
                        #area libre
                        matrix_value_bin[i][j] = 1
                    else:
                        #area prohibida
                        matrix_value_bin[i][j] = 0
            bin_matrix_dict[str(file_ind)] = matrix_value_bin
            gray_matrix_dict[str(file_ind)] = matrix_value_gray
            color_matrix_dict[str(file_ind)] = img_color

        return (filename, bin_matrix_dict, gray_matrix_dict, color_matrix_dict)

    def compare_bin_images(self, bin_imag_1, bin_imag_2):
        compared_img = np.zeros((bin_imag_1.shape[0],bin_imag_1.shape[1]))
        if (bin_imag_1.shape[0] == bin_imag_2.shape[0]) and (bin_imag_1.shape[1] == bin_imag_2.shape[1]):
            for y in range(bin_imag_1.shape[0]):
                for x in range(bin_imag_1.shape[1]):
                    bin_imag_1_bit = bin_imag_1[y][x]
                    bin_imag_2_bit = bin_imag_2[y][x]
                    if bin_imag_1_bit == bin_imag_2_bit:
                        compared_img[y][x] = 1
                    else:
                        compared_img[y][x] = 0
            # cv2.imshow(f'compared_image',compared_img)
        else:
            print('Check if both have the same size')
        return compared_img

    def biggest_bin_section(self, orig_image_name, bin_image):
        orig_image = cv2.imread(orig_image_name)
        # cv2.imshow(f'bin_image',bin_image)
        
        invert_bin_image = (1-bin_image)
        # cv2.imshow(f'invert bin_image',invert_bin_image)

        imagen_gris = cv2.convertScaleAbs(invert_bin_image, alpha=255, beta=0)
        # cv2.imshow(f'converted gray_image',imagen_gris)
        contours, hier = cv2.findContours(imagen_gris,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours_max = max(contours, key=cv2.contourArea)
        x, y, ancho, alto = cv2.boundingRect(contours_max)
        region_interest = orig_image[y:y+alto, x:x+ancho]
        # cv2.imshow(f'mask contorno',region_interest)
        if alto>ancho:
            lado = 3*alto/2
        else:
            lado = 3*ancho/2
        centro = int(lado/2)
        lado = int(lado - 1)
        rectangle_st = [x, y, ancho, alto, centro, lado]
        
        """
        # cv2.imshow(f'cropeed bin_image',invert_bin_image[30:110][30:90])

        # columns_pixel_sum = []
        # rows_pixel_sum = []
        # for x in range(int(count_columns)):
        #     sum_per_column = 0
        #     for y in range(int(count_rows)):
        #         pixel_val = invert_bin_image[y][x]
        #         sum_per_column = sum_per_column + pixel_val
        #     columns_pixel_sum.append(sum_per_column)
        # for y in range(int(count_rows)):
        #     sum_per_row = 0
        #     for x in range(int(count_columns)):
        #         pixel_val = invert_bin_image[y][x]
        #         sum_per_row = sum_per_row + pixel_val
        #     rows_pixel_sum.append(sum_per_row)
        # start_av = True
        # final_av = True
        # columns_pixel_sum_len = len(columns_pixel_sum)
        # print(columns_pixel_sum_len)
        # rows_pixel_sum_len = len(rows_pixel_sum)
        # number_col = count_columns
        # number_row = count_rows
        # while start_av or final_av:
        #     for column_index in range(columns_pixel_sum_len):
        #         if start_av and columns_pixel_sum[column_index] != 0:
        #             print('start_av')
        #             start_av = False
        #             ind_for_start_col = column_index
        #             cropped_img = invert_bin_image[0:count_rows][column_index:number_col]
        #         elif final_av and columns_pixel_sum[column_index] != 0:
        #             print('final_av')
        #             final_av = False
        #             ind_for_final_col = number_col-column_index
        #             cropped_img = invert_bin_image[0:count_rows][0:number_col-column_index]
        #     print(count_rows, ind_for_start_col, ind_for_final_col)
        #     cropped_img = invert_bin_image[0:count_rows][ind_for_start_col:ind_for_final_col]
        #     cv2.imshow(f'cropped bin_image',cropped_img)
        """
        return (region_interest, rectangle_st)

    def main_image_to_map(self):
        file_and_matrix = self.create_img_and_matrix()
        color_images_name = file_and_matrix[0]
        image_with_rob_name = color_images_name[0]
        bin_matrix = file_and_matrix[1]
        color_image = file_and_matrix[3]
        color_image_with_rob = color_image['0']
        compared_bin_image = self.compare_bin_images(bin_matrix['0'], bin_matrix['1'])
        interest, rectangle = self.biggest_bin_section(image_with_rob_name, compared_bin_image)
        # print(color_image_with_rob.shape)
        # print(color_image_with_rob.shape[2])
        # print(color_image_with_rob[0, 0])

        return (color_image_with_rob, interest, rectangle, DIM)

# superficie = pygame.Surface(DIM)
# for fila in range(color_image_with_rob.shape[0]):
#     for columna in range(color_image_with_rob.shape[1]):
#         pixelBGR = color_image_with_rob[fila, columna]
#         color = [pixelBGR[2],pixelBGR[1],pixelBGR[0]]
#         rectangulo = pygame.Rect(columna, fila, 1, 1)
#         pygame.draw.rect(superficie, color, rectangulo)

# pygame.init()

# ventana = pygame.display.set_mode(DIM)
# pygame.display.set_caption('Grid de colores')

# ventana.blit(superficie, (0, 0))
# pygame.display.flip()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

    # cv2.imshow(f'clean image',color_image_with_rob)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# print(interest[30:40, 0:3])
# cv2.imshow(f'clean image',interest[30:40, 0:3])
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# bg_image = pygame.image.load(color_images_name[0]).convert()
# pathfinder = PathFinder()
# run = True
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         screen.blit(bg_image,(0,0))
#         pathfinder.draw_active_cell()

#         pygame.display.update()
#         clock.tick(60)





