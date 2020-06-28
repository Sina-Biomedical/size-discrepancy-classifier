# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                                                                             #
#                 _                 _                                     _                         #
#    ___    ___  | |   ___    ___  | |_           ___    ___    ___    __| |      _ __    _   _     #
#   / __|  / _ \ | |  / _ \  / __| | __|         / __|  / _ \  / _ \  / _` |     | '_ \  | | | |    #
#   \__ \ |  __/ | | |  __/ | (__  | |_          \__ \ |  __/ |  __/ | (_| |  _  | |_) | | |_| |    #
#   |___/  \___| |_|  \___|  \___|  \__|  _____  |___/  \___|  \___|  \__,_| (_) | .__/   \__, |    #
#                                        |_____|                                 |_|      |___/     #
#                                                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Est. June 26, 2020 (6/26/2020)  #
# # # # # # # # # # # # # # # # # #
# SINA BIOMEDICAL RESEARCH GROUP  #
#   +-- S. Kaisar Alam (PI)       #
#   +-- Areeq I. Hasan (Lead)     #
#   +-- Sarina M. Hasan (Assgn.)  #
#   +-- Raiyah Z. Ahmed           #
#   +-- Wasi S. Ahmed             #
# # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# select_seed()                                                                               #
# Computes the ratio between the area of a lesion in a given b-mode and strain image pair.    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- image_directory: (string) | Path to the directory containing strain.png & b-mode.png  #
# @ output                                                                                    #
#   +-- area_ratio:      (double) | the area ratio between strain and b-mode masks.           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# % Steps:
# 1. Pre-processing (@ preprocess.py)
# 2. Segment via Otsu Thresholding
# 3. Seed Generation
# 4. Ranking
# 5. Seed Point Geneneration
# 6. Refining Seed Point
# 7. Seed Point Display/Return

import cv2
import numpy as np
from matplotlib import pyplot as plt
from preprocessing_methods import preprocess

def select_seed(image_filepath):

    image_type = "strain" if image_filepath[-5:] == "n.jpg" else "bmode"
    print(image_filepath[-5:])

    processed_image, _ = preprocess(image_filepath)

    if image_type == "strain":
        threshold = 70
        _, binarized_image = cv2.threshold(processed_image, threshold, 255, cv2.THRESH_BINARY_INV)

        titles = ['Processed Image', 'Binarized Image']
        figures = [processed_image, binarized_image]

        for i in range(len(figures)):
            plt.subplot(2,3,i+1), plt.imshow(figures[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])

        plt.show()

        # %% Calculating features for energy function
        # [labeledImage, ~] = bwlabel(isolatedLesion ~= 0);
        # measurements = regionprops(labeledImage,'Centroid');
        # allCentroids = [measurements.Centroid];
        # xCentroids = allCentroids(1:2:end);     % Column coordinate for candidate seeds
        # yCentroids = allCentroids(2:2:end);     % Row coordinate for candidate seeds
        #
        # % Creating Seed Points Possibilities
        #
        # xCentroids = round(xCentroids);
        # yCentroids = round(yCentroids);
        #
        # [rmax, cmax]=size(joint);
        # k1 = 1; k2 = 5;
        # for image = 1:length(xCentroids)
        #     current_row = yCentroids(image);
        #
        #     if current_row + 10 > rmax
        #         new_row = [yCentroids(image), yCentroids(image) - 10, yCentroids(image), rmax];
        #     elseif yCentroids(image) - 10 < 1
        #         new_row = [yCentroids(image), 1, yCentroids(image), yCentroids(image) + 10];
        #     else
        #         new_row = [yCentroids(image), yCentroids(image) - 10, yCentroids(image), yCentroids(image) + 10];
        #     end
        # 
        #     if xCentroids(image) + 10 > cmax
        #         new_col = [xCentroids(image) - 10, xCentroids(image), cmax, xCentroids(image)];
        #     elseif xCentroids(image) - 10 < 1
        #         new_col = [1, xCentroids(image), xCentroids(image) + 10, xCentroids(image)];
        #     else
        #         new_col = [xCentroids(image) - 10, xCentroids(image), xCentroids(image) + 10, xCentroids(image)];
        #     end
        #
        #     row_can_seed(k1:k2)=[yCentroids(image) new_row];
        #     col_can_seed(k1:k2)=[xCentroids(image) new_col];
        #     k1 = k1 + 5;
        #     k2 = k2 + 5;
        # end
        #
        # % Refining Candidate Seeds
        #
        # for p = 1:length(row_can_seed)
        #
        #     if row_can_seed(p) > rmax
        #         row_can_seed(p) = rmax;
        #     end
        #
        #     if col_can_seed(p) > cmax
        #         col_can_seed(p) = cmax;
        #     end
        #
        #     plot(col_can_seed(p), row_can_seed(p), 'g*');
        # end
        #
        # % Image Center Determination
        #
        # Dum_Im = ones(size(isolatedLesion));
        # [labIm, ~] = bwlabel(Dum_Im ~= 0);
        # meas = regionprops(labIm,'Centroid');
        # cen = [meas.Centroid];  % Center
        # imX = round(cen(1, 1));  % Column
        # [pr, ~] = size(isolatedLesion);
        # imY = round(pr/3); % Row
        #
        # for image = 1:length(row_can_seed)
        #     eu_dis = Distance(row_can_seed(image), col_can_seed(image), imY, imX);
        #     joint_value = joint(row_can_seed(image), col_can_seed(image));                 % Joint Probabilty @ current seed
        #     [xgrid, ygrid] = meshgrid(1:size(joint, 2), 1:size(joint, 1));
        #     mask = ((xgrid - col_can_seed(image)).^2 + (ygrid-row_can_seed(image)).^2) <= 20.^2;
        #     values = joint(mask);
        #     total = sum(sum(values));
        #     av = total;
        #     av1 = entropyFiltered(row_can_seed(image), col_can_seed(image)); % Entropy @ seed point
        #     val(image)=(av*joint_value)./(eu_dis*av1);
        # end
        #
        # seed = find(val == max(val));
        # r_seed = row_can_seed(seed);
        # c_seed = col_can_seed(seed);
        #
        # %% Displaying seed point atop original image.
        # offset1 = 0;
        # centerX = r_seed(1);
        # centerY = c_seed(1)+offset1;

    else:
        pass

    # return seed_x, seed_y

select_seed("../../Data/Frames/Malignant/10-58-09/234/strain.jpg")
